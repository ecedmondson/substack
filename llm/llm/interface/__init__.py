import os
import re
import json
import requests
from functools import cached_property

from transformers import AutoTokenizer, AutoModelForCausalLM, PreTrainedModel
from transformers import AutoModelForSeq2SeqLM, pipeline
import torch

from settings.model_settings import ModelSettingsBase
from settings.interface_types import ModelInterfaceType
from llm.interface.utils import extract_text_from_pdf

# seems interesting: https://docs.chainlit.io/data-persistence/overview
class ModelInterface:
    MODEL_REGISTRY = {}

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if "MODEL_TYPE" in cls.__dict__:
            cls.MODEL_REGISTRY[cls.MODEL_TYPE] = cls

    def __init__(self, config: ModelSettingsBase):
        self.config = config
    
    @cached_property
    def tokenizer(self):
        path = self.config.save_path if os.path.isdir(self.config.save_path) else self.config.model_repo
        return AutoTokenizer.from_pretrained(path)

    def chunks(self, text, max_tokens=512):
        tokens = self.tokenizer.tokenize(text)
        chunks = []
        start = 0
        
        while start < len(tokens):
            end = min(start + max_tokens, len(tokens))
            # Get tokens chunk and convert back to string
            chunk_tokens = tokens[start:end]
            chunk_text = self.tokenizer.convert_tokens_to_string(chunk_tokens)
            chunks.append(chunk_text)
            start = end
        
        return chunks

    def prompt(self, message: str):
        ...

class DecoderOnlyModelInterface(ModelInterface):
    MODEL_TYPE = ModelInterfaceType.DECODER
    @cached_property
    def model(self):
        path = self.config.save_path if os.path.isdir(self.config.save_path) else self.config.model_repo
        return AutoModelForCausalLM.from_pretrained(path, return_dict=True, trust_remote_code=True)

    @cached_property
    def text_generation_pipeline(self):
        return pipeline(
            "text-generation",
            model=self.model,
            tokenizer=self.tokenizer,
        )

    def prompt(self, message: str):
        sequences = self.text_generation_pipeline(
            message,
            max_new_tokens=100,
            do_sample=False,
            eos_token_id=self.tokenizer.eos_token_id,
        )
        return [seq["generated_text"] for seq in sequences]


class Seq2SeqModelInterface(ModelInterface):
    MODEL_TYPE = ModelInterfaceType.SEQ2SEQ
    @cached_property
    def model(self):
        path = self.config.save_path if os.path.isdir(self.config.save_path) else self.config.model_repo
        return AutoModelForSeq2SeqLM.from_pretrained(
            path,
            return_dict=True,
        )

    @cached_property
    def summary_pipeline(self):
        return pipeline(
            "text2text-generation",
            model=self.model,
            tokenizer=self.tokenizer,
        )

    def prompt(self, message: str, max_new_tokens: int = None, do_sample: bool = False):
        final_tokens = max_new_tokens or 350 # default
        all_summaries = []
        chunks = self.chunks(message)
        print(len(chunks), chunks)

        for chunk in chunks:
            if not max_new_tokens:
                final_tokens = max(final_tokens, int(len(self.tokenizer.encode(chunk)) * 0.8))
            print("using this many max new tokens", final_tokens)
            sequences = self.summary_pipeline(
                chunk,
                max_new_tokens=final_tokens,
                do_sample=do_sample,
                temperature=1.5,
                top_p=0.95,
            )
            all_summaries.extend(seq["generated_text"] for seq in sequences)

        return all_summaries

class OllamaModelInterface(ModelInterface):
    MODEL_TYPE = ModelInterfaceType.OLLAMA

    @cached_property
    def model(self):
        return AutoModelForCausalLM.from_pretrained(self.config.org_path)

    def chunks(self, text, max_chars=1000):
        return [text[i:i+max_chars] for i in range(0, len(text), max_chars)]

    def semantic_chunks(self, text, max_chars=3500) -> dict:
        def preprocess_paragraphs(paragraphs, min_length=150):
            grouped = []
            current = ""
            for para in paragraphs:
                para = para.strip()
                if not para:
                    continue
                if len(current) + len(para) < min_length:
                    current += " " + para
                else:
                    if current:
                        grouped.append(current.strip())
                    current = para
            if current:
                grouped.append(current.strip())
            return grouped

        paragraphs = re.split(r'\n\s*\n', text.strip())
        paragraphs = preprocess_paragraphs(paragraphs)
        
        chunks = {}
        current_chunk = ""
        index = 0

        for para in paragraphs:
            if len(current_chunk) + len(para) + 2 < max_chars:
                current_chunk += para + "\n\n"
            else:
                if current_chunk:
                    chunks[index] = current_chunk.strip()
                    index += 1
                current_chunk = para + "\n\n"

        if current_chunk:
            chunks[index] = current_chunk.strip()

        return chunks



    def ollama_prompt(self, prompt_text):
        # url = f"http://localhost:12345/models/{self.config.MODEL_NAME}"
        url = "http://127.0.0.1:12345/api/generate"
        headers = {"Content-Type": "application/json"}
        payload = {
            "model": self.config.MODEL_NAME,
            "prompt": prompt_text,
            "stream": False,
            "max_token": 2000,
            "temperature": 0.6,
        }
        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()
            result = data.get("response", "LLM Response not found.")
            print(result)
            return result
        except requests.RequestException as e:
            print(f"Ollama API request failed: {e}")
            return ""

    def summarize_prompt(self, message: str, chunk_index: int, total_chunk_count: int) -> str:
        return f"""
            You will analyze the following text selection. Please do the following:

            1. Provide a concise summary of the selection.
            2. Identify and extract key quotes (exact language or phrases) that indicate **authoritarian parenting**.
            3. Identify and extract key quotes that indicate **non-authoritarian parenting models** (such as authoritative, permissive, or other styles).
            4. Identify and extract key quotes that reflect **societal constructs or worldviews** mentioned or implied in the text.
            5. Present your results in a clearly formatted output with headings and bullet points.

            Analyze the following section of a longer text. This may be part of a larger argument. Be cautious about attributing positions to the author unless clearly stated. Look for signs of ongoing critique, support, or neutrality.
            Here is the order of this selection: chunk {chunk_index} out of { total_chunk_count} chunks

            Here is the text selection:

            ```
            {message}
            ```

            ---

            Output format:

            Summary:
            - [Concise summary here]

            Key quotes indicating authoritarian parenting:
            - "[Quote 1]"
            - "[Quote 2]"
            - ...

            Key quotes indicating non-authoritarian parenting models:
            - "[Quote 1]"
            - "[Quote 2]"
            - ...

            Key quotes indicating societal constructs or worldviews:
            - "[Quote 1]"
            - "[Quote 2]"
            - ...
        """

    def prompt(self, message: str):
        chunks = self.semantic_chunks(message, max_chars=3500)
        summaries = {}
        total_chunks = max(list(chunks.keys()))
        for idx, chunk in chunks.items():
            print(f"Getting summary {idx}/{total_chunks}...")
            prompt_text = f"Summarize the following text. If there is any language, phrasing, or conceptual models of authoritarian parenting or child abuse, draw attention to those in the summary:\n\n{chunk}"
            summary = self.ollama_prompt(self.summarize_prompt(prompt_text, idx, total_chunks))
            summaries[idx] = summary.strip()
        return summaries

    def summarize_pdf(self, pdf_path):
        pdf_text = extract_text_from_pdf(pdf_path)
        results = f"{pdf_path.split('.')[0]}_results.json"
        summary_results = self.prompt(pdf_text)
        with open(results, "w") as f:
            json.dump(summary_results, f, indent=4)

def model_interface_factory(model_type: ModelInterfaceType) -> ModelInterface:
    return ModelInterface.MODEL_REGISTRY[model_type]

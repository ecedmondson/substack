import os
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
    MODEL_TYPE = ModelInterfaceType.OLLAMA  # You’ll need to define this enum value

    @cached_property
    def model(self):
        return AutoModelForCausalLM.from_pretrained(self.config.org_path)


    def prompt(self, message: str):
        chunks = self.chunks(message, max_tokens=500)  # conservative chunking for llama3
        summaries = []
        for chunk in chunks:
            print("Getting summary...")
            prompt_text = f"Summarize the following text:\n\n{chunk}"
            summary = ollama_prompt(prompt_text, model=self.config.model_repo)  # model_repo holds "llama3" or similar
            summaries.append(summary.strip())
        return summaries

    def summarize_pdf(self, pdf_path):
        pdf_text = extract_text_from_pdf(pdf_path)
        return self.prompt(pdf_text)

def model_interface_factory(model_type: ModelInterfaceType) -> ModelInterface:
    return ModelInterface.MODEL_REGISTRY[model_type]

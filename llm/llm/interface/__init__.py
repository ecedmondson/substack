import os
from functools import cached_property

from transformers import AutoTokenizer, AutoModelForCausalLM, PreTrainedModel
from transformers import AutoModelForSeq2SeqLM, pipeline
import torch

from settings.model_settings import ModelSettingsBase

# seems interesting: https://docs.chainlit.io/data-persistence/overview
class ModelInterface(ABC):
    MODEL_REGISTRY = {}

    def __init_subclass__(cls, model_type: str, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.MODEL_REGISTRY[model_type] = cls

    def __init__(self, config: ModelSettingsBase):
        self.config = config

    @cached_property
    def tokenizer(self):
        path = self.config.save_path if os.path.isdir(self.config.save_path) else self.config.model_repo
        return AutoTokenizer.from_pretrained(path)
    
    def prompt(self, message: str):
        ...

class DecoderOnlyModelInterface(ModelInterface, model_type="decoder"):
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


class Seq2SeqModelInterface(ModelInterface, model_type="seq2seq"):
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

    def prompt(self, message: str):
        sequences = self.summary_pipeline(
            message,
            max_new_tokens=100,
            do_sample=False,
        )
        return [seq["generated_text"] for seq in sequences]

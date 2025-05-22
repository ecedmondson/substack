import re
import os

from pathvalidate import sanitize_filename
from pydantic_settings import BaseSettings
from settings.interface_types import ModelInterfaceType

from pydantic import Field

import re


def normalize_dir_name(pathname):
    if pathname[-1] != "/":
        return pathname + "/"
    return pathname

class ModelSettingsBase(BaseSettings):
    # Does not validate valid path from os env
    LOCAL_PATH: str = Field(default=os.environ.get('LLM_LOCAL_PATH', '/Users/new/Development/llms/'), allow_mutation=False)
    MODEL_NAME: str = ""
    ORGANIZATION_NAME: str = ""
    MODEL_TYPE: ModelInterfaceType = Field(default="decoder")

    @property
    def save_path(self) -> str:
        return f"{normalize_dir_name(self.LOCAL_PATH)}{sanitize_filename(self.MODEL_NAME)}"
    
    @property
    def model_repo(self):
        return f"{self.ORGANIZATION_NAME}/{self.MODEL_NAME.lower()}"
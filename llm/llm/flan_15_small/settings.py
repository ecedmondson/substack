from settings.model_settings import ModelSettingsBase
from llm.interface import ModelInterface

config = ModelSettingsBase(MODEL_NAME="flan-t5-small", ORGANIZATION_NAME="google")

flan_interface = ModelInterface(config)
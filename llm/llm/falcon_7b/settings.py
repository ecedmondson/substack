from settings.model_settings import ModelSettingsBase
from llm.interface import ModelInterface

config = ModelSettingsBase(MODEL_NAME="Falcon-7B", ORGANIZATION_NAME="tiiuae")

falcon_interface = ModelInterface(config)
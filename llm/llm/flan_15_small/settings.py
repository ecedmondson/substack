from settings.model_settings import ModelSettingsBase
from settings.interface_types import ModelInterfaceType
from llm.interface import model_interface_factory

config = ModelSettingsBase(MODEL_NAME="flan-t5-small", ORGANIZATION_NAME="google", MODEL_TYPE=ModelInterfaceType.SEQ2SEQ)

flan_interface = model_interface_factory(config.MODEL_TYPE)(config)
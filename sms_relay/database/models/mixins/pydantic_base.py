from pydantic import BaseModel, ConfigDict

class PydanticBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
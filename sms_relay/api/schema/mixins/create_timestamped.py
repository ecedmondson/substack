from datetime import datetime

from api.schema.pydantic_base import PydanticBase
from pydantic import Field


class CreatedTimestampedPydanticMixin(PydanticBase):
    created: datetime = Field(..., read_only=True)

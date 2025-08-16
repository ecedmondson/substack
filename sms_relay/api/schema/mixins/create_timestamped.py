from datetime import datetime

from database.models.mixins.pydantic_base import PydanticBase
from pydantic import Field


class CreatedTimestampedPydanticMixin(PydanticBase):
    created: datetime = Field(..., read_only=True)

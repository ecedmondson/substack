from typing import Optional
from uuid import UUID as UUIDTyping

from database.models.mixins.pydantic_base import PydanticBase
from pydantic import Field


class UUIDPrimaryKeyPydanticMixin(PydanticBase):
    id: Optional[UUIDTyping] = Field(..., read_only=True)
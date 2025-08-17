from typing import Optional
from uuid import UUID as UUIDTyping

from api.schema.pydantic_base import PydanticBase
from pydantic import Field


class UUIDPrimaryKeyPydanticMixin(PydanticBase):
    id: Optional[UUIDTyping] = Field(..., read_only=True)
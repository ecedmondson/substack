from uuid import UUID as UUIDTyping, uuid4
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from pydantic import BaseModel, Field
from database.models.mixins.pydantic_base import PydanticBase
from typing import Optional

class UUIDPrimaryKey:
    id: Mapped[UUIDTyping] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)

class UUIDPrimaryKeyPydanticMixin(PydanticBase):
    id: Optional[UUIDTyping] = Field(..., read_only=True)
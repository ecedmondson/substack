from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Text, String
from uuid import UUID as UUIDTyping
from typing import List

from database.models.mixins.created_timestamped import (
    CreatedTimestamped, CreatedTimestampedPydanticMixin)
from database.models.mixins.primary_key import (UUIDPrimaryKey,
                                                UUIDPrimaryKeyPydanticMixin)
from database.models.forwarding.contact import ContactShape
from pydantic import BaseModel
from database.models.base  import DeclarativeBase
from database.models.mixins.pydantic_base import PydanticBase

class ForwardedMessage(DeclarativeBase, UUIDPrimaryKey, CreatedTimestamped):
    __tablename__ = "forwarded_message"

    message: Mapped[str] = mapped_column(Text, nullable=False)
    date: Mapped[str] = mapped_column(String(35), nullable=False)
    contact_id: Mapped[UUIDTyping] = mapped_column(ForeignKey("contact.id"), nullable=False)
    contact: Mapped["Contact"] = relationship("Contact", back_populates="messages")

class MessageRequest(PydanticBase):
    message: str
    sender: str
    date: str

class MessageResponse(UUIDPrimaryKeyPydanticMixin, CreatedTimestampedPydanticMixin):
    message: str
    date: str
    contact: ContactShape

class MessageListResponse(UUIDPrimaryKeyPydanticMixin):
    message: str
    contact: ContactShape

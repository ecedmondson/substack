from datetime import datetime
from uuid import UUID as UUIDTyping

from database.models.base import DeclarativeBase
from database.models.mixins.created_timestamped import CreatedTimestamped
from database.models.mixins.primary_key import UUIDPrimaryKey
from sqlalchemy import Boolean, ForeignKey, Index, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship


class ForwardedMessage(DeclarativeBase, UUIDPrimaryKey, CreatedTimestamped):
    __tablename__ = "forwarded_message"

    message: Mapped[str] = mapped_column(Text, nullable=False)
    date: Mapped[str] = mapped_column(String(35), nullable=False)
    device: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False
    )
    contact_id: Mapped[UUIDTyping] = mapped_column(ForeignKey("contact.id"), nullable=True)
    contact: Mapped["Contact"] = relationship("Contact", back_populates="messages") # noqa: F821
    relayed: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False
    )
    integration_id: Mapped[UUIDTyping] = mapped_column(ForeignKey("integration_webhook_payload.id"), nullable=True)
    integration_contact_id: Mapped[UUIDTyping] = mapped_column(ForeignKey("integration_contact.id"), nullable=True)
    integration_contact: Mapped["IntegrationContact"] = relationship("IntegrationContact", back_populates="messages") # noqa: F821
    
    thread_id: Mapped[UUIDTyping] = mapped_column(ForeignKey("conversation_thread.id"), nullable=True)
    thread: Mapped["ConversationThread"] = relationship("ConversationThread", back_populates="messages")
    delivery_confirmed: Mapped[datetime] = mapped_column(nullable=True, index=True)

    __table_args__ = (
        Index("ix_forwarded_message_thread_date", "thread_id", "date"),
    )
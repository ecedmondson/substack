from uuid import UUID as UUIDTyping

from database.models.base import DeclarativeBase
from database.models.mixins.created_timestamped import CreatedTimestamped
from database.models.mixins.primary_key import UUIDPrimaryKey
from sqlalchemy import ForeignKey, Index, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


class ConversationThread(DeclarativeBase, UUIDPrimaryKey, CreatedTimestamped):
    __tablename__ = "conversation_thread"

    contact_id: Mapped[UUIDTyping] = mapped_column(ForeignKey("contact.id"), nullable=False)
    contact: Mapped["Contact"] = relationship("Contact", back_populates="threads") # noqa: F821
    # save a join
    phone_number_used: Mapped[str] = mapped_column(String(15), nullable=False)
    integration_contact_id: Mapped[UUIDTyping] = mapped_column(ForeignKey("integration_contact.id"), nullable=True)
    integration_contact: Mapped["IntegrationContact"] = relationship("IntegrationContact", back_populates="threads") # noqa: F821
    messages: Mapped[list["ForwardedMessage"]] = relationship(
        "ForwardedMessage",
        back_populates="thread",
        cascade="all, delete-orphan",
        order_by="ForwardedMessage.date"  # auto-order messages when loaded, by date for thread
    )

    __table_args__ = (
        Index("ix_conversation_thread_contact", "contact_id"),
    )

# insert into integration_contact (address, id, provider) values ('+18722491108', '5bf9aae6-f19d-4848-ad2b-5a364ce3a3b5', 'TELNYX');
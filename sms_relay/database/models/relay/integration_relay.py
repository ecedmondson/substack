from enum import Enum

from database.models.base import DeclarativeBase
from database.models.mixins.primary_key import UUIDPrimaryKey
from sqlalchemy import JSON
from sqlalchemy import Enum as SQLEnum
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship


class IntegrationProvider(Enum):
    TELNYX = "TELNYX"


class IntegrationContact(DeclarativeBase, UUIDPrimaryKey):
    __tablename__ = "integration_contact"

    provider: Mapped[IntegrationProvider] = mapped_column(
        SQLEnum(IntegrationProvider, name="integration_provider"),
        nullable=False,
    )
    address: Mapped[str] = mapped_column(String(255), nullable=False)
    threads: Mapped[list["ConversationThread"]] = relationship("ConversationThread", back_populates="integration_contact")
    messages: Mapped[list["ForwardedMessage"]] = relationship("ForwardedMessage", back_populates="integration_contact")

class IntegrationPayload(DeclarativeBase, UUIDPrimaryKey):
    __tablename__ = "integration_webhook_payload"

    payload: Mapped[JSON] = mapped_column(type_=JSON)

    provider: Mapped[IntegrationProvider] = mapped_column(
        SQLEnum(IntegrationProvider, name="integration_provider"),
        nullable=False,
    )

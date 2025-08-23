
from datetime import datetime
from typing import Optional, Union
from uuid import UUID

from api.schema.forwarding.contact import ContactShape, ContactSummary
from api.schema.integration.integration import IntegrationContactSummary
from api.schema.mixins.create_timestamped import \
    CreatedTimestampedPydanticMixin
from api.schema.mixins.primary_key import UUIDPrimaryKeyPydanticMixin
from api.schema.pydantic_base import PydanticBase
from pydantic import model_validator


class MessageRequest(PydanticBase):
    message: str
    sender: str
    date: str
    relayed: bool = False
    device: bool = True
    integration: Optional[str] = None
    integration_contact_id: Optional[str] = None

class MessageResponse(UUIDPrimaryKeyPydanticMixin, CreatedTimestampedPydanticMixin):
    message: str
    date: str
    contact: Optional[ContactShape]
    integration_contact: Optional[IntegrationContactSummary]

class MessageSummary(UUIDPrimaryKeyPydanticMixin, CreatedTimestampedPydanticMixin):
    message: str
    date: str
    contact: Optional[ContactSummary]
    integration_contact: Optional[IntegrationContactSummary]

class MessageListResponse(UUIDPrimaryKeyPydanticMixin):
    message: str
    contact: ContactShape

class MessageThreadResponse(UUIDPrimaryKeyPydanticMixin):
    message: str
    date: str

    sender: Union[ContactSummary, IntegrationContactSummary]

    @model_validator(mode="before")
    @classmethod
    def normalize_contact_fields(cls, message):
        if hasattr(message, "contact") and message.contact is not None:
            message.sender = message.contact
            return message
        if hasattr(message, "integration_contact") and message.integration_contact is not None:
            message.sender = message.integration_contact
            return message

class OutgoingMessage(PydanticBase):
    message: str
    sender: str
    date: datetime
    relayed: bool = False
    device: bool = False
    integration_contact_id: UUID
    thread_id: str

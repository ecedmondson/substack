from datetime import datetime
from uuid import UUID

from api.schema.mixins.primary_key import UUIDPrimaryKeyPydanticMixin
from api.schema.pydantic_base import PydanticBase
from pydantic import Field


class TelnyxSMSIDException(Exception):
    pass

class ExpectedTelnyxWebhookShape(PydanticBase):
    sms_id: str
    direction: str
    from_number: str = Field(..., alias="from")
    to_number: str = Field(..., alias="to")
    message_body: str = Field(..., alias="body")

class TelnyxWebhookCreation(UUIDPrimaryKeyPydanticMixin):
    provider: str
    payload: dict

class TelnyxPayloadToMessage(PydanticBase):
    message: str
    sender: str
    date: datetime
    relayed: bool = True
    device: bool = False
    integration: UUID
    integration_contact_id: UUID

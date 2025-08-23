from datetime import datetime
from typing import Optional
from uuid import UUID

from api.schema.forwarding.contact import ContactSummary
from api.schema.forwarding.message import MessageSummary
from api.schema.integration.integration import IntegrationContactSummary
from api.schema.pydantic_base import PydanticBase


class ConversationThread(PydanticBase):
    id: UUID
    created: datetime
    phone_number_used: str
    contact: Optional[ContactSummary]
    integration_contact: Optional[IntegrationContactSummary]
    most_recent_message: Optional[MessageSummary] = None

class ConversationResponse(PydanticBase):
    message_body: str
    phone_number_used: str
    integration_contact_id: UUID
    

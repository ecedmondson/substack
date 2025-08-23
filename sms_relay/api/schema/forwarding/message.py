
from typing import Optional

from api.schema.forwarding.contact import ContactShape
from api.schema.mixins.create_timestamped import \
    CreatedTimestampedPydanticMixin
from api.schema.mixins.primary_key import UUIDPrimaryKeyPydanticMixin
from api.schema.pydantic_base import PydanticBase


class MessageRequest(PydanticBase):
    message: str
    sender: str
    date: str
    relayed: bool = False
    integration: Optional[str] = None

class MessageResponse(UUIDPrimaryKeyPydanticMixin, CreatedTimestampedPydanticMixin):
    message: str
    date: str
    contact: ContactShape

class MessageListResponse(UUIDPrimaryKeyPydanticMixin):
    message: str
    contact: ContactShape

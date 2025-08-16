from typing import List, Optional
from uuid import UUID as UUIDTyping

from api.schema.mixins.primary_key import UUIDPrimaryKeyPydanticMixin
from api.schema.pydantic_base import PydanticBase


class PhoneNumberShape(PydanticBase):
    id: Optional[UUIDTyping] = None
    contact_id: Optional[UUIDTyping] = None
    number: str


class ContactShape(UUIDPrimaryKeyPydanticMixin):
    first_name: Optional[str]
    last_name: Optional[str]
    note: Optional[str]
    phone_numbers: Optional[List[PhoneNumberShape]] = None



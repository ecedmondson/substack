from typing import Optional
from uuid import UUID

from database.models.mixins.primary_key import (UUIDPrimaryKey,
                                                UUIDPrimaryKeyPydanticMixin)
from database.models.mixins.tortoise import TortoiseModelMixin
from pydantic import field_validator
from tortoise import fields


class Contact(UUIDPrimaryKey):
    first_name = fields.CharField(max_length=255, null=True)
    last_name = fields.CharField(max_length=255, null=True)
    note = fields.TextField(null=True)

class ContactShape(TortoiseModelMixin, UUIDPrimaryKeyPydanticMixin):
    first_name: Optional[str]
    last_name: Optional[str]
    note: Optional[str]

class PhoneNumber(UUIDPrimaryKey):
    number = fields.CharField(max_length=15)
    contact = fields.ForeignKeyField('models.Contact', related_name='phone_numbers')

class PhoneNumberShape(TortoiseModelMixin, UUIDPrimaryKeyPydanticMixin):
    number: str
    contact: UUID

    class Meta:
        orm_model = PhoneNumber
    
    @field_validator("contact", mode="before")
    def parse_contact(cls, value):
        # Already sanitized to PKID
        if isinstance(value, UUID):
            return value
        return value.id



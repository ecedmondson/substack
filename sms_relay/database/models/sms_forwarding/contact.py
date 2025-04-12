from typing import List, Optional

from database.models.mixins.primary_key import (UUIDPrimaryKey,
                                                UUIDPrimaryKeyPydanticMixin)
from tortoise import fields
from tortoise.transactions import in_transaction


# Why this setup? Because I know people and organizations who have more than one number
# and message me. Examples: Mom. Vanguard Investments.
class PhoneNumber(UUIDPrimaryKey):
    number = fields.CharField(max_length=15)
    contact = fields.ForeignKeyField('models.Contact', related_name='phone_numbers')

class PhoneNumberShape(UUIDPrimaryKeyPydanticMixin):
    number: str


class Contact(UUIDPrimaryKey):
    first_name = fields.CharField(max_length=255, null=True)
    last_name = fields.CharField(max_length=255, null=True)
    note = fields.TextField(null=True)

    @classmethod
    async def get_by_phone_number(cls, phone_number: str):
        phonenumber = await PhoneNumber.filter(number=phone_number).prefetch_related("contact").first()
        if phonenumber:
            return phonenumber.contact
        return None

    @classmethod
    async def get_or_create(cls, sender_phone_number: str):
        contact = await cls.get_by_phone_number(sender_phone_number)
        if contact:
            return contact
        async with in_transaction():
            contact = await Contact.create(
                first_name="Unknown",
                note=f"Auto-created with new sender number {sender_phone_number!r}."
            )
            await PhoneNumber.create(
                number=sender_phone_number,
                contact=contact
            )
            return contact


class ContactShape(UUIDPrimaryKeyPydanticMixin):
    first_name: Optional[str]
    last_name: Optional[str]
    note: Optional[str]
    phone_numbers: Optional[List[PhoneNumberShape]] = None





from database.models.mixins.created_timestamped import (
    CreatedTimestamped, CreatedTimestampedPydanticMixin)
from database.models.mixins.primary_key import (UUIDPrimaryKey,
                                                UUIDPrimaryKeyPydanticMixin)
from database.models.sms_forwarding.contact import Contact, ContactShape
from pydantic import BaseModel
from tortoise import fields
from tortoise.transactions import in_transaction

# from tortoise.contrib.pydantic.creator import pydantic_model_creator


class ForwardedMessage(UUIDPrimaryKey, CreatedTimestamped):
    message = fields.TextField(null=False, description="Actual message forwarded.")
    date = fields.CharField(max_length=35, null=False, description="Date that the message was forwarded.")
    contact = fields.ForeignKeyField('models.Contact', related_name="messages")

    class Meta:
        table = "forwarded_message"
    
    @classmethod
    async def create_new(cls, message, date, contact):
        return await ForwardedMessage.create(message=message, date=date, contact=contact)
        

class MessageRequest(BaseModel):
    message: str
    sender: str
    date: str

    async def create_forwarded_message(self):
        async with in_transaction():
            contact = await Contact.get_or_create(self.sender)
            return await ForwardedMessage.create_new(self.message, self.date, contact)

    class Config:
        from_attributes = True

class MessageResponse(UUIDPrimaryKeyPydanticMixin, CreatedTimestampedPydanticMixin):
    message: str
    date: str
    contact: ContactShape

    class Config:
        from_attributes=True

    @classmethod
    async def from_tortoise(cls, message_obj):
        contact = await message_obj.contact
        return cls.model_validate({
            "id": message_obj.id,
            "created": message_obj.created,
            "message": message_obj.message,
            "date": message_obj.date,
            "contact": ContactShape.model_validate({
                "id": contact.id,
                "first_name": contact.first_name,
                "last_name": contact.last_name,
                "note": contact.note,
            })
        })


# This would be cool but has an api error in tortoise.
# look into it later.
# MessageShape = pydantic_model_creator(Message, name="MessageShape")
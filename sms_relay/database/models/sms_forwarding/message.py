from database.models.mixins.created_timestamped import (
    CreatedTimestamped, CreatedTimestampedPydanticMixin)
from database.models.mixins.primary_key import (UUIDPrimaryKey,
                                                UUIDPrimaryKeyPydanticMixin)
from database.models.mixins.tortoise import TortoiseModelMixin
from tortoise import fields

# from tortoise.contrib.pydantic.creator import pydantic_model_creator


class Message(UUIDPrimaryKey, CreatedTimestamped):
    message = fields.TextField(null=False)
    sender = fields.CharField(max_length=255, null=False)
    date = fields.CharField(max_length=35, null=False)

class MessageRequest(TortoiseModelMixin):
    message: str
    sender: str
    date: str

    class Meta:
        orm_model = Message
    
    class Config:
        from_attributes = True

class MessageResponse(UUIDPrimaryKeyPydanticMixin, CreatedTimestampedPydanticMixin, MessageRequest):
    pass

# This would be cool but has an api error in tortoise.
# look into it later.
# MessageShape = pydantic_model_creator(Message, name="MessageShape")
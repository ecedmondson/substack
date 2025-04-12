from datetime import datetime

from pydantic import BaseModel, Field
from tortoise import fields
from tortoise.models import Model


class CreatedTimestamped(Model):
    created = fields.DatetimeField(
        auto_now_add=True,
        help_text="Date/time object was created",
        db_index=True
    )

    class Meta:
        abstract = True

class CreatedTimestampedPydanticMixin(BaseModel):
    created: datetime = Field(..., read_only=True) # type: ignore
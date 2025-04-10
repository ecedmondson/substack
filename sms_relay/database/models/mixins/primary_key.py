from uuid import UUID, uuid4

from pydantic import BaseModel, Field
from tortoise import fields
from tortoise.models import Model


class UUIDPrimaryKey(Model):
    id = fields.UUIDField(primary_key=True, db_index=True, default=uuid4)

    class Meta:
        abstract = True


class UUIDPrimaryKeyPydanticMixin(BaseModel):
    id: UUID = Field(..., read_only=True) # type: ignore


from datetime import datetime
from pydantic import BaseModel, Field

from sqlalchemy.orm import Mapped, mapped_column
from database.models.mixins.pydantic_base import PydanticBase


class CreatedTimestamped:
    created: Mapped[datetime] = mapped_column(default=datetime.utcnow, index=True)


class CreatedTimestampedPydanticMixin(PydanticBase):
    created: datetime = Field(..., read_only=True)

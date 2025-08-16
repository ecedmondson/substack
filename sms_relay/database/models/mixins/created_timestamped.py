
from datetime import datetime
from pydantic import BaseModel, Field

from sqlalchemy.orm import Mapped, mapped_column


class CreatedTimestamped:
    created: Mapped[datetime] = mapped_column(default=datetime.utcnow, index=True)

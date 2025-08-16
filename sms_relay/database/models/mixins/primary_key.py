from uuid import UUID as UUIDTyping
from uuid import uuid4

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column


class UUIDPrimaryKey:
    id: Mapped[UUIDTyping] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)


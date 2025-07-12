from typing import List, Optional
from uuid import UUID as UUIDTyping
from uuid import uuid4


from database.models.mixins.pydantic_base import PydanticBase
from database.models.base import DeclarativeBase
from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.models.mixins.primary_key import (
                                                UUIDPrimaryKey, UUIDPrimaryKeyPydanticMixin)


class PhoneNumber(DeclarativeBase, UUIDPrimaryKey):
    __tablename__ = 'phone_number'

    number: Mapped[str] = mapped_column(String(15), nullable=False)
    contact_id: Mapped[UUIDTyping] = mapped_column(ForeignKey('contact.id'), nullable=False)

    contact: Mapped["Contact"] = relationship('Contact', back_populates='phone_numbers')


class PhoneNumberShape(PydanticBase):
    id: Optional[UUIDTyping] = None
    contact_id: Optional[UUIDTyping] = None
    number: str


class Contact(DeclarativeBase, UUIDPrimaryKey):
    __tablename__ = 'contact'

    first_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    last_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    note: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    phone_numbers: Mapped[List["PhoneNumber"]] = relationship('PhoneNumber', back_populates='contact')
    messages: Mapped[List["ForwardedMessage"]] = relationship('ForwardedMessage', back_populates='contact')

class ContactShape(UUIDPrimaryKeyPydanticMixin):
    first_name: Optional[str]
    last_name: Optional[str]
    note: Optional[str]
    phone_numbers: Optional[List[PhoneNumberShape]] = None



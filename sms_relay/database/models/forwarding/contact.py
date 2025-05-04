from typing import List, Optional
from uuid import UUID as UUIDTyping, uuid4

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.models.mixins.primary_key import UUIDPrimaryKey, UUIDPrimaryKeyPydanticMixin
from database.models.base import DeclarativeBase
from database.models.mixins.pydantic_base import PydanticBase


class PhoneNumber(DeclarativeBase):
    __tablename__ = 'phone_number'

    id: Mapped[UUIDTyping] = mapped_column(primary_key=True, default=uuid4)
    number: Mapped[str] = mapped_column(String(15), nullable=False)
    contact_id: Mapped[UUIDTyping] = mapped_column(ForeignKey('contact.id'), nullable=False)

    contact: Mapped["Contact"] = relationship('Contact', back_populates='phone_numbers')


class PhoneNumberShape(PydanticBase):
    id: Optional[UUIDTyping] = None
    contact_id: Optional[UUIDTyping] = None
    number: str


class Contact(DeclarativeBase):
    __tablename__ = 'contact'

    id: Mapped[UUIDTyping] = mapped_column(primary_key=True, default=uuid4)
    first_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    last_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    note: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    phone_numbers: Mapped[List["PhoneNumber"]] = relationship('PhoneNumber', back_populates='contact')
    messages: Mapped[List["ForwardedMessage"]] = relationship('ForwardedMessage', back_populates='contact')


class ContactShape(PydanticBase):
    first_name: Optional[str]
    last_name: Optional[str]
    note: Optional[str]
    phone_numbers: Optional[List[PhoneNumberShape]] = None

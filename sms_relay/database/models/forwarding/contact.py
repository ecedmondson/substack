from typing import List, Optional
from uuid import UUID as UUIDTyping

from database.models.base import DeclarativeBase
from database.models.mixins.primary_key import UUIDPrimaryKey
from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship


class PhoneNumber(DeclarativeBase, UUIDPrimaryKey):
    __tablename__ = 'phone_number'

    number: Mapped[str] = mapped_column(String(15), nullable=False)
    contact_id: Mapped[UUIDTyping] = mapped_column(ForeignKey('contact.id'), nullable=False)

    contact: Mapped["Contact"] = relationship('Contact', back_populates='phone_numbers')


class Contact(DeclarativeBase, UUIDPrimaryKey):
    __tablename__ = 'contact'

    first_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    last_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    note: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    phone_numbers: Mapped[List["PhoneNumber"]] = relationship('PhoneNumber', back_populates='contact')
    messages: Mapped[List["ForwardedMessage"]] = relationship('ForwardedMessage', back_populates='contact')

    rules: Mapped[List["ContactRuleConfig"]] = relationship(
        back_populates="contact",
        lazy="selectin",
        cascade="all, delete-orphan",
    )

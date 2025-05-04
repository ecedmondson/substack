from typing import Optional
from database.models.forwarding.contact import Contact, PhoneNumber

from sqlalchemy import select
from sqlalchemy.orm import Session

class PhoneNumberQueryService:
    @classmethod
    def create(cls, session: Session, phone_number: str, contact: Contact) -> PhoneNumber:
        phone = PhoneNumber(number=phone_number, contact=contact)
        session.add(phone)
        session.commit()
        session.refresh(phone)
        return phone


class ContactQueryService:
    @classmethod
    def get_by_phone_number(cls, session: Session, phone_number: str) -> Optional[Contact]:
        result = session.execute(
            select(PhoneNumber).where(PhoneNumber.number == phone_number)
        )
        phone = result.scalars().first()
        return phone.contact if phone else None

    @classmethod
    def get_or_create(cls, session: Session, sender_phone_number: str) -> Contact:
        contact = cls.get_by_phone_number(session, sender_phone_number)
        if contact:
            return contact

        contact = Contact(
            first_name="Unknown",
            note=f"Auto-created with new sender number {sender_phone_number!r}.",
        )
        session.add(contact)
        session.flush()

        PhoneNumberQueryService.create(session, sender_phone_number, contact)
        session.commit()
        return contact

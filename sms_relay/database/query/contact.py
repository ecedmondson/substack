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
    def all(cls, session: Session) -> list[Contact]:
        return session.execute(select(Contact)).scalars().all()

    @classmethod
    def by_pkid(cls, session: Session, pkid: UUID) -> Optional[Contact]:
        return session.get(Contact, pkid)

    @classmethod
    def update(
        cls, session: Session, pkid: UUID, updated_fields: dict
    ) -> Optional[Contact]:
        contact = cls.by_pkid(session, pkid)
        if not contact:
            return None

        for field, value in updated_fields.items():
            setattr(contact, field, value)

        session.commit()
        session.refresh(contact)
        return contact

    @classmethod
    def create(cls, session: Session, contact_data: dict) -> Contact:
        contact = Contact(**contact_data)
        session.add(contact)
        session.commit()
        session.refresh(contact)
        return contact

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

from typing import Optional
from uuid import UUID

from database.models.forwarding.contact import Contact, PhoneNumber
from database.query.contact_rule_config import ContactRuleConfigQueryService
from sqlalchemy import select
from sqlalchemy.orm import Session


def update_phone_numbers(session, contact, phone_numbers_data):
    existing_numbers_map = {pn.number: pn for pn in contact.phone_numbers}

    updated_phone_numbers = []

    for pn_data in phone_numbers_data:
        number = pn_data.get('number')
        if number in existing_numbers_map:
            # Update existing phone number object (if you have more fields)
            phone_number_obj = existing_numbers_map[number]
            # For example, update other fields here if needed
        else:
            # Create new phone number with contact_id
            phone_number_obj = PhoneNumber(
                number=number,
                contact_id=contact.id,
            )
            session.add(phone_number_obj)

        updated_phone_numbers.append(phone_number_obj)

    # Remove phone numbers not in the new list
    for pn in contact.phone_numbers:
        if pn.number not in [p['number'] for p in phone_numbers_data]:
            session.delete(pn)

    # Replace contact.phone_numbers list to reflect current state
    contact.phone_numbers = updated_phone_numbers



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
    def update(cls, session: Session, contact_id: str, update_data: dict) -> Optional[Contact]:
        contact = session.get(Contact, contact_id)
        if not contact:
            return None

        # Update simple contact fields (first_name, last_name, note)
        simple_fields = ['first_name', 'last_name', 'note']
        for field in simple_fields:
            if field in update_data:
                setattr(contact, field, update_data[field])

        # Handle phone_numbers update
        if 'phone_numbers' in update_data:
            incoming_phone_numbers = update_data['phone_numbers']
            existing_numbers_map = {pn.number: pn for pn in contact.phone_numbers}

            updated_phone_numbers = []

            for pn_data in incoming_phone_numbers:
                number = pn_data.get('number')
                if not number:
                    continue  # skip invalid entry

                if number in existing_numbers_map:
                    # Optionally update existing phone number fields here
                    phone_number_obj = existing_numbers_map[number]
                else:
                    # Create new phone number with contact_id
                    phone_number_obj = PhoneNumber(
                        number=number,
                        contact_id=contact.id,
                    )
                    session.add(phone_number_obj)

                updated_phone_numbers.append(phone_number_obj)

            # Remove phone numbers not present in incoming data
            for pn in list(contact.phone_numbers):
                if pn.number not in [p['number'] for p in incoming_phone_numbers]:
                    session.delete(pn)

            # Replace the phone_numbers relationship list with updated list
            contact.phone_numbers = updated_phone_numbers

        # DEBUG LOG: print all phone numbers before commit
        for p in contact.phone_numbers:
            print(f"PhoneNumber id={p.id} number={p.number} contact_id={p.contact_id}")

        session.commit()
        session.refresh(contact)
        return contact


    @classmethod
    def create(cls, session: Session, contact_data: dict) -> Contact:
        contact = Contact(**contact_data)
        session.add(contact)
        ContactRuleConfigQueryService.add_to_session(session, contact)
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

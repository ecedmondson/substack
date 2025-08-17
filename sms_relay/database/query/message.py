from uuid import UUID

from database.models.forwarding.contact import Contact
from database.models.forwarding.message import ForwardedMessage
from database.query.contact import ContactQueryService
from sqlalchemy import select
from sqlalchemy.orm import Session


class ForwardedMessageQueryService:
    @classmethod
    def all(cls, session: Session, select_only=None):
        select_only = select_only or []

        msg_fields = []
        contact_fields = []

        for field in select_only:
            if field.startswith("contact."):
                contact_fields.append(field.split(".", 1)[1])
            else:
                msg_fields.append(field)

        if not msg_fields and not contact_fields:
            stmt = select(ForwardedMessage).join(Contact, ForwardedMessage.contact)
            result = session.execute(stmt).scalars().all()
            return result

        columns = []
        for f in msg_fields:
            columns.append(getattr(ForwardedMessage, f))
        for f in contact_fields:
            columns.append(getattr(Contact, f))

        stmt = select(*columns).join(Contact, ForwardedMessage.contact)
        result = session.execute(stmt).all()
        return result

    @classmethod
    def by_pkid(cls, session: Session, pkid: UUID):
        return session.execute(
            select(ForwardedMessage).where(ForwardedMessage.id == pkid)
        ).scalar_one_or_none()

    @classmethod
    def create_forwarded_message(cls, session: Session, incoming_message) -> ForwardedMessage:
        contact = ContactQueryService.get_or_create(session, incoming_message.sender)

        message = ForwardedMessage(
            message=incoming_message.message,
            date=incoming_message.date,
            contact=contact,
        )
        session.add(message)
        session.commit()
        session.refresh(message)
        return message


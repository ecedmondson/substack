from datetime import datetime
from uuid import UUID
from zoneinfo import ZoneInfo

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
            relayed=incoming_message.relayed,
            integration_id=incoming_message.integration,
            integration_contact_id=incoming_message.integration_contact_id,
            device=incoming_message.device,
        )
        session.add(message)
        session.commit()
        session.refresh(message)
        return message
    
    @classmethod
    def create_integration_message(cls, session: Session, outgoing_message) -> ForwardedMessage:
        message = ForwardedMessage(
            message=outgoing_message.message,
            date=outgoing_message.date,
            integration_contact_id=outgoing_message.integration_contact_id,
            thread_id=outgoing_message.thread_id,
        )
        session.add(message)
        session.commit()
        session.refresh(message)
        return message
    
    @classmethod
    def mark_message_as_sent_to_integration(cls, session: Session, message_id) -> ForwardedMessage:
        message = session.get(ForwardedMessage, message_id)
        if not message:
            raise ValueError(f"ForwardedMessage {message_id} not found")

        message.delivery_confirmed = datetime.now(tz=ZoneInfo('UTC'))
        session.add(message)
        session.commit()
        session.refresh(message)

        return message
    
    @classmethod
    def message_thread(cls, session: Session, thread_id: UUID, offset: int = 0, page_size: int = 5) -> list[ForwardedMessage]:
        stmt = (
            select(ForwardedMessage)
            .where(ForwardedMessage.thread_id == thread_id)
            .order_by(ForwardedMessage.date)
            .offset(offset)
            .limit(page_size)
        )
        return session.execute(stmt).scalars().all()

    @classmethod
    def assign_thread(
        cls, session: Session, message_id: int, thread_id: int
    ) -> ForwardedMessage:
        message = session.get(ForwardedMessage, message_id)
        if not message:
            raise ValueError(f"ForwardedMessage {message_id} not found")

        message.thread_id = thread_id
        session.add(message)
        session.commit()
        session.refresh(message)

        return message


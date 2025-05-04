from database.models.forwarding.message import ForwardedMessage, MessageRequest
from database.query.contact import ContactQueryService

from sqlalchemy.orm import Session
from sqlalchemy import select
from uuid import UUID

class ForwardedMessageQueryService:
    @classmethod
    def create_forwarded_message(cls, session: Session, incoming_message: MessageRequest) -> ForwardedMessage:
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

    @classmethod
    def by_pkid(cls, session: Session, pkid: UUID):
        return session.execute(select(ForwardedMessage(ForwardedMessage.id == pkid))).one_or_none()


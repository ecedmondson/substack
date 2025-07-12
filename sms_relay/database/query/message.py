from uuid import UUID

from database.models.forwarding.message import ForwardedMessage, MessageRequest
from database.query.contact import ContactQueryService
from sqlalchemy import select
from sqlalchemy.orm import Session


class ForwardedMessageQueryService:
    @classmethod
    def all(cls, session: Session):
        result = session.execute(select(ForwardedMessage))
        return result.scalars().all()

    @classmethod
    def by_pkid(cls, session: Session, pkid: UUID):
        return session.execute(
            select(ForwardedMessage).where(ForwardedMessage.id == pkid)
        ).scalar_one_or_none()

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


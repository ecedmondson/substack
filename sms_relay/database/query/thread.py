from typing import List
from uuid import UUID

from database.models.conversation.thread import ConversationThread
from database.models.forwarding.message import ForwardedMessage
from sqlalchemy import desc, select
from sqlalchemy.orm import Session, aliased, joinedload


class ConversationThreadQueryService:
    @classmethod
    def flush_to_session(cls, session: Session, integration_contact_id: UUID, contact_id: UUID, phone_number_used: str) -> ConversationThread:
        thread = ConversationThread(integration_contact_id=integration_contact_id, contact_id=contact_id, phone_number_used=phone_number_used)
        session.add(thread)
        session.flush()
        return thread

    @classmethod
    def create(cls, session: Session, integration_contact_id: UUID, contact_id: UUID, phone_number_used: str) -> ConversationThread:
        thread = cls.flush_to_session(session, integration_contact_id, contact_id, phone_number_used)
        session.commit()
        session.refresh(thread)
        return thread

    @classmethod
    def all(cls, session: Session) -> List[ConversationThread]:
        return session.execute(select(ConversationThread)).scalars().all()
    
    @classmethod
    def summaries(cls, session: Session, page: int = 0, page_size: int = 50) -> list[ConversationThread]:
        """
        Returns paginated conversation threads with:
        - nested contact and integration_contact objects
        - most recent message
        """
        offset = page * page_size

        latest_msg_alias = aliased(ForwardedMessage)

        # Subquery: get the latest message per thread
        latest_msg_subq = (
            select(
                latest_msg_alias.thread_id,
                latest_msg_alias.id.label("latest_msg_id")
            )
            .order_by(latest_msg_alias.thread_id, desc(latest_msg_alias.date))
            .distinct(latest_msg_alias.thread_id)
            .subquery()
        )

        # Main query: join thread with its latest message + contact + integration contact
        stmt = (
            select(ConversationThread, ForwardedMessage)
            .join(
                latest_msg_subq,
                ConversationThread.id == latest_msg_subq.c.thread_id,
                isouter=True
            )
            .join(
                ForwardedMessage,
                ForwardedMessage.id == latest_msg_subq.c.latest_msg_id,
                isouter=True
            )
            .options(
                joinedload(ConversationThread.contact),
                joinedload(ConversationThread.integration_contact)
            )
            .order_by(desc(ForwardedMessage.date))
            .offset(offset)
            .limit(page_size)
        )

        rows = session.execute(stmt).all()

        # Each row is (ConversationThread, ForwardedMessage | None)
        result = []
        for thread, latest_msg in rows:
            thread.most_recent_message = latest_msg
            result.append(thread)

        return result


from database.models.relay.rule import ContactRule
from sqlalchemy import select
from sqlalchemy.orm import Session


class ContactRuleQueryService:
    @classmethod
    def all(cls, session: Session) -> list[ContactRule]:
        return session.execute(select(ContactRule)).scalars().all()
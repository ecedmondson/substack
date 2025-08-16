from uuid import uuid4

from database.models.relay.rule import ContactRule, ContactRuleCategories
from sqlalchemy.orm import Session


def create_contact_rules(session: Session):
    existing_categories = {
        rule.category for rule in session.query(ContactRule.category).all()
    }

    for category in ContactRuleCategories.values():
        if category not in existing_categories:
            session.add(
                ContactRule(
                    id=uuid4(),
                    category=category
                )
            )


def delete_contact_rules(session: Session):
    rules = session.query(ContactRule).filter(
        ContactRule.category.in_(ContactRuleCategories.values())
    ).all()

    for rule in rules:
        session.delete(rule)

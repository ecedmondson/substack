from uuid import UUID

from database.models.forwarding.contact import Contact
from database.models.relay.rule import (ContactRule, ContactRuleConfig,
                                        ContactRuleConfigRule)
from sqlalchemy.orm import Session


class ContactRuleConfigQueryService:
    @classmethod
    def add_to_session(cls, session: Session, contact) -> ContactRuleConfig:
        config = ContactRuleConfig(
            contact_id=contact.id
        )
        session.add(
            ContactRuleConfig(
                contact_id=contact.id
            )
        )
        return config

    @classmethod
    def create(cls, session: Session, contact: Contact, commit=True) -> ContactRuleConfig:
        cls.add_to_session(session, contact)
        session.commit()

    @classmethod
    def add_rule_to_config(
        cls,
        session: Session,
        config_id: UUID,
        rule_id: UUID
    ) -> ContactRuleConfig:
        """
        Adds a ContactRule to an existing ContactRuleConfig.
        Returns the updated ContactRuleConfig.
        """
        config = session.get(ContactRuleConfig, config_id)
        if not config:
            raise ValueError(f"ContactRuleConfig {config_id} not found")

        rule = session.get(ContactRule, rule_id)
        if not rule:
            raise ValueError(f"ContactRule {rule_id} not found")

        existing_rule_ids = {link.rule_id for link in config.rule_links}
        if rule_id not in existing_rule_ids:
            config.rule_links.append(ContactRuleConfigRule(rule=rule))

        session.commit()
        session.refresh(config)
        return config

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
        If the rule already exists but is disabled, re-enable it.
        Returns the updated ContactRuleConfig.
        """
        contact_config = session.get(ContactRuleConfig, config_id)
        if not contact_config:
            raise ValueError(f"ContactRuleConfig {config_id} not found")

        rule = session.get(ContactRule, rule_id)
        if not rule:
            raise ValueError(f"ContactRule {rule_id} not found")

        # Look for an existing link (enabled or disabled)
        existing_link = next((link for link in contact_config.rule_links if link.rule_id == rule_id), None)

        if existing_link:
            if not existing_link.enabled:
                existing_link.enabled = True  # Re-enable instead of creating new
        else:
            contact_config.rule_links.append(ContactRuleConfigRule(rule=rule, enabled=True))

        session.commit()
        session.refresh(contact_config)
        return contact_config

    @classmethod
    def disable_rule_in_config(
        cls,
        session: Session,
        config_id: UUID,
        rule_id: UUID
    ) -> ContactRuleConfig:
        """
        Disables a ContactRule in an existing ContactRuleConfig.
        Returns the updated ContactRuleConfig.
        """
        config = session.get(ContactRuleConfig, config_id)
        if not config:
            raise ValueError(f"ContactRuleConfig {config_id} not found")

        existing_link = next((link for link in config.rule_links if link.rule_id == rule_id), None)
        if not existing_link:
            raise ValueError(f"Rule {rule_id} not linked to ContactRuleConfig {config_id}")

        existing_link.enabled = False

        session.commit()
        session.refresh(config)
        return config
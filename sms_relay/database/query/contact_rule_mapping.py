
from database.models.relay.contact_relay import ContactRuleConfigRule
from sqlalchemy.orm import Session


class ContactRuleConfigRuleQueryService:
    @classmethod
    def create(cls, session: Session, contact_id: int, rule_id: int):
        config_mapping = ContactRuleConfigRule(
            contact_id=contact_id,
            rule_id=rule_id,
        )
        session.add(
            config_mapping
        )
        session.commit(config_mapping)
        session.refresh(config_mapping)
        return config_mapping
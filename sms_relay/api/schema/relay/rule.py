from typing import Optional
from uuid import UUID

from api.schema.mixins.primary_key import UUIDPrimaryKeyPydanticMixin
from api.schema.pydantic_base import PydanticBase


class RuleShape(UUIDPrimaryKeyPydanticMixin):
    category: str

class ContactRuleConfigRuleShape(PydanticBase):
    enabled: bool
    rule_id: UUID
    config_id: UUID

class ContactRuleConfigShape(UUIDPrimaryKeyPydanticMixin):
    rule_links: Optional[list[ContactRuleConfigRuleShape]] = None

class CreateRulePayload(PydanticBase):
    rule_id: UUID
    config_id: UUID

class DisableRulePayload(PydanticBase):
    config_id: UUID
    rule_id: UUID
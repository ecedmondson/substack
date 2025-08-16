from typing import Optional
from uuid import UUID

from api.schema.mixins.primary_key import UUIDPrimaryKeyPydanticMixin
from api.schema.pydantic_base import PydanticBase


class RuleShape(UUIDPrimaryKeyPydanticMixin):
    category: str

class ContactRuleConfigShape(UUIDPrimaryKeyPydanticMixin):
    id: UUID
    rule_links: Optional[list[RuleShape]] = None

class CreateRulePayload(PydanticBase):
    rule_id: UUID
    config_id: UUID
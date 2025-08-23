from enum import Enum
from typing import List

from database.models.base import DeclarativeBase
from database.models.mixins.primary_key import UUIDPrimaryKey
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship


class RuleType(Enum):
    CONTACT = "CONTACT"
    EXTERNAL = "EXTERNAL"
    SYSTEM = "SYSTEM"

class ContactRuleCategories(Enum):
    DISABLED = "DISABLED"
    DISPLAY_BUSINESS_HOURS_ONLY = "BUSINESS_HOURS_ONLY"
    DISPLAY = "DISPLAY"
    CLEANUP = "CLEANUP"

    @staticmethod
    def values():
        return [cat.value for cat in ContactRuleCategories]


class ContactRule(DeclarativeBase, UUIDPrimaryKey):
    __tablename__ = "contact_rule_type"

    category: Mapped[ContactRuleCategories] = mapped_column(
        SQLEnum(ContactRuleCategories, name="contact_rule_categories"),
        nullable=False,
    )

    rule_type: Mapped[RuleType] = mapped_column(
        SQLEnum(RuleType, name="rule_type_enum"),
        nullable=False,
        default=RuleType.CONTACT,
        server_default="CONTACT",
    )

    config_links: Mapped[List['ContactRuleConfigRule']] = relationship( # noqa: F821
        back_populates="rule",
        lazy="selectin",
        cascade="all, delete-orphan",
    )

#class SystemRule(DeclarativeBase, UUIDPrimaryKey):
#    __tablename__ = "system_rule_type"
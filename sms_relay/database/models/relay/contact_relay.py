from typing import List
from uuid import UUID

from database.models.base import DeclarativeBase
from database.models.forwarding.contact import Contact
from database.models.mixins.primary_key import UUIDPrimaryKey
from sqlalchemy import UUID as SQLUUID
from sqlalchemy import Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


class ContactRuleConfigRule(DeclarativeBase):
    __tablename__ = "contact_rule_config_rules"

    config_id: Mapped[UUID] = mapped_column(
        ForeignKey("contact_rule_config.id"), primary_key=True
    )
    rule_id: Mapped[UUID] = mapped_column(
        ForeignKey("contact_rule_type.id"), primary_key=True
    )

    enabled: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True
    )

    config: Mapped["ContactRuleConfig"] = relationship(back_populates="rule_links")
    rule: Mapped["ContactRule"] = relationship(back_populates="config_links") # noqa: F821


class ContactRuleConfig(DeclarativeBase, UUIDPrimaryKey):
    __tablename__ = "contact_rule_config"

    contact_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True), ForeignKey("contact.id"), nullable=False
    )
    contact: Mapped["Contact"] = relationship(back_populates="rules")

    rule_links: Mapped[List[ContactRuleConfigRule]] = relationship(
        back_populates="config",
        lazy="selectin",
        cascade="all, delete-orphan",
    )

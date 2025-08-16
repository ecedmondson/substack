"""autopopulate rules

Revision ID: cc4758ac4932
Revises: 4b7102714be2
Create Date: 2025-08-16 01:32:40.416905

"""
import logging
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from database.migrations.utils.contact_rule import (create_contact_rules,
                                                    delete_contact_rules)

logger = logging.getLogger(__name__)

# revision identifiers, used by Alembic.
revision: str = 'cc4758ac4932'
down_revision: Union[str, None] = '4b7102714be2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    bind = op.get_bind()
    session = sa.orm.Session(bind=bind)
    try:
        create_contact_rules(session)
        session.commit()
    except Exception as oops:
        logger.error(f"Received exception {oops!r} trying to create contact rules.")



def downgrade():
    bind = op.get_bind()
    session = sa.orm.Session(bind=bind)
    try:
        delete_contact_rules(session)
        session.commit()
    except Exception as oops:
        logger.error(f"Received exception {oops!r} trying to delete contact rules.")
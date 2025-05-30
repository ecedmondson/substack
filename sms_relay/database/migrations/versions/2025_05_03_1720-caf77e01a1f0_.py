"""empty message

Revision ID: caf77e01a1f0
Revises: 
Create Date: 2025-05-03 17:20:48.711935

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'caf77e01a1f0'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('contact',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('first_name', sa.String(length=255), nullable=True),
    sa.Column('last_name', sa.String(length=255), nullable=True),
    sa.Column('note', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('forwarded_message',
    sa.Column('message', sa.Text(), nullable=False),
    sa.Column('date', sa.String(length=35), nullable=False),
    sa.Column('contact_id', sa.Uuid(), nullable=False),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['contact_id'], ['contact.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_forwarded_message_created'), 'forwarded_message', ['created'], unique=False)
    op.create_index(op.f('ix_forwarded_message_id'), 'forwarded_message', ['id'], unique=False)
    op.create_table('phone_number',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('number', sa.String(length=15), nullable=False),
    sa.Column('contact_id', sa.Uuid(), nullable=False),
    sa.ForeignKeyConstraint(['contact_id'], ['contact.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('phone_number')
    op.drop_index(op.f('ix_forwarded_message_id'), table_name='forwarded_message')
    op.drop_index(op.f('ix_forwarded_message_created'), table_name='forwarded_message')
    op.drop_table('forwarded_message')
    op.drop_table('contact')
    # ### end Alembic commands ###

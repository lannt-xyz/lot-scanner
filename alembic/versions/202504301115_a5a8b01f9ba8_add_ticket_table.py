"""add ticket table

Revision ID: a5a8b01f9ba8
Revises: 523a361fbebf
Create Date: 2025-04-30 11:15:01.541281

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a5a8b01f9ba8'
down_revision: Union[str, None] = '523a361fbebf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('ticket',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('channel', sa.String(length=10), nullable=True),
    sa.Column('prize_date', sa.DateTime(), nullable=True),
    sa.Column('prize_number', sa.String(length=6), nullable=True),
    sa.Column('result', sa.String(length=2), nullable=True),
    sa.Column('prize_amount', sa.Integer(), nullable=True),
    sa.Column('is_deleted', sa.Boolean(), nullable=True),
    sa.Column('created_by', sa.String(length=255), nullable=True),
    sa.Column('updated_by', sa.String(length=255), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('ticket')

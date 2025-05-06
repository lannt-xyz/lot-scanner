"""add table related scan history

Revision ID: 36c7587e60a3
Revises: a5a8b01f9ba8
Create Date: 2025-05-06 16:34:48.307988

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '36c7587e60a3'
down_revision: Union[str, None] = 'a5a8b01f9ba8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('device_information',
    sa.Column('device_id', sa.String(length=255), nullable=False),
    sa.Column('fingerprint', sa.String(length=255), nullable=False),
    sa.Column('is_deleted', sa.Boolean(), nullable=False),
    sa.Column('created_by', sa.String(length=20), nullable=False),
    sa.Column('updated_by', sa.String(length=20), nullable=False),
    sa.Column('created_at', sa.DateTime, nullable=False),
    sa.Column('updated_at', sa.DateTime, nullable=False),
    sa.PrimaryKeyConstraint('device_id')
    )
    op.create_table('scan_history',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('file_path', sa.String(length=255), nullable=False),
    sa.Column('ocr_text', sa.String(length=255), nullable=False),
    sa.Column('corrected_text', sa.String(length=255), nullable=False),
    sa.Column('device_id', sa.String(length=255), nullable=False),
    sa.Column('is_deleted', sa.Boolean(), nullable=False),
    sa.Column('created_by', sa.String(length=20), nullable=False),
    sa.Column('updated_by', sa.String(length=20), nullable=False),
    sa.Column('created_at', sa.DateTime, nullable=False),
    sa.Column('updated_at', sa.DateTime, nullable=False),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('scan_history')
    op.drop_table('device_information')

"""add code_master

Revision ID: 523a361fbebf
Revises: 4ebb368674e2
Create Date: 2025-04-29 23:38:57.835338

"""
import csv
from datetime import datetime, UTC
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '523a361fbebf'
down_revision: Union[str, None] = '4ebb368674e2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    code_master_table = op.create_table('code_master',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('group_code', sa.String(10), nullable=True),
        sa.Column('group_name', sa.String(255), nullable=True),
        sa.Column('code_value', sa.String(10), nullable=True),
        sa.Column('code_name1', sa.String(255), nullable=True),
        sa.Column('code_name2', sa.String(255), nullable=True),
        sa.Column('display_order', sa.Integer(), nullable=True),
        sa.Column('is_deleted', sa.Boolean(), nullable=True),
        sa.Column('created_by', sa.String(255), nullable=True),
        sa.Column('updated_by', sa.String(255), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    # Load data from CSV file and insert for the Global_punc dictionary
    created_date = datetime.now(UTC)
    rows = [
        {
            'group_code': '100001',
            'group_name': 'Group Channels',
            'code_value': 'MB',
            'code_name1': 'Xổ Số Miền Bắc',
            'display_order': 0,
            'is_deleted': False,
            'created_by': revision,
            'updated_by': revision,
            'created_at': created_date,
            'updated_at': created_date,
        },
        {
            'group_code': '100001',
            'group_name': 'Group Channels',
            'code_value': 'MT',
            'code_name1': 'Xổ Số Miền Trung',
            'display_order': 1,
            'is_deleted': False,
            'created_by': revision,
            'updated_by': revision,
            'created_at': created_date,
            'updated_at': created_date,
        },
        {
            'group_code': '100001',
            'group_name': 'Group Channels',
            'code_value': 'MN',
            'code_name1': 'Xổ Số Miền Nam',
            'display_order': 2,
            'is_deleted': False,
            'created_by': revision,
            'updated_by': revision,
            'created_at': created_date,
            'updated_at': created_date,
        }
    ]
    with open('alembic/csv/20250429233857_523a361fbebf_code_master.csv', 'r', encoding='utf-8-sig', newline='\r\n') as file:
        reader = csv.DictReader(file)
        index = 0
        for row in reader:
            rows.append({
                'group_code': '100002',
                'group_name': 'Channels',
                'code_value': row['ma_dai'],
                'code_name1': row['ten_dai'],
                'display_order': index,
                'is_deleted': False,
                'created_by': revision,
                'updated_by': revision,
                'created_at': created_date,
                'updated_at': created_date,
            })
            index += 1
    op.bulk_insert(code_master_table, rows)


def downgrade() -> None:
    op.drop_table('code_master')


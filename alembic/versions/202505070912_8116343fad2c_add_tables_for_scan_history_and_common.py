"""add tables for scan history and common

Revision ID: 8116343fad2c
Revises: 4ebb368674e2
Create Date: 2025-05-07 09:12:10.521965

"""
import csv
from datetime import UTC, datetime
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8116343fad2c'
down_revision: Union[str, None] = '4ebb368674e2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    code_master_table = op.create_table('code_master',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('group_code', sa.String(length=10), nullable=True),
    sa.Column('group_name', sa.String(length=255), nullable=True),
    sa.Column('code_value', sa.String(length=10), nullable=True),
    sa.Column('code_name1', sa.String(length=255), nullable=True),
    sa.Column('code_name2', sa.String(length=255), nullable=True),
    sa.Column('display_order', sa.Integer(), nullable=True),
    sa.Column('is_deleted', sa.Boolean(), nullable=False),
    sa.Column('created_by', sa.String(length=255), nullable=False),
    sa.Column('updated_by', sa.String(length=255), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('device_information',
    sa.Column('device_id', sa.String(length=255), nullable=False),
    sa.Column('fingerprint', sa.String(length=255), nullable=False),
    sa.Column('is_deleted', sa.Boolean(), nullable=False),
    sa.Column('created_by', sa.String(length=255), nullable=False),
    sa.Column('updated_by', sa.String(length=255), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('device_id')
    )
    op.create_table('scan_history',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('file_path', sa.String(length=255), nullable=False),
    sa.Column('ocr_text', sa.Text(), nullable=False),
    sa.Column('corrected_text', sa.Text(), nullable=False),
    sa.Column('device_id', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_device_id', 'scan_history', ['device_id'], unique=False)
    op.create_table('ticket',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('channel', sa.String(length=10), nullable=True),
    sa.Column('prize_date', sa.DateTime(), nullable=True),
    sa.Column('prize_number', sa.String(length=6), nullable=True),
    sa.Column('result', sa.String(length=2), nullable=True),
    sa.Column('prize_amount', sa.Integer(), nullable=True),
    sa.Column('is_deleted', sa.Boolean(), nullable=False),
    sa.Column('created_by', sa.String(length=255), nullable=False),
    sa.Column('updated_by', sa.String(length=255), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
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
            'code_name2': 'mien-bac',
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
            'code_name2': 'mien-trung',
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
            'code_name2': 'mien-nam',
            'display_order': 2,
            'is_deleted': False,
            'created_by': revision,
            'updated_by': revision,
            'created_at': created_date,
            'updated_at': created_date,
        }
    ]
    with open('alembic/csv/202505070912_8116343fad2c_code_master.csv', 'r', encoding='utf-8-sig', newline='\r\n') as file:
        reader = csv.DictReader(file)
        index = 0
        for row in reader:
            rows.append({
                'group_code': '100002',
                'group_name': 'Channels',
                'code_value': row['ma_dai'],
                'code_name1': row['ten_dai'],
                'code_name2': row['ten_dai2'],
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
    op.drop_table('ticket')
    op.drop_index('idx_device_id', table_name='scan_history')
    op.drop_table('scan_history')
    op.drop_table('device_information')
    op.drop_table('code_master')

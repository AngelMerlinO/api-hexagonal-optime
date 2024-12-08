"""create_table_schedules

Revision ID: 58dc05c3eb9a
Revises: 
Create Date: 2024-11-21 23:58:37.470493

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
import uuid

# revision identifiers, used by Alembic.
revision: str = '58dc05c3eb9a'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def generate_uuid() -> str:
    return str(uuid.uuid4())

def upgrade() -> None:
    op.create_table('schedules',
                    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False, primary_key=True),
                    sa.Column('uuid', sa.String(36), nullable=False, unique=True, default=generate_uuid),
                    sa.Column('user_id', sa.Integer(), nullable=False, unique=True),
                    sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.current_timestamp()),
                    sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.func.current_timestamp(), onupdate=sa.func.current_timestamp()),
                    sa.Column('deleted_at', sa.DateTime(), nullable=True)
                    )
    schedules_table = sa.table('schedules',
                               sa.column('id', sa.Integer()),
                               sa.column('uuid', sa.Integer()),
                               sa.column('user_id', sa.Integer()),
                               sa.column('created_at', sa.DateTime()),
                               sa.column('updated_at', sa.DateTime()),
                               sa.column('deleted_at', sa.DateTime()),
                               )

    seed_schedules = [
        {
            'id': 1,
            'uuid': str(uuid.uuid4()),
            'user_id': 1,
            'created_at': '2024-11-22 01:06:10.949281',
            'updated_at': '2024-11-22 01:06:10.949281',
            'deleted_at': None,
        },
        {
            'id': 2,
            'uuid': str(uuid.uuid4()),
            'user_id': 2,
            'created_at': '2024-11-22 01:06:10.949281',
            'updated_at': '2024-11-22 01:06:10.949281',
            'deleted_at': None,
        },
        {
            'id': 3,
            'uuid': str(uuid.uuid4()),
            'user_id': 3,
            'created_at': '2024-11-22 01:06:10.949281',
            'updated_at': '2024-11-22 01:06:10.949281',
            'deleted_at': None,
        },
    ]
    
    op.bulk_insert(schedules_table, seed_schedules)

def downgrade() -> None:
    op.drop_table('schedules')
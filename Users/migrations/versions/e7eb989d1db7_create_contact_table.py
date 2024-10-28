"""create_contact_table

Revision ID: e7eb989d1db7
Revises: d4661526e5ea
Create Date: 2024-10-16 22:16:39.235341

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

revision: str = 'e7eb989d1db7'
down_revision: Union[str, None] = 'd4661526e5ea'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'contacts',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('email', sa.String(length=100), nullable=False),
        sa.Column('phone', sa.String(length=20), nullable=False, unique=True),
        sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('deleted_at', sa.TIMESTAMP(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    
    contacts_table = sa.table(
        'contacts',
        sa.column('id', sa.Integer),
        sa.column('email', sa.String(length=100)),
        sa.column('phone', sa.String(length=20)),
        sa.column('created_at', sa.TIMESTAMP),
        sa.column('updated_at', sa.TIMESTAMP),
        sa.column('deleted_at', sa.TIMESTAMP)
    )
    
    seed_contact = [
        {
            'email': 'john.doe@example.com',
            'phone': '529515271070',
        },
        {
            'email': 'jane.smith@example.com',
            'phone': '529515271071',
        },
        {
            'email': 'alice.jones@example.com',
            'phone': '529515271072',
        },
    ]
    
    op.bulk_insert(contacts_table, seed_contact)
    

def downgrade() -> None:
    op.execute(
        "DELETE FROM contacts WHERE email IN ('john.doe@example.com', 'jane.smith@example.com', 'alice.jones@example.com')"
    )
    
    op.drop_table('contacts')
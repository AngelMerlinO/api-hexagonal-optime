"""add_foreignkey_users_from_contacts

Revision ID: 90d93c0136b2
Revises: e7eb989d1db7
Create Date: 2024-10-17 11:49:28.663602

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '90d93c0136b2'
down_revision: Union[str, None] = 'e7eb989d1db7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('contact_id', sa.Integer(), nullable=True))
    
    op.create_foreign_key(
        'fk_users_contact_id',  
        'users',  
        'contacts',  
        ['contact_id'],  
        ['id']  
    )


def downgrade() -> None:
    
    op.drop_constraint('fk_users_contact_id', 'users', type_='foreignkey')
    
    op.drop_column('users', 'contact_id')

"""Create payment table

Revision ID: 207e717702ba
Revises: b7d4004a8164
Create Date: 2024-10-02 22:47:58.219837

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '207e717702ba'
down_revision: Union[str, None] = 'b7d4004a8164'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    op.create_table('payments',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('preference_id', sa.String(255), nullable=False),
        sa.Column('payment_id', sa.String(255), nullable=True),
        sa.Column('status', sa.String(50), nullable=True),
        sa.Column('status_detail', sa.String(255), nullable=True),
        sa.Column('amount', sa.Numeric(10, 2), nullable=False),
        sa.Column('currency_id', sa.String(10), nullable=False),
        sa.Column('description', sa.String(255), nullable=True),
        sa.Column('date_created', sa.TIMESTAMP(), nullable=True),  # Agregado
        sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade():
    op.drop_table('payments')

"""Created table Messanging

Revision ID: d4661526e5ea
Revises: 207e717702ba
Create Date: 2024-10-02 22:49:28.697312

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = 'd4661526e5ea'
down_revision: Union[str, None] = '207e717702ba'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table('messages',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True, nullable=False),
        sa.Column('recipient_phone_number', sa.String(length=20), nullable=False),
        sa.Column('message_type', sa.String(length=50), nullable=False),
        sa.Column('message_content', sa.Text(), nullable=False),
        sa.Column('status', sa.String(length=50), nullable=True),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('date_created', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False, onupdate='CURRENT_TIMESTAMP')
    )

def downgrade():
    op.drop_table('messages')
    
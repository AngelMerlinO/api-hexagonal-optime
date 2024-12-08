"""add_verifyAt_from_users

Revision ID: 25c34d81337d
Revises: ff7d75f064ef
Create Date: 2024-10-21 18:17:01.956462

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

revision: str = '25c34d81337d'
down_revision: Union[str, None] = 'ff7d75f064ef'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column("verify_at", sa.DateTime(), nullable=True))


def downgrade() -> None:
    op.drop_column("users", "verify_at")
   
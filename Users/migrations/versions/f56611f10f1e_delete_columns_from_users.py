"""delete_columns_from_users

Revision ID: f56611f10f1e
Revises: 25c34d81337d
Create Date: 2024-11-05 21:15:43.941692

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'f56611f10f1e'
down_revision: Union[str, None] = '25c34d81337d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table("users") as batch_op:
        batch_op.drop_column("email")


def downgrade() -> None:
    with op.batch_alter_table("users") as batch_op:
        batch_op.add_column(sa.Column("email", sa.String(length=255), nullable=True))
  

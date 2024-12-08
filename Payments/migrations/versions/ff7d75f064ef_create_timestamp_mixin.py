"""create-timestamp-mixin

Revision ID: ff7d75f064ef
Revises: 90d93c0136b2
Create Date: 2024-10-19 11:58:35.460958

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

revision: str = 'ff7d75f064ef'
down_revision: Union[str, None] = '207e717702ba'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:


    op.add_column('payments', sa.Column('deleted_at', sa.TIMESTAMP(), nullable=True))


def downgrade() -> None:

    op.drop_column('payments', 'deleted_at')
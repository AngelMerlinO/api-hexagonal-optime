"""add_columns_from_contact

Revision ID: edf75a12e486
Revises: f56611f10f1e
Create Date: 2024-11-05 21:29:16.056760

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'edf75a12e486'
down_revision: Union[str, None] = 'f56611f10f1e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("contacts", sa.Column("name", sa.String(length=255), nullable=True))
    op.add_column("contacts", sa.Column("last_name", sa.String(length=255), nullable=True))

    


def downgrade() -> None:
    op.drop_column("contacts", "name")
    op.drop_column("contacts", "last_name")
    

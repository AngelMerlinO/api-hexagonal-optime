"""Create schedules and schedule_items tables

Revision ID: d34f511c9a9d
Revises: d0e032aa4973
Create Date: 2024-10-01 23:42:19.707732

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.mysql import JSON


# revision identifiers, used by Alembic.
revision: str = 'd34f511c9a9d'
down_revision: Union[str, None] = 'd0e032aa4973'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Crear tabla 'schedules'
    op.create_table(
        'schedules',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id'), nullable=False)
    )

    # Crear tabla 'schedule_items'
    op.create_table(
        'schedule_items',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('schedule_id', sa.Integer, sa.ForeignKey('schedules.id', ondelete='CASCADE'), nullable=False),
        sa.Column('nombre', sa.String(255), nullable=False),
        sa.Column('grupo', sa.String(50), nullable=True),
        sa.Column('cuatrimestre', sa.Integer, nullable=True),
        sa.Column('calif_cuatrimestre', sa.Integer, nullable=True),
        sa.Column('calif_holgura', sa.Integer, nullable=True),
        sa.Column('calif_seriacion', sa.Integer, nullable=True),
        sa.Column('lunes', JSON, nullable=True),
        sa.Column('martes', JSON, nullable=True),
        sa.Column('miercoles', JSON, nullable=True),
        sa.Column('jueves', JSON, nullable=True),
        sa.Column('viernes', JSON, nullable=True)
    )

def downgrade():
    op.drop_table('schedule_items')
    op.drop_table('schedules')
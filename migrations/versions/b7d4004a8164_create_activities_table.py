"""create_activities_table

Revision ID: b7d4004a8164
Revises: b2bf860f9524
Create Date: 2024-10-02 17:58:22.431051

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = 'b7d4004a8164'
down_revision: Union[str, None] = 'b2bf860f9524'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('activities',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=255), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('type', sa.Enum('exam', 'assignment', 'project', 'quiz', name='activitytype'), nullable=False),
    sa.Column('status', sa.Enum('sent', 'pending', 'completed', 'overdue', name='activitystatus'), nullable=False),
    sa.Column('delivery_date', sa.Date(), nullable=False),
    sa.Column('link_classroom', sa.String(length=512), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_constraint('schedule_items_ibfk_1', 'schedule_items', type_='foreignkey')
    op.create_foreign_key(None, 'schedule_items', 'schedules', ['schedule_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'schedule_items', type_='foreignkey')
    op.create_foreign_key('schedule_items_ibfk_1', 'schedule_items', 'schedules', ['schedule_id'], ['id'], ondelete='CASCADE')
    op.drop_table('activities')
    # ### end Alembic commands ###

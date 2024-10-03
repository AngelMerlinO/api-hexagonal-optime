"""create_activities_table

Revision ID: b7d4004a8164
Revises: b2bf860f9524
Create Date: 2024-10-02 17:58:22.431051

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

revision: str = 'b7d4004a8164'
down_revision: Union[str, None] = 'b2bf860f9524'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
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

    activities_table = sa.table(
        'activities',
        sa.column('id', sa.Integer),
        sa.column('user_id', sa.Integer),
        sa.column('title', sa.String(length=255)),
        sa.column('description', sa.Text),
        sa.column('type', sa.Enum('exam', 'assignment', 'project', 'quiz', name='activitytype')),
        sa.column('status', sa.Enum('sent', 'pending', 'completed', 'overdue', name='activitystatus')),
        sa.column('delivery_date', sa.Date),
        sa.column('link_classroom', sa.String(length=512)),
        sa.column('created_at', sa.TIMESTAMP),
        sa.column('updated_at', sa.TIMESTAMP),
    )

    seed_activities = [
        {
            'user_id': 1,  
            'title': 'Examen Final de Matemáticas',
            'description': 'Examen final para el curso de Matemáticas II.',
            'type': 'exam',
            'status': 'sent',
            'delivery_date': '2024-12-15',
            'link_classroom': 'https://classroom.example.com/exam-matematicas-final',
        },
        {
            'user_id': 2,  
            'title': 'Proyecto de Física Aplicada',
            'description': 'Desarrollo de un proyecto de Física aplicada sobre movimiento rectilíneo.',
            'type': 'project',
            'status': 'pending',
            'delivery_date': '2024-11-30',
            'link_classroom': 'https://classroom.example.com/proyecto-fisica-aplicada',
        },
        {
            'user_id': 3, 
            'title': 'Quiz de Química Orgánica',
            'description': 'Quiz sobre reacciones de química orgánica.',
            'type': 'quiz',
            'status': 'completed',
            'delivery_date': '2024-10-20',
            'link_classroom': 'https://classroom.example.com/quiz-quimica-organica',
        },
        {
            'user_id': 1,
            'title': 'Asignación de Laboratorio de Biología',
            'description': 'Preparación para el laboratorio de biología sobre genética.',
            'type': 'assignment',
            'status': 'overdue',
            'delivery_date': '2024-10-10',
            'link_classroom': 'https://classroom.example.com/asignacion-biologia-genetica',
        },
    ]

    op.bulk_insert(activities_table, seed_activities)


def downgrade() -> None:
    activities_table = sa.table(
        'activities',
        sa.column('id', sa.Integer),
        sa.column('user_id', sa.Integer),
        sa.column('title', sa.String(length=255)),
        sa.column('description', sa.Text),
        sa.column('type', sa.Enum('exam', 'assignment', 'project', 'quiz', name='activitytype')),
        sa.column('status', sa.Enum('sent', 'pending', 'completed', 'overdue', name='activitystatus')),
        sa.column('delivery_date', sa.Date),
        sa.column('link_classroom', sa.String(length=512)),
        sa.column('created_at', sa.TIMESTAMP),
        sa.column('updated_at', sa.TIMESTAMP),
    )

    op.execute(
        activities_table.delete().where(
            sa.or_(
                activities_table.c.title == 'Examen Final de Matemáticas',
                activities_table.c.title == 'Proyecto de Física Aplicada',
                activities_table.c.title == 'Quiz de Química Orgánica',
                activities_table.c.title == 'Asignación de Laboratorio de Biología',
            )
        )
    )

    op.drop_constraint(None, 'schedule_items', type_='foreignkey')
    op.create_foreign_key('schedule_items_ibfk_1', 'schedule_items', 'schedules', ['schedule_id'], ['id'], ondelete='CASCADE')

    op.drop_table('activities')
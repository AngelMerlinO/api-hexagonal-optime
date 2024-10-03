"""create notifications table

Revision ID: b2bf860f9524
Revises: d34f511c9a9d
Create Date: 2024-10-02 12:41:23.211071

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'b2bf860f9524'
down_revision: Union[str, None] = 'd34f511c9a9d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    
    op.create_table('notifications',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('message', sa.Text(), nullable=False),
        sa.Column('type', sa.Enum('email', 'sms', 'push', 'in-app', name='notificationtype'), nullable=False),
        sa.Column('status', sa.Enum('sent', 'pending', 'failed', name='notificationstatus'), server_default='pending', nullable=False),
        sa.Column('link', sa.String(length=255), nullable=True),
        sa.Column('sent_at', sa.TIMESTAMP(), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    notifications_table = sa.table(
        'notifications',
        sa.column('id', sa.Integer),
        sa.column('user_id', sa.Integer),
        sa.column('title', sa.String(length=255)),
        sa.column('message', sa.Text),
        sa.column('type', sa.Enum('email', 'sms', 'push', 'in-app', name='notificationtype')),
        sa.column('status', sa.Enum('sent', 'pending', 'failed', name='notificationstatus')),
        sa.column('link', sa.String(length=255)),
        sa.column('sent_at', sa.TIMESTAMP),
        sa.column('created_at', sa.TIMESTAMP),
        sa.column('updated_at', sa.TIMESTAMP),
    )

    seed_notifications = [
        {
            'user_id': 1, 
            'title': 'Examen Próximo',
            'message': 'Tienes un examen de Matemáticas el próximo 15 de noviembre.',
            'type': 'email',
            'status': 'sent',
            'link': 'https://classroom.example.com/exam/mathematics',
            'sent_at': '2024-10-03 09:00:00',
        },
        {
            'user_id': 2, 
            'title': 'Proyecto Asignado',
            'message': 'Se te ha asignado un nuevo proyecto de Física.',
            'type': 'push',
            'status': 'pending',
            'link': 'https://classroom.example.com/project/physics',
            'sent_at': None,
        },
        {
            'user_id': 1,
            'title': 'Quiz Disponible',
            'message': 'Un nuevo quiz de Química está disponible.',
            'type': 'sms',
            'status': 'failed',
            'link': None,
            'sent_at': '2024-10-02 14:30:00',
        },
    ]

    op.bulk_insert(notifications_table, seed_notifications)


def downgrade():
    notifications_table = sa.table(
        'notifications',
        sa.column('id', sa.Integer),
        sa.column('user_id', sa.Integer),
        sa.column('title', sa.String(length=255)),
        sa.column('message', sa.Text),
        sa.column('type', sa.Enum('email', 'sms', 'push', 'in-app', name='notificationtype')),
        sa.column('status', sa.Enum('sent', 'pending', 'failed', name='notificationstatus')),
        sa.column('link', sa.String(length=255)),
        sa.column('sent_at', sa.TIMESTAMP),
        sa.column('created_at', sa.TIMESTAMP),
        sa.column('updated_at', sa.TIMESTAMP),
    )

    op.execute(
        notifications_table.delete().where(
            sa.or_(
                sa.and_(
                    notifications_table.c.user_id == 1,
                    notifications_table.c.title == 'Examen Próximo',
                    notifications_table.c.message == 'Tienes un examen de Matemáticas el próximo 15 de noviembre.',
                ),
                sa.and_(
                    notifications_table.c.user_id == 2,
                    notifications_table.c.title == 'Proyecto Asignado',
                    notifications_table.c.message == 'Se te ha asignado un nuevo proyecto de Física.',
                ),
                sa.and_(
                    notifications_table.c.user_id == 1,
                    notifications_table.c.title == 'Quiz Disponible',
                    notifications_table.c.message == 'Un nuevo quiz de Química está disponible.',
                ),
            )
        )
    )
    op.drop_table('notifications')
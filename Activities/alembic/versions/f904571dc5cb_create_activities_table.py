"""create_activities_table

Revision ID: f904571dc5cb
Revises: 
Create Date: 2024-11-16 11:50:05.318315

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import uuid


# revision identifiers, used by Alembic.
revision: str = 'f904571dc5cb'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def generate_uuid():
    """Helper function to generate UUIDs for seed data"""
    return str(uuid.uuid4())

def upgrade() -> None:
    op.create_table(
        "activities",
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False, primary_key=True),
        sa.Column('uuid', sa.String(36), nullable=False, unique=True, default=lambda: str(uuid.uuid4())),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('type', sa.Enum('exam', 'assignment', 'project', 'quiz'), nullable=False),
        sa.Column('status', sa.Enum('sent', 'pending', 'completed', 'overdue'), nullable=False),
        sa.Column('delivery_date', sa.Date(), nullable=False),
        sa.Column('link_classroom', sa.String(512), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.current_timestamp()),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.func.current_timestamp(), onupdate=sa.func.current_timestamp()),
        sa.Column('deleted_at', sa.DateTime(), nullable=True),
    )
    
    activities_table = sa.table(
        'activities',
        sa.column('id', sa.Integer),
        sa.column('uuid', sa.String(36)),
        sa.column('user_id', sa.Integer),
        sa.column('title', sa.String(255)),
        sa.column('description', sa.Text),
        sa.column('type', sa.Enum('exam', 'assignment', 'project', 'quiz')),
        sa.column('status', sa.Enum('sent', 'pending', 'completed', 'overdue')),
        sa.column('delivery_date', sa.Date),
        sa.column('link_classroom', sa.String(512)),
        sa.column('created_at', sa.DateTime),
        sa.column('updated_at', sa.DateTime),
        sa.column('deleted_at', sa.DateTime),
    )
    
    seed_activities = [
        {
            'id': 1,
            'uuid': str(uuid.uuid4()),
            'user_id': 1,
            'title': 'Test Activity 1',
            'description': 'Test Activity 1 Description',
            'type': 'exam',
            'status': 'pending',
            'delivery_date': '2024-11-14',
            'link_classroom': 'https://classroom.example.com/exam-matematicas-final',
            'created_at': '2024-11-14 18:08:42.228475',
            'updated_at': '2024-11-14 18:08:42.228475',
            'deleted_at': None,
        },
        {
            'id': 2,
            'uuid': str(uuid.uuid4()),
            'user_id': 2,
            'title': 'Test Activity 2',
            'description': 'Test Activity 2 Description',
            'type': 'assignment',
            'status': 'sent',
            'delivery_date': '2024-11-14',
            'link_classroom': 'https://classroom.example.com/assignment-matematicas-final',
            'created_at': '2024-11-14 18:20:42.228475',
            'updated_at': '2024-11-14 18:20:42.228475',
            'deleted_at': None,
        },
        {
            'id': 3,
            'uuid': str(uuid.uuid4()),
            'user_id': 3,
            'title': 'Test Activity 3',
            'description': 'Test Activity 3 Description',
            'type': 'project',
            'status': 'completed',
            'delivery_date': '2024-11-14',
            'link_classroom': 'https://classroom.example.com/project-matematicas-final',
            'created_at': '2024-11-14 18:08:42.228475',
            'updated_at': '2024-11-14 18:08:42.228475',
            'deleted_at': None,
        },
        {
            "id": 4,
            "uuid": str(uuid.uuid4()),
            "user_id": 4,
            "title": "Test Activity 4",
            "description": "Test Activity 4 Description",
            "type": "quiz",
            "status": "overdue",
            "delivery_date": "2024-11-14",
            "link_classroom": "https://classroom.example.com/quiz-matematicas-final",
            "created_at": "2024-11-14 18:25:42.228475",
            "updated_at": "2024-11-14 18:25:42.228475", 
            "deleted_at": None,
        }
    ]
    
    op.bulk_insert(activities_table, seed_activities)

def downgrade() -> None:
    op.drop_table('activities')
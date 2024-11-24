"""create_table_schedules

Revision ID: 00ed694c00e4
Revises: 58dc05c3eb9a
Create Date: 2024-11-22 01:06:10.949281

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql
from sqlalchemy.dialects.mysql import JSON
import uuid

# revision identifiers, used by Alembic.
revision: str = '00ed694c00e4'
down_revision: Union[str, None] = '58dc05c3eb9a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def generate_uuid() -> str:
    return str(uuid.uuid4())

def upgrade() -> None:
    op.create_table('subjects',
        sa.Column('id', sa.Integer, autoincrement=True, nullable=False, primary_key=True),
        sa.Column('uuid', sa.String(36), nullable=False, unique=True, default=generate_uuid),
        sa.Column('schedule_id', sa.Integer, sa.ForeignKey('schedules.id', ondelete='CASCADE'), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('period', sa.Integer, nullable=False),
        sa.Column('group', sa.String(10), nullable=False),
        sa.Column('semester_grade', sa.Integer, nullable=False),
        sa.Column('serialization_raiting', sa.Integer, nullable=False),
        sa.Column('clearance_raiting', sa.Integer, nullable=False),
        sa.Column('monday', JSON, nullable=True),
        sa.Column('tuesday', JSON, nullable=True),
        sa.Column('wednesday', JSON, nullable=True),
        sa.Column('thursday', JSON, nullable=True),
        sa.Column('friday', JSON, nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.current_timestamp()),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.func.current_timestamp(), onupdate=sa.func.current_timestamp()),
        sa.Column('deleted_at', sa.DateTime(), nullable=True)
    )
    
    subjects_table = sa.table(
        'subjects',
        sa.column('id', sa.Integer()),
        sa.column('uuid', sa.String(36)),
        sa.column('schedule_id', sa.Integer),
        sa.column('name', sa.String(255)),
        sa.column('period', sa.Integer),
        sa.column('group', sa.String(10)),
        sa.column('semester_grade', sa.Integer),
        sa.column('serialization_raiting', sa.Integer),
        sa.column('clearance_raiting', sa.Integer),
        sa.column('monday', JSON),
        sa.column('tuesday', JSON),
        sa.column('wednesday', JSON),
        sa.column('thursday', JSON),
        sa.column('friday', JSON),
        sa.column('created_at', sa.DateTime()),
        sa.column('updated_at', sa.DateTime()),
        sa.column('deleted_at', sa.DateTime()),
    )
    
    seed_subjects = [
        {
            "id": 1,
            "uuid": str(uuid.uuid4()),
            'schedule_id': 1,
            "name": 'Expresión Oral y Escrita II',
            'period': 9,
            'group': 'A',
            'semester_grade': 1,
            'serialization_raiting': 0,
            'clearance_raiting': 1,
            'monday': [8, 9],
            'tuesday': [8, 9],
            'wednesday': [8, 9],
            'thursday': [8, 9],
            'friday': [8, 9],
            'created_at': '2024-11-21 23:58:37.470493',
            'updated_at': '2024-11-21 23:58:37.470493',
            'deleted_at': None,
        },
        {
            "id": 2,
            "uuid": str(uuid.uuid4()),
            'schedule_id': 1,
            "name": 'Arquitectura orientada a servicios',
            'period': 9,
            'group': 'A',
            'semester_grade': 1,
            'serialization_raiting': 0,
            'clearance_raiting': 1,
            'monday': [10, 11],
            'tuesday': [10, 11],
            'wednesday': [10, 11],
            'thursday': [10, 11],
            'friday': [10, 11],
            'created_at': '2024-11-21 23:58:37.470493',
            'updated_at': '2024-11-21 23:58:37.470493',
            'deleted_at': None,
        },
        {
            "id": 3,
            "uuid": str(uuid.uuid4()),
            'schedule_id': 1,
            "name": 'Administración de proyectos',
            'period': 9,
            'group': 'A',
            'semester_grade': 1,
            'serialization_raiting': 0,
            'clearance_raiting': 1,
            'monday': [11, 12],
            'tuesday': [11, 12],
            'wednesday': [11, 12],
            'thursday': [11, 12],
            'friday': [11, 12],
            'created_at': '2024-11-21 23:58:37.470493',
            'updated_at': '2024-11-21 23:58:37.470493',
            'deleted_at': None,
        },
        {
            "id": 4,
            "uuid": str(uuid.uuid4()),
            'schedule_id': 1,
            "name": 'Minería de datos',
            'period': 9,
            'group': 'A',
            'semester_grade': 1,
            'serialization_raiting': 0,
            'clearance_raiting': 1,
            'monday': [12, 13],
            'tuesday': [12, 13],
            'wednesday': [12, 13],
            'thursday': [12, 13],
            'friday': [12, 13],
            'created_at': '2024-11-21 23:58:37.470493',
            'updated_at': '2024-11-21 23:58:37.470493',
            'deleted_at': None,
        },
        {
            "id": 5,
            "uuid": str(uuid.uuid4()),
            'schedule_id': 2,
            "name": 'Seguridad de la información',
            'period': 9,
            'group': 'A',
            'semester_grade': 1,
            'serialization_raiting': 0,
            'clearance_raiting': 1,
            'monday': [13, 14],
            'tuesday': [13, 14],
            'wednesday': [13, 14],
            'thursday': [13, 14],
            'friday': [13, 14],
            'created_at': '2024-11-21 23:58:37.470493',
            'updated_at': '2024-11-21 23:58:37.470493',
            'deleted_at': None,
        },
        {
            "id": 6,
            "uuid": str(uuid.uuid4()),
            'schedule_id': 2,
            "name": 'Ingles IX',
            'period': 9,
            'group': 'A',
            'semester_grade': 1,
            'serialization_raiting': 0,
            'clearance_raiting': 1,
            'monday': [14, 15],
            'tuesday': [14, 15],
            'wednesday': [14, 15],
            'thursday': [14, 15],
            'friday': [14, 15],
            'created_at': '2024-11-21 23:58:37.470493',
            'updated_at': '2024-11-21 23:58:37.470493',
            'deleted_at': None,
        },
    ]
    
    op.bulk_insert(subjects_table, seed_subjects)


def downgrade() -> None:
    op.drop_table('subjects')
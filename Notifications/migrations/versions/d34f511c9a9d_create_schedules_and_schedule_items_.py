"""Create schedules and schedule_items tables and seed data

Revision ID: d34f511c9a9d
Revises: d0e032aa4973
Create Date: 2024-10-01 23:42:19.707732

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.mysql import JSON
import uuid



revision: str = 'd34f511c9a9d'
down_revision: Union[str, None] = 'd0e032aa4973'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def generate_uuid():
    """Helper function to generate a UUIDs for seed data"""
    return str(uuid.uuid4())

def upgrade():
    
    
    op.create_table(
        'schedules',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('uuid', sa.String(36), nullable=False, unique=True, default=lambda: str(uuid.uuid4())),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id'), nullable=False)
    )

    
    op.create_table(
        'schedule_items',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("uuid", sa.String(36), nullable=False, unique=True, default=lambda: str(uuid.uuid4())),
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

    
    schedules_table = sa.table(
        'schedules',
        sa.column('id', sa.Integer),
        sa.column('uuid', sa.String(36)),
        sa.column('user_id', sa.Integer),
    )

    
    seed_schedules = [
        {
            'id': 1,  
            'uuid': generate_uuid(),
            'user_id': 1,  
        },
        {
            'id': 2,
            'uuid': generate_uuid(),
            'user_id': 2,  
        },
    ]

    
    op.bulk_insert(schedules_table, seed_schedules)

   
    schedule_items_table = sa.table(
        'schedule_items',
        sa.column('id', sa.Integer),
        sa.column('uuid', sa.String(36)),
        sa.column('schedule_id', sa.Integer),
        sa.column('nombre', sa.String(255)),
        sa.column('grupo', sa.String(50)),
        sa.column('cuatrimestre', sa.Integer),
        sa.column('calif_cuatrimestre', sa.Integer),
        sa.column('calif_holgura', sa.Integer),
        sa.column('calif_seriacion', sa.Integer),
        sa.column('lunes', JSON),
        sa.column('martes', JSON),
        sa.column('miercoles', JSON),
        sa.column('jueves', JSON),
        sa.column('viernes', JSON),
    )

   
    seed_schedule_items = [
        {
            'id': 1,
            'uuid': generate_uuid(),
            'schedule_id': 1,
            'nombre': 'Matemáticas',
            'grupo': 'A',
            'cuatrimestre': 1,
            'calif_cuatrimestre': 90,
            'calif_holgura': 85,
            'calif_seriacion': 88,
            'lunes': {"start": "08:00", "end": "10:00"},
            'martes': {"start": "10:00", "end": "12:00"},
            'miercoles': None,
            'jueves': {"start": "14:00", "end": "16:00"},
            'viernes': {"start": "16:00", "end": "18:00"},
        },
        {
            'id': 2,
            'uuid': generate_uuid(),
            'schedule_id': 1,
            'nombre': 'Física',
            'grupo': 'B',
            'cuatrimestre': 1,
            'calif_cuatrimestre': 85,
            'calif_holgura': 80,
            'calif_seriacion': 82,
            'lunes': None,
            'martes': {"start": "12:00", "end": "14:00"},
            'miercoles': {"start": "14:00", "end": "16:00"},
            'jueves': None,
            'viernes': {"start": "10:00", "end": "12:00"},
        },
        {
            'id': 3,
            'uuid': generate_uuid(),
            'schedule_id': 2,
            'nombre': 'Química',
            'grupo': 'A',
            'cuatrimestre': 2,
            'calif_cuatrimestre': 88,
            'calif_holgura': 90,
            'calif_seriacion': 85,
            'lunes': {"start": "08:00", "end": "10:00"},
            'martes': None,
            'miercoles': {"start": "10:00", "end": "12:00"},
            'jueves': {"start": "12:00", "end": "14:00"},
            'viernes': None,
        },
    ]

   
    op.bulk_insert(schedule_items_table, seed_schedule_items)


def downgrade():
    
    schedule_items_table = sa.table(
        'schedule_items',
        sa.column('id', sa.Integer),
        sa.column('uuid', sa.String(36)),
        sa.column('schedule_id', sa.Integer),
        sa.column('nombre', sa.String(255)),
        sa.column('grupo', sa.String(50)),
        sa.column('cuatrimestre', sa.Integer),
        sa.column('calif_cuatrimestre', sa.Integer),
        sa.column('calif_holgura', sa.Integer),
        sa.column('calif_seriacion', sa.Integer),
        sa.column('lunes', JSON),
        sa.column('martes', JSON),
        sa.column('miercoles', JSON),
        sa.column('jueves', JSON),
        sa.column('viernes', JSON),
    )

   
    op.execute(
        schedule_items_table.delete().where(
            sa.or_(
                sa.and_(
                    schedule_items_table.c.id == 1,
                    schedule_items_table.c.schedule_id == 1,
                ),
                sa.and_(
                    schedule_items_table.c.id == 2,
                    schedule_items_table.c.schedule_id == 1,
                ),
                sa.and_(
                    schedule_items_table.c.id == 3,
                    schedule_items_table.c.schedule_id == 2,
                ),
            )
        )
    )

 
    schedules_table = sa.table(
        'schedules',
        sa.column('id', sa.Integer),
        sa.column('uuid', sa.String(36)),
        sa.column('user_id', sa.Integer),
    )

    op.execute(
        schedules_table.delete().where(
            sa.or_(
                schedules_table.c.id == 1,
                schedules_table.c.id == 2,
            )
        )
    )

   
    op.drop_table('schedule_items')
    op.drop_table('schedules')
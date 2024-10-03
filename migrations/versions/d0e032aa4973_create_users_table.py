"""Create users table and seed data

Revision ID: d0e032aa4973
Revises: 
Create Date: 2024-10-01 16:14:32.334597

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd0e032aa4973'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Crear la tabla 'users'
    op.create_table('users',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('username', sa.String(length=100), nullable=False),
        sa.Column('email', sa.String(length=100), nullable=False),
        sa.Column('password', sa.String(length=255), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('username'),
        sa.UniqueConstraint('email')
    )
    
    # Definir la tabla 'users' para usar en bulk_insert, excluyendo 'id'
    users_table = sa.table(
        'users',
        sa.column('username', sa.String(length=100)),
        sa.column('email', sa.String(length=100)),
        sa.column('password', sa.String(length=255)),
    )

    # Datos de ejemplo para insertar en 'users'
    seed_users = [
        {
            'username': 'john_doe',
            'email': 'john.doe@example.com',
            'password': '$2b$12$KIXQ4.LTn4bF.4ZjX9jEKe/Ju5X1LqHc6HtLYPghW6oRzZVbG1F5O',  # Hasheada
        },
        {
            'username': 'jane_smith',
            'email': 'jane.smith@example.com',
            'password': '$2b$12$A3Wc9pTQZL7P8C1LxQjKkOl8vG6sF7DgH8uI9J0K1M2N3O4P5Q6R7',  # Hasheada
        },
        {
            'username': 'alice_jones',
            'email': 'alice.jones@example.com',
            'password': '$2b$12$B1C2D3E4F5G6H7I8J9K0L1M2N3O4P5Q6R7S8T9U0V1W2X3Y4Z5A6B',  # Hasheada
        },
    ]

    # Insertar los datos en la tabla 'users'
    op.bulk_insert(users_table, seed_users)


def downgrade() -> None:
    # Definir la tabla 'users' para usar en bulk_delete, excluyendo 'id'
    users_table = sa.table(
        'users',
        sa.column('username', sa.String(length=100)),
        sa.column('email', sa.String(length=100)),
        sa.column('password', sa.String(length=255)),
    )

    # Condiciones para eliminar los datos insertados
    op.execute(
        users_table.delete().where(
            sa.or_(
                users_table.c.username == 'john_doe',
                users_table.c.username == 'jane_smith',
                users_table.c.username == 'alice_jones',
            )
        )
    )
    
    # Eliminar la tabla 'users'
    op.drop_table('users')
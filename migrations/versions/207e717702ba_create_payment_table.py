"""Create payment table

Revision ID: 207e717702ba
Revises: b7d4004a8164
Create Date: 2024-10-02 22:47:58.219837

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql


revision: str = '207e717702ba'
down_revision: Union[str, None] = 'b7d4004a8164'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade():
    
    op.create_table('payments',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('preference_id', sa.String(length=255), nullable=False),
        sa.Column('payment_id', sa.String(length=255), nullable=True),
        sa.Column('status', sa.String(length=50), nullable=True),
        sa.Column('status_detail', sa.String(length=255), nullable=True),
        sa.Column('amount', sa.Numeric(10, 2), nullable=False),
        sa.Column('currency_id', sa.String(10), nullable=False),
        sa.Column('description', sa.String(length=255), nullable=True),
        sa.Column('date_created', sa.TIMESTAMP(), nullable=True),  
        sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    

    
    payments_table = sa.table(
        'payments',
        sa.column('id', sa.Integer),
        sa.column('user_id', sa.Integer),
        sa.column('preference_id', sa.String(length=255)),
        sa.column('payment_id', sa.String(length=255)),
        sa.column('status', sa.String(length=50)),
        sa.column('status_detail', sa.String(length=255)),
        sa.column('amount', sa.Numeric(10, 2)),
        sa.column('currency_id', sa.String(length=10)),
        sa.column('description', sa.String(length=255)),
        sa.column('date_created', sa.TIMESTAMP),
        sa.column('created_at', sa.TIMESTAMP),
        sa.column('updated_at', sa.TIMESTAMP),
    )

    
    seed_payments = [
        {
            'user_id': 1,  
            'preference_id': 'pref_12345',
            'payment_id': 'pay_67890',
            'status': 'completed',
            'status_detail': 'Payment successful',
            'amount': 1500.00,
            'currency_id': 'MXN',
            'description': 'Pago mensual de suscripción',
            'date_created': '2024-10-02 10:00:00',
        },
        {
            'user_id': 2,  
            'preference_id': 'pref_54321',
            'payment_id': 'pay_09876',
            'status': 'pending',
            'status_detail': 'Awaiting payment confirmation',
            'amount': 3000.50,
            'currency_id': 'USD',
            'description': 'Pago de curso avanzado',
            'date_created': '2024-10-03 12:30:00',
        },
        {
            'user_id': 1,
            'preference_id': 'pref_11223',
            'payment_id': None,  
            'status': 'failed',
            'status_detail': 'Insufficient funds',
            'amount': 750.75,
            'currency_id': 'MXN',
            'description': 'Pago de compra única',
            'date_created': '2024-10-04 09:15:00',
        },
    ]

    
    op.bulk_insert(payments_table, seed_payments)


def downgrade():
   
    payments_table = sa.table(
        'payments',
        sa.column('id', sa.Integer),
        sa.column('user_id', sa.Integer),
        sa.column('preference_id', sa.String(length=255)),
        sa.column('payment_id', sa.String(length=255)),
        sa.column('status', sa.String(length=50)),
        sa.column('status_detail', sa.String(length=255)),
        sa.column('amount', sa.Numeric(10, 2)),
        sa.column('currency_id', sa.String(length=10)),
        sa.column('description', sa.String(length=255)),
        sa.column('date_created', sa.TIMESTAMP),
        sa.column('created_at', sa.TIMESTAMP),
        sa.column('updated_at', sa.TIMESTAMP),
    )

    
    op.execute(
        payments_table.delete().where(
            sa.or_(
                sa.and_(
                    payments_table.c.user_id == 1,
                    payments_table.c.preference_id == 'pref_12345',
                    payments_table.c.payment_id == 'pay_67890',
                    payments_table.c.amount == 1500.00,
                ),
                sa.and_(
                    payments_table.c.user_id == 2,
                    payments_table.c.preference_id == 'pref_54321',
                    payments_table.c.payment_id == 'pay_09876',
                    payments_table.c.amount == 3000.50,
                ),
                sa.and_(
                    payments_table.c.user_id == 1,
                    payments_table.c.preference_id == 'pref_11223',
                    payments_table.c.payment_id == None,
                    payments_table.c.amount == 750.75,
                ),
            )
        )
    )

    
    op.drop_table('payments')
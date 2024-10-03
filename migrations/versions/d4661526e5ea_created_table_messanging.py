"""Created table messages
 
Revision ID: d4661526e5ea
Revises: 207e717702ba
Create Date: 2024-10-03 08:00:00.000000
 
"""
from typing import Sequence, Union
 
from alembic import op
import sqlalchemy as sa
 
 
revision: str = 'd4661526e5ea'
down_revision: Union[str, None] = '207e717702ba'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None
 
 
def upgrade():
    
    op.create_table('messages',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('recipient_phone_number', sa.String(length=20), nullable=False),
        sa.Column('message_type', sa.String(length=50), nullable=False),
        sa.Column('message_content', sa.Text(), nullable=False),
        sa.Column('status', sa.String(length=50), nullable=False),
        sa.Column('error_message', sa.String(length=255), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    messages_table = sa.table(
        'messages',
        sa.column('recipient_phone_number', sa.String(length=20)),
        sa.column('message_type', sa.String(length=50)),
        sa.column('message_content', sa.Text()),
        sa.column('status', sa.String(length=50)),
        sa.column('error_message', sa.String(length=255)),
    )
 
    seed_data = [
        {
            'recipient_phone_number': '529515271070',
            'message_type': 'template',
            'message_content': 'hello_world',
            'status': 'sent',
            'error_message': None,
        },
        {
            'recipient_phone_number': '529515271071',
            'message_type': 'text',
            'message_content': 'Hola, este es un mensaje de prueba.',
            'status': 'sent',
            'error_message': None,
        },
        {
            'recipient_phone_number': '529515271072',
            'message_type': 'template',
            'message_content': 'invalid_template',
            'status': 'failed',
            'error_message': 'Invalid template name',
        },
        {
            'recipient_phone_number': '529515271073',
            'message_type': 'text',
            'message_content': 'Este mensaje está pendiente de envío.',
            'status': 'pending',
            'error_message': None,
        },
    ]
 
    op.bulk_insert(messages_table, seed_data)
 
 
def downgrade():
    
    messages_table = sa.table(
        'messages',
        sa.column('recipient_phone_number', sa.String(length=20)),
        sa.column('message_type', sa.String(length=50)),
        sa.column('message_content', sa.Text()),
        sa.column('status', sa.String(length=50)),
        sa.column('error_message', sa.String(length=255)),
    )
 
    op.execute(
        messages_table.delete().where(
            sa.or_(
                sa.and_(
                    messages_table.c.recipient_phone_number == '529515271070',
                    messages_table.c.message_type == 'template',
                    messages_table.c.message_content == 'hello_world',
                    messages_table.c.amount == 1500.00,  
                ),
                sa.and_(
                    messages_table.c.recipient_phone_number == '529515271071',
                    messages_table.c.message_type == 'text',
                    messages_table.c.message_content == 'Hola, este es un mensaje de prueba.',
                ),
                sa.and_(
                    messages_table.c.recipient_phone_number == '529515271072',
                    messages_table.c.message_type == 'template',
                    messages_table.c.message_content == 'invalid_template',
                ),
                sa.and_(
                    messages_table.c.recipient_phone_number == '529515271073',
                    messages_table.c.message_type == 'text',
                    messages_table.c.message_content == 'Este mensaje está pendiente de envío.',
                ),
            )
        )
    )
 
    op.drop_table('messages')
"""create user tables

Revision ID: 3473402c38bc
Revises: None
Create Date: 2012-11-14 22:35:40.666134

"""

# revision identifiers, used by Alembic.
revision = '3473402c38bc'
down_revision = None

from alembic import op
import sqlalchemy as sa

def upgrade():
    op.create_table('user_info',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('motoo', sa.String(255)),
        sa.Column('introduction', sa.Text),
        sa.Column('phone', sa.String(15), unique=True, nullable=True),
        sa.Column('phone_status', sa.Integer, nullable=True),
        sa.Column('photo', sa.String(255), nullable=True))

def downgrade():
    op.drop_table('user_info')

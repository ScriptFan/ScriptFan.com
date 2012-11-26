"""add privilege

Revision ID: 24c171278ca6
Revises: 107b4efd0f7c
Create Date: 2012-11-26 22:34:28.876708

"""

# revision identifiers, used by Alembic.
revision = '24c171278ca6'
down_revision = '107b4efd0f7c'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('users', sa.Column('privilege', sa.Integer))

def downgrade():
    op.drop_column('users', 'privilege')

"""fix categories

Revision ID: 4b005d73a873
Revises: 308b76f8dee7
Create Date: 2013-03-29 00:41:36.953000

"""

# revision identifiers, used by Alembic.
revision = '4b005d73a873'
down_revision = '308b76f8dee7'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.alter_column('categories', 'name', existing_type=sa.Integer, existing_nullable=False, type_=sa.String(255))
    op.drop_column('categories', 'slug') 


def downgrade():
    op.alter_column('categories', 'name', existing_type=sa.String(255), type_=sa.Integer)
    op.add_column('categories', sa.Column('slug', sa.Integer, nullable=False, unique=True))

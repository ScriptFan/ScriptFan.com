"""remove type field from articles

Revision ID: 308b76f8dee7
Revises: 504407e54867
Create Date: 2013-03-14 08:12:18.234000

"""

# revision identifiers, used by Alembic.
revision = '308b76f8dee7'
down_revision = '504407e54867'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.drop_column('articles', 'type')


def downgrade():
    op.add_column('articles', sa.Column('type', sa.Integer))

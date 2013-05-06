"""remove tag count

Revision ID: 50321cae8ba5
Revises: 921338e045b
Create Date: 2013-05-07 02:01:46.234000

"""

# revision identifiers, used by Alembic.
revision = '50321cae8ba5'
down_revision = '921338e045b'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.drop_column('tags', 'count')


def downgrade():
    op.add_column('tags', sa.Column('count', sa.Integer, default=0))


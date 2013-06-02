"""article draft

Revision ID: 11fb09f6dba5
Revises: 50321cae8ba5
Create Date: 2013-06-02 19:11:42.968000

"""

# revision identifiers, used by Alembic.
revision = '11fb09f6dba5'
down_revision = '50321cae8ba5'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('articles', sa.Column('published', sa.Boolean(), nullable=False))

def downgrade():
    op.drop_column('articles', 'published')

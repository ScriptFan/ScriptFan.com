"""create articles table

Revision ID: 504407e54867
Revises: 24c171278ca6
Create Date: 2013-03-13 00:31:25.500000

"""

# revision identifiers, used by Alembic.
revision = '504407e54867'
down_revision = '24c171278ca6'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table('categories',
            sa.Column('id', sa.Integer, primary_key=True),
            sa.Column('name', sa.Integer, nullable=False, unique=True),
            sa.Column('slug', sa.Integer, nullable=False, unique=True))

    op.create_table('articles',
            sa.Column('id', sa.Integer, primary_key=True),
            sa.Column('title', sa.String(255), nullable=False),
            sa.Column('type', sa.Integer), # news/anno/posts/
            sa.Column('content', sa.Text, nullable=False),
            sa.Column('content_html', sa.Text, nullable=True),
            sa.Column('author_id', sa.Integer),
            sa.Column('category_id', sa.Integer),
            sa.Column('created_time', sa.DateTime),
            sa.Column('updated_time', sa.DateTime))

def downgrade():
    op.drop_table('articles')
    op.drop_table('categories')

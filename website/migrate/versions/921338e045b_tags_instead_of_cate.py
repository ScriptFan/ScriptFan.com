"""tags instead of categories

Revision ID: 921338e045b
Revises: 4b005d73a873
Create Date: 2013-04-12 00:04:49.796000

"""

# revision identifiers, used by Alembic.
revision = '921338e045b'
down_revision = '4b005d73a873'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.drop_column('articles', 'category_id')
    op.drop_table('categories')

    op.create_table('tags',
            sa.Column('id', sa.Integer, primary_key=True),
            sa.Column('name', sa.String(255), nullable=False, unique=True),
            sa.Column('slug', sa.String(255), nullable=True,  unique=True),
            sa.Column('count', sa.Integer, default=0))

    op.create_table('article_tags',
            sa.Column('id', sa.Integer, primary_key=True),
            sa.Column('article_id', sa.Integer, nullable=False),
            sa.Column('tag_id', sa.Integer, nullable=False))

def downgrade():
    op.drop_table('article_tags')
    op.drop_table('tags')

    op.create_table('categories',
            sa.Column('id', sa.Integer, primary_key=True),
            sa.Column('name', sa.String(255), nullable=False, unique=True))
    op.add_column('articles', sa.Column('category_id', sa.Integer))

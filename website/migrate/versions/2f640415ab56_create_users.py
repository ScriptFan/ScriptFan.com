"""create_users

Revision ID: 2f640415ab56
Revises: None
Create Date: 2012-11-23 23:37:50.277992

"""

# revision identifiers, used by Alembic.
revision = '2f640415ab56'
down_revision = None

from alembic import op
import sqlalchemy as sa

def upgrade():
    op.create_table('users',
            sa.Column('id', sa.Integer, primary_key=True),
            sa.Column('slug', sa.String(255)),
            sa.Column('nickname', sa.String(255)),
            sa.Column('password', sa.String(255)),
            sa.Column('email', sa.String(255)),
            sa.Column('email_security', sa.Integer),
            sa.Column('phone', sa.String(255)),
            sa.Column('phone_security', sa.Integer),
            sa.Column('photo', sa.String(255)),
            sa.Column('photo_security', sa.Integer),
            sa.Column('motoo', sa.String(255)),
            sa.Column('intro', sa.Text),
            sa.Column('login_time', sa.DateTime),
            sa.Column('created_time', sa.DateTime),
            sa.Column('updated_time', sa.DateTime))

    op.create_table('user_openids',
            sa.Column('id', sa.Integer, primary_key=True),
            sa.Column('provider', sa.String(255)),
            sa.Column('user_id', sa.Integer),
            sa.Column('openid', sa.String(255)))

def downgrade():
    op.drop_table('user_openids')
    op.drop_table('users')

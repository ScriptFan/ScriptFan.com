"""rename_security_to_privacy

Revision ID: 107b4efd0f7c
Revises: 30cb49648d54
Create Date: 2012-11-24 00:50:50.629688

"""

# revision identifiers, used by Alembic.
revision = '107b4efd0f7c'
down_revision = '30cb49648d54'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.alter_column('users', 'email_security', name='email_privacy',
            existing_type=sa.Integer)
    op.alter_column('users', 'phone_security', name='phone_privacy',
            existing_type=sa.Integer)
    op.alter_column('users', 'photo_security', name='photo_privacy',
            existing_type=sa.Integer)

def downgrade():
    op.alter_column('users', 'email_privacy', name='email_security',
            existing_type=sa.Integer)
    op.alter_column('users', 'phone_privacy', name='phone_security',
            existing_type=sa.Integer)
    op.alter_column('users', 'photo_privacy', name='photo_security',
            existing_type=sa.Integer)

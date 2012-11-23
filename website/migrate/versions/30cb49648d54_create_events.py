"""create_events

Revision ID: 30cb49648d54
Revises: 2f640415ab56
Create Date: 2012-11-24 00:11:32.773938

"""

# revision identifiers, used by Alembic.
revision = '30cb49648d54'
down_revision = '2f640415ab56'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table('events',
            sa.Column('id', sa.Integer, primary_key=True),
            sa.Column('title', sa.String(255)),
            sa.Column('content', sa.Text),
            sa.Column('content_html', sa.Text),
            sa.Column('address', sa.String(255)),
            sa.Column('lat', sa.Numeric(10,7)),
            sa.Column('lng', sa.Numeric(10,7)),
            sa.Column('status', sa.Integer),
            sa.Column('creator_id', sa.DateTime),
            sa.Column('created_time', sa.DateTime),
            sa.Column('updated_time', sa.DateTime))

    op.create_table('event_durations',
            sa.Column('id', sa.Integer, primary_key=True),
            sa.Column('event_id', sa.Integer),
            sa.Column('date', sa.Date),
            sa.Column('start_time', sa.Time),
            sa.Column('end_time', sa.Time))

    op.create_table('event_members',
            sa.Column('id', sa.Integer, primary_key=True),
            sa.Column('event_id', sa.Integer),
            sa.Column('member_id', sa.Integer),
            sa.Column('status', sa.Integer))

def downgrade():
    op.drop_table('event_members')
    op.drop_table('event_durations')
    op.drop_table('events')

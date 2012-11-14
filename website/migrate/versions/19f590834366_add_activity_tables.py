"""Add activity tables

Revision ID: 19f590834366
Revises: 43cda5e14cf0
Create Date: 2012-11-14 23:31:56.202053

"""

# revision identifiers, used by Alembic.
revision = '19f590834366'
down_revision = '43cda5e14cf0'

from alembic import op
import sqlalchemy as db


def upgrade():
    op.create_table('activities',
        db.Column('id', db.Integer, primary_key=True),
        db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
        db.Column('title', db.String(255)),
        db.Column('content', db.Text),
        db.Column('slug', db.String(255)),
        db.Column('start_time', db.DateTime),
        db.Column('end_time', db.DateTime),
        db.Column('address', db.String(255)),
        db.Column('longitude', db.Numeric(10, 7)),
        db.Column('latitude', db.Numeric(10, 7)),
        db.Column('created_time', db.DateTime),
        db.Column('modified_time', db.DateTime))

    op.create_table('activity_users',
        db.Column('activity_id', db.Integer, db.ForeignKey('activities.id'), primary_key=True),
        db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True))

    op.create_table('resources',
        db.Column('id', db.Integer, primary_key=True),
        db.Column('cser_id', db.Integer, db.ForeignKey('users.id')),
        db.Column('filetype', db.String(50)),
        db.Column('url', db.String(255)),
        db.Column('created_time', db.DateTime),
        db.Column('modified_time', db.DateTime))

    op.create_table('activity_resources',
        db.Column('activity_id', db.Integer, db.ForeignKey('activities.id'), primary_key=True),
        db.Column('resource_id', db.Integer, db.ForeignKey('resources.id'), primary_key=True))

    op.create_table('activity_comments',
        db.Column('id', db.Integer, primary_key=True),
        db.Column('author_name', db.String(50)),
        db.Column('author_email', db.String(255)),
        db.Column('author_site', db.String(255)),
        db.Column('content', db.Text, nullable=False),
        db.Column('created_time', db.DateTime),
        db.Column('modified_time', db.DateTime),
        db.Column('parent_id', db.Integer, db.ForeignKey('activity_comments.id')),
        db.Column('user_id', db.Integer, db.ForeignKey('users.id')))

    op.create_table('topics',
        db.Column('id', db.Integer, primary_key=True),
        db.Column('name', db.String(255)),
        db.Column('inro', db.Text),
        db.Column('rate_count', db.Integer, default=0),
        db.Column('user_id', db.Integer, db.ForeignKey('users.id'), nullable=False))

    op.create_table('topic_resources',
        db.Column('topic_id', db.Integer, db.ForeignKey('topics.id'), primary_key=True),
        db.Column('resource_id', db.Integer, db.ForeignKey('resources.id'), primary_key=True))

    op.create_table('topic_users',
        db.Column('topic_id', db.Integer, db.ForeignKey('topics.id'), primary_key=True),
        db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True))

def downgrade():
    op.drop_table('topic_users')
    op.drop_table('topic_resources')
    op.drop_table('topics')
    op.drop_table('activity_comments')
    op.drop_table('activity_resources')
    op.drop_table('resources')
    op.drop_table('activity_users')
    op.drop_table('activities')

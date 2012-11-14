"""Update user tables

Revision ID: 43cda5e14cf0
Revises: 3473402c38bc
Create Date: 2012-11-14 23:11:34.817678

"""


revision = '43cda5e14cf0'
down_revision = '3473402c38bc'

from alembic import op
import sqlalchemy as db
from datetime import datetime

def upgrade():
    op.create_table('users',
        db.Column('id', db.Integer, primary_key=True),
        db.Column('email', db.String(50), unique=True, nullable=False), 
        db.Column('email_status', db.Integer, nullable=True, default=0),
        db.Column('nickname', db.String(50), unique=True, nullable=False),
        db.Column('password', db.String(50), nullable=True),
        db.Column('is_email_verified', db.Boolean, nullable=False, default=True),
        db.Column('slug', db.String(50), nullable=True),
        db.Column('created_time', db.DateTime, nullable=False, default=datetime.now),
        db.Column('modified_time', db.DateTime, nullable=False, default=datetime.now),
        db.Column('last_login_time', db.DateTime),
        db.Column('privilege', db.Integer, default=3),
        db.Column('user_info_id', db.Integer, db.ForeignKey('user_info.id'), nullable=False))
    
    op.create_table('user_openids',
        db.Column('id', db.Integer, primary_key=True),
        db.Column('user_id', db.Integer, db.ForeignKey('users.id'), nullable=False),
        db.Column('openid', db.String(255), nullable=False, unique=True),
        db.Column('provider', db.String(50), nullable=False)) 

def downgrade():
    op.drop_table('user_openids')
    op.drop_table('users')

#!/usr/bin/env python
#-*-coding:utf-8-*-
import os, sys
sys.path.insert(0, '../../scriptfan.com/website/')

from datetime import datetime
from hashlib import md5, sha1
from flask_peewee.auth import BaseUser
from peewee import *
from scriptfan import db
from scriptfan.models import *

def create_tables():
    User.create_table()
    Relationship.create_table()
    News.create_table()
    NewsComment.create_table()

if __name__ == '__main__':
    create_tables()

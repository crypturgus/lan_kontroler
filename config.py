# -*- coding: utf8 -*-
import os
basedir = os.path.abspath(os.path.dirname(__file__))
print basedir
CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'lancontrol.db')
print SQLALCHEMY_DATABASE_URI
print os.path.join(basedir, 'lancontrol.db')
print os.path.isfile(os.path.join(basedir, 'lancontrol.db'))
DATABASE=os.path.join(basedir, 'lancontrol.db')

# SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_RECORD_QUERIES = True
# WHOOSH_BASE = os.path.join(basedir, 'search.db')

# slow database query threshold (in seconds)
DATABASE_QUERY_TIMEOUT = 0.5




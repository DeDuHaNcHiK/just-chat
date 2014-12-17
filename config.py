# coding: utf-8
import os

basedir = os.path.abspath(os.path.dirname(__file__))

if os.environ.get('DATABASE_URL') is None:
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:postgres@localhost:5432/just_chat'
else:
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_RECORD_QUERIES = True

# slow database query threshold (in seconds)
DATABASE_QUERY_TIMEOUT = 0.5

CSRF_ENABLED = True
SECRET_KEY = 'tLXY5ivB8vVJH3$O2i5OSJ2ShwAgoZH7VJO2i5H+1OSJ2ShQCEfQMhE'
OPENID_PROVIDERS = [
    {'name': 'Google', 'url': 'https://www.google.com/accounts/o8/id'},
    {'name': 'Yahoo', 'url': 'https://me.yahoo.com'},
    {'name': 'Yandex', 'url': 'http://openid.yandex.ru/<username>'},
    # {'name': 'AOL', 'url': 'http://openid.aol.com/<username>'},
    # {'name': 'Flickr', 'url': 'http://www.flickr.com/<username>'},
    # {'name': 'MyOpenID', 'url': 'https://www.myopenid.com'},
    # {'name': 'LiveJournal', 'url': '<username>.livejournal.com'},
    # {'name': 'WordPress.com', 'url': '<username>.wordpress.com'}
    ]

# email server
MAIL_SERVER = 'localhost'
MAIL_PORT = 1025
MAIL_USE_TLS = False
MAIL_USE_SSL = False
MAIL_USERNAME = None
MAIL_PASSWORD = None

# administrator list
ADMINS = ['avtierzov@gmail.com']

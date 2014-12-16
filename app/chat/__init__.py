# coding: utf-8
from config import basedir
from flask.ext.debugtoolbar import DebugToolbarExtension
from flask.ext.sqlalchemy import SQLAlchemy
import os
from flask import Blueprint
from flask.ext.babel import lazy_gettext
from flask.ext.login import LoginManager
from flask.ext.openid import OpenID

chat = Blueprint('chat', __name__)

db = SQLAlchemy()

# define Login manager
lm = LoginManager()
# lm.init_app(chat)
lm.login_view = 'login'
lm.login_message = lazy_gettext('Please log in to access this page.')

# add OpenID login
oid = OpenID(fs_store_path=os.path.join(basedir, 'tmp'))

# toolbar = DebugToolbarExtension(chat)

@chat.record_once
def on_load(state):
    lm.init_app(state.app)
    db.init_app(state.app)
    oid.init_app(state.app)


import views, models

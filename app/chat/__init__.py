# coding: utf-8
from config import basedir
from examples.auth.app import MyAdminIndexView
from flask.ext.admin import Admin, expose
from flask.ext.sqlalchemy import SQLAlchemy
import os
from flask import Blueprint, url_for, redirect
from flask.ext.babel import lazy_gettext
from flask.ext.login import LoginManager, current_user
from flask.ext.openid import OpenID
from werkzeug.routing import RequestRedirect

chat = Blueprint('chat', __name__)

db = SQLAlchemy()

# define Login manager
lm = LoginManager()
lm.login_view = 'login'
lm.login_message = lazy_gettext('Please log in to access this page.')

# add OpenID login
oid = OpenID(fs_store_path=os.path.join(basedir, 'tmp'))


class CustomAdminIndexView(MyAdminIndexView):

    @expose('/')
    def index(self):
        if current_user.is_authenticated():
            if not current_user.is_admin():
                return redirect(url_for('chat.login'))
        else:
            return redirect(url_for('chat.login'))
        return super(CustomAdminIndexView, self).index()

    def is_accessible(self):
        if current_user.is_authenticated():
            return current_user.is_admin()
        return False

    def _handle_view(self, name, **kwargs):
        if not self.is_accessible():
            return RequestRedirect(url_for('chat.login'))


admin = Admin(base_template='layout.html', index_view=CustomAdminIndexView(), template_mode='bootstrap3')


@chat.record_once
def on_load(state):
    lm.init_app(state.app)
    db.init_app(state.app)
    oid.init_app(state.app)
    admin.init_app(state.app)


import views, models

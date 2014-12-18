# coding: utf-8
from hashlib import md5

from app.chat import db, admin
from flask.ext.admin.contrib.sqla import ModelView
from flask.ext.login import current_user
import re


ROLE_USER = 0
ROLE_ADMIN = 1


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    role = db.Column(db.SmallInteger, default=ROLE_USER)
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime)
    rooms = db.relationship('Room', backref='owner', lazy='dynamic')

    def is_admin(self):
        return self.role == ROLE_ADMIN

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def avatar(self, size):
        return 'http://www.gravatar.com/avatar/' + md5(self.email).hexdigest() + '?d=mm&s=' + str(size)

    @staticmethod
    def make_unique_nickname(nickname):
        if User.query.filter_by(nickname=nickname).first() is None:
            return nickname
        version = 2
        new_nickname = nickname + str(version)
        while True:
            new_nickname = nickname + str(version)
            if User.query.filter_by(nickname=new_nickname).first() is None:
                break
            version += 1
        return new_nickname

    @staticmethod
    def make_valid_nickname(nickname):
        return re.sub('[^a-zA-Z0-9_\.]', '', nickname)

    def __repr__(self):
        return '<User %r>' % (self.nickname,)

    def __unicode__(self):
        return self.nickname


class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), index=True, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __unicode__(self):
        return self.name


class CustomView(ModelView):
    list_template = 'admin/admin_list.html'
    create_template = 'admin/admin_create.html'
    edit_template = 'admin/admin_edit.html'

    def is_accessible(self):
        if current_user.is_authenticated():
            return current_user.is_admin()
        return False


class UserAdmin(CustomView):
    column_searchable_list = ('nickname', 'email',)
    column_filters = ('last_seen', 'role', 'email')


admin.add_view(UserAdmin(User, db.session))

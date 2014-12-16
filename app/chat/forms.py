# coding: utf-8
from app.chat.models import User
from flask.ext.wtf import Form
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired


class LoginForm(Form):
    openid = StringField('openid', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)


class RoomAddForm(Form):
    name = StringField('name', validators=[DataRequired()])


class ChangeNicknameForm(Form):
    nickname = StringField('nickname', validators=[DataRequired()])

    def __init__(self, orig_nickname, *args, **kwargs):
        super(ChangeNicknameForm, self).__init__(*args, **kwargs)
        self.orig_nickname = orig_nickname

    def validate(self):
        if not Form.validate(self):
            return False
        if self.nickname.data == self.orig_nickname:
            return True
        if self.nickname.data != User.make_valid_nickname(self.nickname.data):
            self.nickname.errors.append(
                'This nickname has invalid characters. Please use letters, numbers, dots and underscores only.')
            return False
        user = User.query.filter_by(nickname=self.nickname.data).first()
        if user is not None:
            self.nickname.errors.append('This nickname is already in use. Please choose another one.')
            return False
        return True

# coding: utf-8
from datetime import datetime

from app import socketio
from app.chat import chat, lm, db, oid
from app.chat.forms import LoginForm, RoomAddForm, ChangeNicknameForm
from app.chat.models import User, ROLE_USER, Room
from config import DATABASE_QUERY_TIMEOUT, OPENID_PROVIDERS
from flask import g, render_template, flash, url_for, request, session, redirect
from flask.ext.login import current_user, logout_user, login_user, login_required
from flask.ext.socketio import join_room, emit, leave_room
from flask.ext.sqlalchemy import get_debug_queries
from lxml.html import fromstring
from lxml.html.clean import Cleaner, autolink_html


cleaner = Cleaner(
    style=True,
    links=True,
    add_nofollow=True,
    page_structure=True,
    safe_attrs_only=False,
    remove_tags=['p']
)


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@chat.before_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated():
        g.user.last_seen = datetime.utcnow()
        db.session.add(g.user)
        db.session.commit()


@chat.after_request
def after_request(response):
    for query in get_debug_queries():
        if query.duration >= DATABASE_QUERY_TIMEOUT:
            chat.logger.warning(
                "SLOW QUERY: %s\nParameters: %s\nDuration: %fs\nContext: %s\n" % (
                    query.statement,
                    query.parameters,
                    query.duration,
                    query.context
                )
            )
    return response


# @chat.errorhandler(404)
# def not_found_error(error):
# return render_template('404.html'), 404
#
#
# @chat.errorhandler(500)
# def internal_error(error):
# db.session.rollback()
#     return render_template('500.html'), 500


@chat.route('/')
@chat.route('/index')
def index():
    return render_template('index.html')


@chat.route('/login', methods=['GET', 'POST'])
@oid.loginhandler
def login():
    if g.user is not None and g.user.is_authenticated():
        flash('You are already logged in.')
        return redirect(url_for('.index'))
    form = LoginForm()
    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data
        return oid.try_login(form.openid.data, ask_for=['nickname', 'email'])
    return render_template(
        'login.html',
        title='Sign In',
        form=form,
        providers=OPENID_PROVIDERS
    )


@oid.after_login
def after_login(resp):
    if resp.email is None or resp.email == "":
        flash('Invalid login. Please try again.')
        return redirect(url_for('.login'))
    user = User.query.filter_by(email=resp.email).first()
    if user is None:
        nickname = resp.nickname
        if nickname is None or nickname == "":
            nickname = resp.email.split('@')[0]
        nickname = User.make_valid_nickname(nickname)
        nickname = User.make_unique_nickname(nickname)
        user = User(nickname=nickname, email=resp.email, role=ROLE_USER)
        db.session.add(user)
        db.session.commit()
    remember_me = False
    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me', None)
    login_user(user, remember=remember_me)
    return redirect(request.args.get('next') or url_for('.index'))


@chat.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('.index'))


@chat.route('/change_nickname', methods=['GET', 'POST'])
@login_required
def change_nickname():
    form = ChangeNicknameForm(g.user.nickname)
    if form.validate_on_submit():
        g.user.nickname = form.nickname.data
        db.session.add(g.user)
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('.change_nickname'))
    else:
        form.nickname.data = g.user.nickname
    return render_template('change_nickname.html', form=form, title='Change nickname')


@chat.route('/room')
@chat.route('/room/<int:id>')
@login_required
def room_select(id=None):
    if id is not None:
        room = Room.query.get(id)
        session['name'] = g.user.nickname
        session['room'] = room.name
        return redirect(url_for('.chat'))
    rooms = Room.query.all()
    return render_template('room.html', title='Select a room', rooms=rooms)


@chat.route('/room/add', methods=['GET', 'POST'])
@login_required
def room_add():
    form = RoomAddForm()
    if form.validate_on_submit():
        room = Room(name=fromstring(cleaner.clean_html(form.name.data)).text, owner=g.user)
        db.session.add(room)
        db.session.commit()
        session['name'] = g.user.nickname
        session['room'] = form.name.data
        return redirect(url_for('.chat'))
    return render_template('room_add.html', title='Create new room', form=form)


@chat.route('/chat')
@login_required
def chat():
    name = session.get('name', '')
    room = session.get('room', '')
    if name == '' or room == '':
        return redirect(url_for('.index'))
    return render_template('chat.html', name=name, room=room, title='{} room'.format(room))


@socketio.on('joined', namespace='/chat')
def joined(message):
    """Sent by clients when they enter a room.
    A status message is broadcast to all people in the room."""
    room = session.get('room')
    join_room(room)
    emit('status', {'msg': u'<i><strong>{}</strong> has entered the room.</i>'.format(session.get('name'))}, room=room)


@socketio.on('text', namespace='/chat')
def left(message):
    """Sent by a client when the user entered a new message.
    The message is sent to all people in the room."""
    room = session.get('room')
    text = find_links_in_message(message['msg'], session.get('name'))
    emit('message', {
        'msg': text,
    }, room=room)


@socketio.on('left', namespace='/chat')
def left(message):
    """Sent by clients when they leave a room.
    A status message is broadcast to all people in the room."""
    room = session.get('room')
    leave_room(room)
    emit('status', {'msg': u'<i><strong>{}</strong> has left the room.</i>'.format(session.get('name'))}, room=room)


def find_links_in_message(text, name):
    html = fromstring(text)
    result = u'<strong>{}:</strong> '.format(name)
    for i in html.itertext():
        result += autolink_html(i)

    return cleaner.clean_html(result)

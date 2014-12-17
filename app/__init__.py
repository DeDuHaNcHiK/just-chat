# coding: utf-8
from app.moment import MomentJS
from flask import Flask
from flask.ext.socketio import SocketIO


socketio = SocketIO()

app = Flask(__name__)
app.config.from_object('config')
app.debug = False
app.config['DEBUG_TB_TEMPLATE_EDITOR_ENABLED'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.jinja_env.globals['momentjs'] = MomentJS
from chat import chat as chat_blueprint

app.register_blueprint(chat_blueprint)
socketio.init_app(app)

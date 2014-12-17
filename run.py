#!flask/bin/python
from app import app, socketio
from gevent import monkey

monkey.patch_all()

if __name__ == '__main__':
    # app.debug = True
    socketio.run(app, host='0.0.0.0')
web: gunicorn --worker-class socketio.sgunicorn.GeventSocketIOWorker app:app
init: python db_create.py
upgrade: python db_upgrade.py
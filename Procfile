release: python manage.py migrate
release: python db_init.py
web: gunicorn root_app.wsgi --log-file -
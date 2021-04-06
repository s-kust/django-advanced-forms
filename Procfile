release: python manage.py migrate
release: python db_init.py
web: gunicorn planeks.wsgi --log-file -
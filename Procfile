release: python manage.py migrate --noinput && python manage.py ensure_seed_data
web: gunicorn backend.wsgi --log-file -

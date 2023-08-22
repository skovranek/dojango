web: gunicorn planner.wsgi --log-file -
python manage.py collectstatic --noinput
release: ./manage.py migrate --no-input

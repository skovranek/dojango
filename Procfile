web: gunicorn planner.wsgi --log-file -
./manage.py collectstatic --noinput
release: ./manage.py migrate --no-input

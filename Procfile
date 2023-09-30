web: gunicorn main.wsgi --log-file -
./manage.py collectstatic --noinput
release: ./manage.py migrate --no-input

# DoJango
Do + Django = DoJango

[#DoJango_on_Heroku](https://dojango-2bea5c2d6d6c.herokuapp.com/)

## What
DoJango is yet another todo list web app. It demonstrates my knowledge of Python, Django and backend development.

## Why
I made DoJango to challenge myself to build a real functional web app using Python.

## How
It is a [Python](https://www.python.org/) [CRUD](https://en.wikipedia.org/wiki/Create,_read,_update_and_delete) [web app](https://en.wikipedia.org/wiki/Web_application) built with the [Django](https://www.djangoproject.com/) framework, hosted on [Heroku](https://www.heroku.com/home) with a [PostgreSQL](https://www.postgresql.org/) database.

## Download/Install
## Configure
## Implement
## Dependencies
runtime.txt
```
python-3.12.0
```
requirements.txt
```
django>=4.2,<5.0
gunicorn>=21.2,<22.0
dj-database-url>=2.0,<3.0
whitenoise[brotli]>=6.0,<7.0
psycopg; sys_platform == "linux"
psycopg[binary]; sys_platform != "linux"
```
Non-Django dependencies in main/settings.py:
```
MIDDLEWARE = ['whitenoise.middleware.WhiteNoiseMiddleware']
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```
## Testing
The website is manually tested to ensure the UI and backend function as expected.
## Contact
Questions, issues or suggestions: mattjskov at gmail.com
## Contribute
This project is just a proof of concept and I consider it finished.

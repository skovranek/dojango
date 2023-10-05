# DoJango
Do + Django = DoJango

Hosted on Heroku:
[dojango-2bea5c2d6d6c.herokuapp.com](https://dojango-2bea5c2d6d6c.herokuapp.com/)

## What
DoJango is yet another todo list web app. It demonstrates my knowledge of Python, Django and backend development.

## Why
I made DoJango to challenge myself to build a real functional web app using Python.

## How
It is a [Python](https://www.python.org/) [CRUD](https://en.wikipedia.org/wiki/Create,_read,_update_and_delete) [web app](https://en.wikipedia.org/wiki/Web_application) built with the [Django](https://www.djangoproject.com/) framework, hosted on [Heroku](https://www.heroku.com/home) with a [PostgreSQL](https://www.postgresql.org/) database.

## Download/Install
Fork this repo, then clone your forked repo on your local machine: [GitHub Fork A Repo](https://docs.github.com/en/get-started/quickstart/fork-a-repo)

Install the Heroku CLI: [Heroku CLI Installation](https://devcenter.heroku.com/articles/heroku-cli#install-the-heroku-cli)

## Configure
Add your app's web address to the 'main/settings.py' file:
```python
ALLOWED_HOSTS = ['your-app-name-2f9sdf4f5.herokuapp.com']
```

Add the following configuration variables to your app: [Heroku Config Vars](https://devcenter.heroku.com/articles/config-vars)
```
$ heroku config:set DJANGO_SECRET_KEY=your_unique_secret_key
```

You may also choose to enable debug mode while deploying and testing. Change it to an empty string to disable debug mode later.
```
$ heroku config:set DJANGO_DEBUG=True
```

## Implement
Create and verify a Heroku account: [Heroku Sign Up](https://signup.heroku.com/), [Heroku Account Verification](https://devcenter.heroku.com/articles/account-verification)

Subscribe to the Ecos Dynos Plan: [Heroku Ecos Dyno Hours](https://devcenter.heroku.com/articles/eco-dyno-hours)

Using the Heroku CLI, create a Heroku remote for the existing app in the forked repo on your local machine. Do not deploy yet. [Deploying to Heroku with Git](https://devcenter.heroku.com/articles/git)

Create a database for your app by subscribing to the Heroku PostgreSQL Mini plan, for an additional cost. [Provision Heroku PostgreSQL Mini](https://devcenter.heroku.com/articles/provisioning-heroku-postgres)
```
$ heroku addons:create heroku-postgresql:mini
```

Now you may deploy to Heroku with Git, following the instructions linked above.

Check the Heroku log to ensure the app is online and configured correctly:
```
heroku logs --tail
```
If you run into any issues, you may check these articles for additional guidance: 
[Getting Started with Python on Heroku](https://devcenter.heroku.com/articles/getting-started-with-python?singlepage=true)
[Deploying Django on Heroku](https://devcenter.heroku.com/articles/deploying-python)

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

## Testing
The website is manually tested to ensure the UI and backend function as expected.

## Contact
Questions, issues or suggestions: mattjskov at gmail.com

## Contribute
This project is just a proof of concept and I consider it finished.

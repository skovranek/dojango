# DoJango
Do + Django = DoJango

[View DoJango on Heroku](https://dojango-2bea5c2d6d6c.herokuapp.com/)

[![License: LGPL v3](https://img.shields.io/badge/License-LGPL_v3-blue.svg)](https://www.gnu.org/licenses/lgpl-3.0)

## Table of Contents

1) [Overview](#overview)
2) [Features](#Features)
3) [Download/Install With Heroku](#downloadinstall-with-heroku)
4) [Configure and Implement With Heroku](#configure-and-implement-with-heroku)
5) [Run on Localhost](#run-on-localhost)
6) [Customization](#customization)
7) [Dependencies](#dependencies)
8) [Contact](#contact)
9) [Contribute](#contribute)
10) [License](#license)

## Overview
DoJango is yet another todo list web app. More specifically, DoJango is a [Python](https://www.python.org/) [CRUD](https://en.wikipedia.org/wiki/Create,_read,_update_and_delete) [web app](https://en.wikipedia.org/wiki/Web_application) built with the [Django](https://www.djangoproject.com/) framework, hosted on [Heroku](https://www.heroku.com/home) with a [PostgreSQL](https://www.postgresql.org/) database. I challenged myself to build a simple web app using Python. This project demonstrates knowledge of Python, Django and backend development.

## Features
DoJango's features and how to use them are explained on its landing page:
[DoJango Introduction](https://dojango-2bea5c2d6d6c.herokuapp.com/introduction)

- Add, Edit and Delete Models: Categories/Projects, Tasks, SubTasks, Counters.
- "Today's Tasks": See todos listed by priority and due date.
- "Projects": See tasks per project.
- "Deadlines": See tasks listed by due date.
- "Previous # Days": See days with tasks.
- "Library": Find all categories, projects, tasks or unfinished tasks.
- "Archive": See todo lists by date.
- Users are distinguished by browser session id. 
> **Note**
> [Previously](https://github.com/skovranek/dojango/tree/b913092123b2c516eed3b887133bdc9e9670132c), I implemented user accounts but I decided that registering an account was an unnecessary burden to ask of potential users of such a straightforward app.

## Download/Install with Heroku
1) Fork this repo, then clone your forked repo on your local machine: [GitHub Fork A Repo](https://docs.github.com/en/get-started/quickstart/fork-a-repo)

- You may use the GitHub CLI: [GitHub CLI](https://docs.github.com/en/get-started/quickstart/fork-a-repo?tool=cli)
```
$ gh repo fork skovranek/dojango --clone=true
```

- Or you may use the 'Fork' button above, then clone your forked repo: [Browser](https://docs.github.com/en/get-started/quickstart/fork-a-repo?tool=webui)
```
$ git clone https://github.com/YOUR-USERNAME/dojango
```

2) Create and verify a Heroku account: [Heroku Sign Up](https://signup.heroku.com/) & [Heroku Account Verification](https://devcenter.heroku.com/articles/account-verification)

3) Install the Heroku CLI, verify the version, and then login: [Heroku CLI Installation](https://devcenter.heroku.com/articles/heroku-cli#install-the-heroku-cli)
```
$ brew tap heroku/brew && brew install heroku

$ heroku --version

$ heroku login
```

## Configure and Implement with Heroku

1) Subscribe to the Ecos Dynos Plan: [Heroku Ecos Dyno Hours](https://devcenter.heroku.com/articles/eco-dyno-hours)

2) Using the Heroku CLI, create a Heroku remote for the existing app in the forked repo on your local machine. (Do not deploy yet): [Deploying to Heroku with Git](https://devcenter.heroku.com/articles/git)

```
$ heroku git:remote -a your-app-name
```

3) In the 'main/settings.py' file, change the 'ALLOWED_HOSTS' setting to include your app's web address.
```python
ALLOWED_HOSTS = ['your-app-name-2bea5c2d6d6c.herokuapp.com']
```
4) Add your own secret key to the configuration variables of your app: [Heroku Config Vars](https://devcenter.heroku.com/articles/config-vars)
```
$ heroku config:set DJANGO_SECRET_KEY=your_unique_secret_key
```
5) You may also choose to enable debug mode while deploying and testing. Change it to an empty string to disable debug mode later.
```
$ heroku config:set DJANGO_DEBUG=True
```

6) Create a database for your app by subscribing to the Heroku PostgreSQL Mini plan, for an additional cost: [Provision Heroku PostgreSQL Mini](https://devcenter.heroku.com/articles/provisioning-heroku-postgres)
```
$ heroku addons:create heroku-postgresql:mini
```

7) Prepare the database for your app.
```
$ heroku run python manage.py makemigrations

$ heroku run python manage.py migrate
```

8) Create an administrator account. Follow the prompts.
```
$ heroku run python manage.py createsuperuser
```

9) Now you may deploy to Heroku with Git, following the rest of the instructions from the [link](https://devcenter.heroku.com/articles/git) in Step 2.
```
$ git push heroku main
```

10) Check the Heroku log to ensure the app is online and configured correctly.
```
$ heroku logs --tail
```

If you run into any issues, you may check these articles for additional guidance: 

[Getting Started with Python on Heroku](https://devcenter.heroku.com/articles/getting-started-with-python?singlepage=true)

[Deploying Django on Heroku](https://devcenter.heroku.com/articles/deploying-python)

[Medium Article - Deploying Django App to Heroku: Full Guide](https://medium.com/quick-code/deploying-django-app-to-heroku-full-guide-6ff7252578d7)

## Run on Localhost
Django provides a developmental server you may run on localhost, which is free, unlike Heroku.

1) Change the configuration by making these changes in the 'main/settings.py' file: [Django Settings](https://docs.djangoproject.com/en/4.2/ref/settings/#databases)
```python
DEBUG = bool(os.environ.get('DJANGO_DEBUG', True))

# do not push or deploy this secret key to production.
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'q!m3b=%0d1v9m_m+2ygv-o*+3@w0a3vutzuy(ol*$()na10am)')

ALLOWED_HOSTS = ['127.0.0.1']

SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SECURE_PROXY_SSL_HEADER = None

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "dojango_database",
    }
}
```

2) Create a virtual environment: [Python.org Virtual Environment](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/#creating-a-virtual-environment)
```
$ python3 -m venv env
```

3) Activate virtual environment: [Python.org Activate](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/#activating-a-virtual-environment)
```
$ source env/bin/activate
```
**Note**
> When you want to turn off the virtual environment later:
> ```
> $ deactivate
> ```

4) Install dependencies: [Python.org 'requirements.txt'](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/#activating-a-virtual-environment)
```
$ python3 -m pip install -r requirements.txt
```

5) Prepare the database: [Django Workflow](https://docs.djangoproject.com/en/4.2/topics/migrations/#workflow)
```
$ python3 manage.py makemigrations
$ python3 manage.py migrate
```

6) Create a 'superuser' admin account: [Django Admin User](https://docs.djangoproject.com/en/1.8/intro/tutorial02/#creating-an-admin-user)
```
$ python3 manage.py createsuperuser
```

7) Ensure your browser's security settings permit 'http' traffic. Modern browsers automatically redirect requests through 'https' instead of 'http'. This can be a headache for developers who just want to test a local server. Be sure to change your browser's security settings back to your preferences when you are done. 

8) Start the server: [Django 'runserver'](https://docs.djangoproject.com/en/4.2/ref/django-admin/#runserver)
```
$ python3 manage.py runserver
```

9) Use your browser to check your server by navigating to the default localhost address, 'http://127.0.0.1:8000'. This is not a production server and should only be used for development and testing.

## Customization
You may customize DoJango's design by modifying the CSS style in the `todo_app/static/style.css` file.

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

## Contact
Questions, issues or suggestions: mattjskov at gmail.com

## Contribute
This project is just a proof of concept and I consider it finished.

## License
[![License: LGPL v3](https://img.shields.io/badge/License-LGPL_v3-blue.svg)](https://www.gnu.org/licenses/lgpl-3.0)

DoJango is released under the [GNU Lesser General Public License v3.0](LICENSE).

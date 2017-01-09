[![Build Status](https://travis-ci.org/andela-rwachira/cp3.svg?branch=develop)](https://travis-ci.org/andela-rwachira/cp3)
[![Coverage Status](https://coveralls.io/repos/github/andela-rwachira/cp3/badge.svg?branch=develop)](https://coveralls.io/github/andela-rwachira/cp3?branch=develop)
[![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/andela-rwachira/cp3/badges/quality-score.png?b=develop)](https://scrutinizer-ci.com/g/andela-rwachira/cp3/?branch=develop)
![Python Version](https://img.shields.io/badge/python-3.5-brightgreen.svg)

# Bucketlist API. 

This is a to-do list API built using Django REST Framework. Authentication uses [JWT Tokens](https://jwt.io/introduction/).

This API powers a bucketlist app whose repo you can take a look at [here](https://github.com/andela-rwachira/bucket-app/).

## Install

These are the basic steps to install and run the API locally on a linux system:

Create a project directory:
```
$ mkdir cp3

$ cd cp3
```

Set up and activate your virtual environment:

You can find instructions [here](http://docs.python-guide.org/en/latest/dev/virtualenvs/).

Once you have activated your virtualenv, clone the repo from GitHub:
```
$ cd cp3

$ git clone https://github.com/andela-rwachira/cp3
```

Install the requirements:
```
$ pip install -r requirements.txt
```

### Optional: Setting up a PostgreSQL database:

This API uses a PostgreSQL database but you are free to use whichever you'd like. 

If you want to use a PostgreSQL db I'd recommend that you install the [Postgres app](http://postgresapp.com/) to help you set up a local db and [pgAdmin](https://www.pgadmin.org/download/) to manage it. These are not included in the requirements.txt file. 

If this is your first interaction with PostgreSQL, take a look at these brief but helpful directions from [DigitalOcean](https://www.digitalocean.com/community/tutorials/how-to-use-postgresql-with-your-django-application-on-ubuntu-14-04) and [Django Girls](https://djangogirls.gitbooks.io/django-girls-tutorial-extensions/content/optional_postgresql_installation/).

## Launch

Once you have created your database and added your user and password details to the global settings file, activate your virtual environment and run the following commands from the root folder containing manage.py:
```
$ python manage.py makemigrations

$ python manage.py migrate
```

Then create an administrative user to allow you to log in to your application as the admin:
```
$ python manage.py createsuperuser
```

Finally, start the local server and click on the localhost URL to experiment with the API:
```
$ python manage.py runserver
``` 

## Usage

You can watch a 1.30 minute video demo on [Youtube](https://youtu.be/RQAW0YGOEts)

## Testing

Run either of the following commands from the root folder
```
$ python manage.py test

$ coverage run --source='.' manage.py test
```

Run the following command to see the results in an easy-to-read table 
```
$ coverage report
```

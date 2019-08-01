#### FLIGHT BOOKING API
[![Build Status](https://travis-ci.org/marthamareal/flight-booking-app.svg?branch=develop)](https://travis-ci.org/marthamareal/flight-booking-app)
[![Coverage Status](https://coveralls.io/repos/github/marthamareal/flight-booking-app/badge.svg?branch=develop)](https://coveralls.io/github/marthamareal/flight-booking-app?branch=develop)
#### Setup
Before you start, make sure you have the following installed on your machine.
- [PostgreSQL](https://www.postgresql.org/)
- [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv)

Clone the repository with:
```
$ git clone https://github.com/marthamareal/flight-booking-app.git
$ flight-booking-app
```
Install `Python` version of your choice with `pyenv`. eg
```
$ pyenv install 3.5.0  
```
Create and activate a virtual environment with:
```
$ pyenv virtualenv 3.6.5 flight-app  # you can use other python versions eg 3.5.0
$ pyenv activate flight-app 
```

setup database
- create database called `flight-app` with your Postgres.

Rename the .env.sample file to .env and modify the variables with your credentials.

Source the variables with:
```
$ source .env
```
Install dependencies with:
```
$ pip install -r requirements.txt
```
Apply migrations and run the server:
```
$ python manage.py migrate
$ python manage.py runserver
```
Testing the application
```
$ python manage.py test
# with coverage
$ coverage run --source='.' ./manage.py test && coverage report && coverage html
```
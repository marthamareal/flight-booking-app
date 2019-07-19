#### FLIGHT BOOKING API

#### Setup
Before you start, make sure you have the following installed on your machine.
- [PostgreSQL](https://www.postgresql.org/)
- [Pyenv](https://pypi.org/project/pyenv/)

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
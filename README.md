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

Endpoints:
----------

#### Authentication:

`POST /api/auth/users/login/`

Example request body:

```source-json
{
    "email": "jake@jake.com",
    "password": "jakejake"
}
```

No authentication required, returns a User

Required fields: `email`, `password`

#### Registration:

`POST /api/auth/users/`

Example request body:

```source-json
{
    "email": "jake@jake.jake",
    "password": "jakejake",
    "first_name": "jake",
    "last_name": "jake",
    "phone": "+256-789-889-979"
}
```

No authentication required, returns a User

Required fields: `email`,  `password`

#### Create Flight

`POST /api/flights/create/`

Example request body:

```source-json
{
    "provider": "Kenya airwqs",
    "origin": "ebb",
    "destination": "jkia",
    "arrival_time": "2012-09-04T21:00:00Z",
    "departure_time": "2012-09-04T18:00:00Z",
    "seats": ["2A", "2B"]
}
```
Authentication required (must be admin)

#### Get Flights

`GET /api/flights`

Authentication required, returns a list of Flights

#### Book a Flight
`POST api/flights/booking/:flight/`

Example request body:

```source-json
{
    "seat": "2A"
}
```
Authentication required

field seat is optional, if not provided, a seat is assigned to you automatically

#### Cancel Booking
`PUT api/flights/booking/:booking/cancel/`

Authentication required

#### Get bookings on a given date
`PUT api/flights/booking/:flight/:date/`

Authentication required

#### Upload Passport photo
`PUT api/auth/users/passport/upload/`

Authentication required

### Deployment

The API is deployed using [Heroku](https://www.heroku.com/)

Check out the deployed application [here](https://flight-booking-application.herokuapp.com/)
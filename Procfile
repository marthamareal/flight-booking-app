release: python manage.py makemigrations;python manage.py migrate
web: gunicorn flight_booking.wsgi
web: honcho start -f ProcfileHoncho

import os

from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flight_booking.settings')
app = Celery("flight_booking")

app.config_from_object("django.conf:settings")
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS, force=True)
app.conf.CELERY_ALWAYS_EAGER = True
app.conf.CELERY_EAGER_PROPAGATES_EXCEPTIONS = True

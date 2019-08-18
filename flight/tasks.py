from datetime import timedelta

from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger

from django.utils import timezone
from django.conf import settings
from django.core.mail import send_mail

logger = get_task_logger(__name__)

SUBJECT = "Flight Reminder"


@periodic_task(
    run_every=crontab(),
    name="flight_reminder",
    max_retries=5,
    ignore_result=False,
)
def remind_user_traveling():
    from flight.models import Booking

    lower_date = timezone.now().today()  # Current Date
    upper_bound = lower_date + timedelta(days=1)

    bookings = Booking.objects.filter(
        flight__departure_time__gt=lower_date,
        flight__departure_time__lt=upper_bound,
        status='active'
    ).all()
    for booking in bookings:
        email_message = """
        Hello {0},
        This is a reminder that your flight({1}) will be departing at {2} from {3} to {4}
        Kind Regards
        """.format(booking.user.first_name, booking.flight.number,
                   booking.flight.departure_time, booking.flight.origin,
                   booking.flight.destination
                   )
        send_mail(
            subject=SUBJECT,
            message=email_message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[booking.user.email],
        )
        logger.info(
            "Successfully sent mail to {email}".format(email=booking.user.email)
        )

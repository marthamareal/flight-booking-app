from django.db import models

from utils.base.model import BaseModel

from flight_booking import settings

STATUSES = (
    ("active", "active"),
    ("closed", "closed")
)


class Flight(BaseModel):

    provider = models.CharField(max_length=100, blank=False, null=False)
    origin = models.CharField(max_length=100, blank=False, null=False)
    destination = models.CharField(max_length=100, blank=False, null=False)
    departure_time = models.DateTimeField(blank=False, null=False)
    arrival_time = models.DateTimeField(blank=False, null=False)
    number = models.CharField(max_length=25, unique=True)
    status = models.CharField(max_length=10, choices=STATUSES, default=STATUSES[0][0])
    seats = models.ManyToManyField('flight.Seat', related_name='seats')

    def __str__(self):
        return self.number

    @property
    def total_seats(self):
        return self.seats.all()

    @property
    def available_seats(self):
        return self.seats.filter(is_available=True).all()


class Seat(BaseModel):

    seat_number = models.CharField(max_length=10)


class Booking(BaseModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="bookings",
        on_delete=models.CASCADE
    )
    flight = models.ForeignKey(
        Flight, related_name="bookings", on_delete=models.CASCADE
    )
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=10, choices=STATUSES, default=STATUSES[0][0])

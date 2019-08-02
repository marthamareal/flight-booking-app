from django.db import models

from utils.base.model import BaseModel

STATUSES = (
    ("ACTIVE", "active"),
    ("CLOSED", "closed")
)


class Flight(BaseModel):

    provider = models.CharField(max_length=100, blank=False, null=False)
    origin = models.CharField(max_length=100, blank=False, null=False)
    destination = models.CharField(max_length=100, blank=False, null=False)
    departure_time = models.DateTimeField(blank=False, null=False)
    arrival_time = models.DateTimeField(blank=False, null=False)
    flight_number = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=10, choices=STATUSES)

    def __str__(self):
        return self.flight_number

    @property
    def total_seats(self):
        return self.seats.all()

    @property
    def available_seats(self):
        return self.seats.filter(is_available=True).all()


class Seat(BaseModel):

    flight = models.ForeignKey(Flight, related_name="seats", on_delete=models.CASCADE)
    seat_number = models.CharField(max_length=10, blank=False, null=False)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.flight.flight_number}-{self.seat_number}"

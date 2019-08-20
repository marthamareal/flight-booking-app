import factory
from faker import Factory

from flight.models import Flight, Seat

faker = Factory.create()


class SeatFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Seat

    seat_number = factory.LazyAttribute(lambda _: faker.text()[:10])

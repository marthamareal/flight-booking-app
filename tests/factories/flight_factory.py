from datetime import timedelta

from django.utils import timezone

import factory
from faker import Factory

from flight.models import Flight, Booking
from tests.factories.seat_factory import SeatFactory
from tests.factories.user_factory import UserFactory

faker = Factory.create()


class FlightFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Flight

    provider = factory.LazyAttribute(lambda _: faker.text(20))
    origin = factory.LazyAttribute(lambda _: faker.text(20))
    destination = factory.LazyAttribute(lambda _: faker.text(20))
    # departure_time = factory.LazyAttribute(lambda _: timezone.now().today())
    # arrival_time = factory.LazyFunction(lambda _: timezone.now().today() + timedelta(days=365))
    number = factory.LazyAttribute(lambda _: faker.text(9))
    status = factory.LazyAttribute(lambda _: faker.text(20))


class BookingFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Booking
    user = factory.SubFactory(UserFactory)
    seat = factory.SubFactory(SeatFactory)
    flight = factory.SubFactory(FlightFactory)
    status = factory.Iterator(['active', 'closed'])

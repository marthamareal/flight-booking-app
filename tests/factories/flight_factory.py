from datetime import timedelta, datetime

import factory
from faker import Factory
import factory.fuzzy

from flight.models import Flight, Booking
from tests.factories.seat_factory import SeatFactory
from tests.factories.user_factory import UserFactory

faker = Factory.create()


class FlightFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Flight
        exclude = ('now',)

    now = factory.fuzzy.FuzzyDate(datetime.now().date())

    provider = factory.LazyAttribute(lambda _: faker.text(20))
    origin = factory.LazyAttribute(lambda _: faker.text(20))
    destination = factory.LazyAttribute(lambda _: faker.text(20))
    departure_time = factory.LazyAttribute(lambda o: o.now + timedelta(hours=1))
    arrival_time = factory.LazyAttribute(lambda o: o.departure_time + timedelta(days=1))
    number = factory.LazyAttribute(lambda _: faker.text(9))
    status = factory.LazyAttribute(lambda _: faker.text(10))

    @factory.post_generation
    def seats(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for seat in extracted:
                self.seats.add(seat)


class BookingFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Booking
    user = factory.SubFactory(UserFactory)
    seat = factory.SubFactory(SeatFactory)
    flight = factory.SubFactory(FlightFactory)
    status = factory.Iterator(['active', 'closed'])


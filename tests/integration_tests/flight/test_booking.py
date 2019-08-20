from rest_framework import status
from django.urls import reverse

from tests.factories.flight_factory import FlightFactory
from tests.factories.seat_factory import SeatFactory
from tests.integration_tests.flight import BaseTestFlight


class TestFlightBooking(BaseTestFlight):
    """Class for testing """

    def test_book_flight_succeeds(self):
        seat = SeatFactory()
        flight = FlightFactory(seats=[seat])
        response = self.client.post(reverse('book_flight', kwargs={'flight': flight.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

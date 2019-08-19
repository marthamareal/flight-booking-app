from rest_framework import status
from django.urls import reverse

from tests.factories.flight_factory import FlightFactory
from tests.factories.seat_factory import SeatFactory
from tests.integration_tests.flight import BaseTestFlight


class TestFlightBooking(BaseTestFlight):
    """Class for testing """

    def test_book_flight_succeeds(self):
        pass
        # seat = SeatFactory()
        # flight = FlightFactory()
        # response = self.client.post(reverse('book_flight'), flight=flight.id)
        # print(response.data)
        # self.assertEqual(response.status_code, status.HTTP_200_OK)

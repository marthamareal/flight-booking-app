from rest_framework import status
from django.urls import reverse

from tests.factories.flight_factory import FlightFactory
from tests.factories.seat_factory import SeatFactory
from tests.factories.user_factory import UserFactory
from tests.integration_tests.flight import BaseTestFlight


class TestFlight(BaseTestFlight):
    """Class for testing """

    def test_create_flight_with_valid_data_succeeds(self):
        response = self.client.post(reverse('create_flights'), data=self.flight_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_flight_with_invalid_data_fails(self):
        response = self.client.post(reverse('create_flights'), data={})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_flight_not_admin_fails(self):
        user = UserFactory(is_superuser=False)
        user_data = {
            "email": user.email,
            "password": "password123"
        }
        login_response = self.client.post(reverse('login'), data=user_data)
        token = login_response.data["token"]
        self.client.credentials(HTTP_AUTHORIZATION=token)
        response = self.client.post(reverse('create_flights'), data={})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_flights_succeeds(self):

        response = self.client.get(reverse('list_flights'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_flight_succeeds(self):
        seat = SeatFactory(seat_number="2K")
        flight = FlightFactory()
        response = self.client.patch(reverse(
            'single_flight', kwargs={"pk": flight.id}), data={"seats": [seat.seat_number]})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

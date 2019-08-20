from rest_framework import status
from django.urls import reverse

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
        login_response = self.client.post(reverse('login'), data={"email": user.email, "password": "password123"})
        token = login_response.data["token"]
        self.client.credentials(HTTP_AUTHORIZATION=token)
        response = self.client.post(reverse('create_flights'), data={})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_flights_succeeds(self):

        response = self.client.get(reverse('list_flights'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

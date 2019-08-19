from rest_framework.test import APIClient
from django.urls import reverse
from django.test import TestCase

from tests.factories.user_factory import UserFactory


class BaseTestFlight(TestCase):
    """"""

    def setUp(self):
        self.client = APIClient()
        self.user = UserFactory(is_superuser=True)
        self.user_data = {
            "email": self.user.email,
            "password": "password123"
        }
        self.flight_data = {
            "provider": "Kenya Air",
            "origin": "ebb",
            "destination": "jkia",
            "arrival_time": "2019-06-23 8:00",
            "departure_time": "2019-06-23 8:00",
            "seats": ["2U", "28F"]
        }
        self.login_response = self.client.post(reverse('login'), data=self.user_data)
        token = self.login_response.data["token"]
        self.client.credentials(HTTP_AUTHORIZATION=token)
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from django.test import TestCase

from tests.factories.user_factory import UserFactory


class TestLogin(TestCase):
    """Class for testing the User registration"""

    def setUp(self):
        self.client = APIClient()
        self.user = UserFactory()
        data = {
            "email": self.user.email,
            "password": "password123"
        }
        self.login_response = self.client.post(reverse('login'), data=data)

    def test_login_with_valid_data_succeeds(self):
        self.assertIn('You have successfully logged in.', self.login_response.json()['message'])
        self.assertEqual(self.login_response.status_code, status.HTTP_200_OK)

    def test_login_with_invalid_data_fails(self):
        data = {
            "email": self.user.email,
            "password": "wrong123334"
        }
        response = self.client.post(reverse('login'), data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

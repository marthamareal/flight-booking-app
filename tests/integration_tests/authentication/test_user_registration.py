from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from django.test import TestCase

from tests.test_data import valid_user_data, invalid_user_data


class TestRegistration(TestCase):
    """Class for testing the User registration"""

    def setUp(self):
        self.client = APIClient()
        self.register_response = self.client.post(reverse('create_and_list_users'), data=valid_user_data)

    def test_registration_with_valid_data_succeeds(self):
        self.assertIn('Your account has been successfully created.you can login with your email and password.',
                      self.register_response.data['message'])
        self.assertEqual(self.register_response.status_code, status.HTTP_201_CREATED)

    def test_registration_with_invalid_data_fails(self):
        response = self.client.post(reverse('create_and_list_users'), data=invalid_user_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

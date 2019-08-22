import cloudinary.uploader

from unittest.mock import Mock

from rest_framework import status
from rest_framework.test import APIClient

from django.core.files import File
from django.urls import reverse
from django.test import TestCase

from tests.factories.user_factory import UserFactory


class TestUploadImage(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = UserFactory()
        self.user_data = {
            "email": self.user.email,
            "password": "password123"
        }
        self.login_response = self.client.post(reverse('login'), data=self.user_data)
        token = self.login_response.data["token"]
        self.client.credentials(HTTP_AUTHORIZATION=token)

    def test_upload_image_succeeds(self):

        cloudinary_mock_response = {
            'public_id': 'public-id',
            'secure_url': 'http://hello.com/here',
        }
        cloudinary.uploader.upload = Mock(
            side_effect=lambda *args: cloudinary_mock_response)
        image_mock = Mock(spec=File, name='FileMock')

        response = self.client.put(reverse('upload_photo'),
                                   {'passport_photo': image_mock},
                                   format="multipart"
                                   )
        self.assertTrue(cloudinary.uploader.upload.called)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "You have successfully uploaded your photo")

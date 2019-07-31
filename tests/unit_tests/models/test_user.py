import mock

from django.test import TestCase

from authentication.models import User, UserManager


class TestUserModel(TestCase):

    def test_create_user(self):
        with self.assertRaises(ValueError):
            with mock.patch('authentication.models.User') as user_mock:
                user_mock.objects = mock.MagicMock()
                user_mock.objects.create_user = mock.MagicMock()
                user_mock.objects.create_user.return_value = User()

                user_manager = UserManager()
                user_manager.create_user(None, None)
                self.assertTrue(user_mock.objects.create_user.called)

    def test_create_superuser(self):
        with self.assertRaises(ValueError):
            with mock.patch('authentication.models.User') as user_mock:
                user_mock.objects = mock.MagicMock()
                user_mock.objects.create_superuser = mock.MagicMock()
                user_mock.objects.create_superuser.return_value = User()

                user_manager = UserManager()
                user_manager.create_superuser(None, None)
                self.assertTrue(user_mock.objects.create_superuser.called)

    def test_validated_user(self):
        with self.assertRaises(ValueError):
            with mock.patch('authentication.models.User') as user_mock:
                user_mock.objects._validated_user = mock.MagicMock()
                user_mock.objects._validated_user.return_value = User()

                user_manager = UserManager()
                user_manager._validated_user(None, None)
                self.assertTrue(user_mock.objects._validated_user.called)

import mock

from rest_framework.exceptions import ValidationError
from django.test import TestCase

from authentication.serializers import UserSerializer


class TestUserSerializer(TestCase):

    def test_invalid_first_name_fails(self):
        with self.assertRaises(ValidationError):
            with mock.patch('authentication.serializers.BaseUserSerializer') as _mock:
                _mock.validate_field = mock.MagicMock()
                _mock.validate_field.return_value = mock.MagicMock()

                serializer = UserSerializer()
                serializer.validate_first_name('na')
                self.assertTrue(_mock.validate_field.called())

    def test_valid_first_name_succeeds(self):
        with mock.patch('authentication.serializers.BaseUserSerializer') as _mock:
            _mock.validate_field = mock.MagicMock()
            _mock.validate_field.return_value = mock.MagicMock()

            serializer = UserSerializer()
            self.assertEqual(serializer.validate_first_name('Martha'), 'Martha')

    def test_invalid_last_name_fails(self):
        with self.assertRaises(ValidationError):
            with mock.patch('authentication.serializers.BaseUserSerializer') as _mock:
                _mock.validate_field = mock.MagicMock()
                _mock.validate_field.return_value = mock.MagicMock()

                serializer = UserSerializer()
                serializer.validate_last_name('na')
                self.assertTrue(_mock.validate_field.called())

    def test_valid_last_name_succeeds(self):
        with mock.patch('authentication.serializers.BaseUserSerializer') as _mock:
            _mock.validate_field = mock.MagicMock()
            _mock.validate_field.return_value = mock.MagicMock()

            serializer = UserSerializer()
            self.assertEqual(serializer.validate_last_name('Martha'), 'Martha')

    def test_invalid_phone_fails(self):
        with self.assertRaises(ValidationError):
            with mock.patch('authentication.serializers.BaseUserSerializer') as _mock:
                _mock.validate_field = mock.MagicMock()
                _mock.validate_field.return_value = mock.MagicMock()

                serializer = UserSerializer()
                serializer.validate_phone('0 789-889-979')
                self.assertTrue(_mock.validate_field.called())

    def test_valid_phone_succeeds(self):
        with mock.patch('authentication.serializers.BaseUserSerializer') as _mock:
            _mock.validate_field = mock.MagicMock()
            _mock.validate_field.return_value = mock.MagicMock()

            serializer = UserSerializer()
            self.assertEqual(serializer.validate_phone('+256-789-889-979'), '+256-789-889-979')

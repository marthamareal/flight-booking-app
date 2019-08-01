from rest_framework import serializers
from django.contrib.auth import authenticate

from authentication.models import User
from utils.error_messages import error_messages
from utils.regex import patterns
from utils.validators import validate_field


class BaseUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def validate_email(self, field):
        """Validates an email address

        Args:
            field (str): value for email
        Raises:
            ValidationError: if provided email does not match the pattern
        Returns:
            field (str): email value if its valid
        """
        return validate_field(field,
                              patterns['email_pattern'],
                              error_messages['invalid_email'])

    def validate_password(self, field):
        """Validates password

        Args:
            field (str): value for password
        Raises:
            ValidationError: if provided password does not match the pattern
        Returns:
            field (str): password value if its valid
        """
        return validate_field(field,
                              patterns['password_pattern'],
                              error_messages['invalid_password'])


class UserSerializer(BaseUserSerializer):
    """User model serializer"""
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'first_name', 'last_name',
                  'phone', 'image_url', 'created_at', 'updated_at')

        read_only_fields = 'id',

    def validate_first_name(self, field):
        """Validates first_name

        Args:
            field (str): value for first_name
        Raises:
            ValidationError: if provided first_name does not match the pattern
        Returns:
            field (str): first_name value if its valid
        """
        return validate_field(field,
                              patterns['name_pattern'],
                              error_messages['invalid_name'])

    def validate_last_name(self, field):
        """Validates last_name

        Args:
            field (str): value for last_name
        Raises:
            ValidationError: if provided last_name does not match the pattern
        Returns:
            field (str): last_name value if its valid
        """
        return validate_field(field,
                              patterns['name_pattern'],
                              error_messages['invalid_name'])

    def validate_phone(self, field):
        """Validates a user's phone

        Args:
            field (str): value for a user's phone
        Raises:
            ValidationError: if provided phone number does not match the pattern
        Returns:
            field (str): user's phone value if its valid
        """
        return validate_field(field,
                              patterns['phone_number_pattern'],
                              error_messages['invalid_phone_number'])

    def create(self, data):
        return User.objects.create_user(**data)

    def update(self, instance, validated_data):
        """ Updates a user from the data provided
        Args:
            instance(object): User object updated
            validated_data(dict): a dictionary of validated data of a user to update
        Returns:
            user(object): Risk type object updated
        """
        user = super().update(instance, validated_data)
        user.save()
        return user


class LoginSerializer(BaseUserSerializer):
    email = serializers.CharField(max_length=255, required=True)
    password = serializers.CharField(max_length=128, write_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'password')

        read_only_fields = 'id',

    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)

        user = authenticate(username=email, password=password)

        if user is None:
            raise serializers.ValidationError(
                'Invalid login in details, Please make sure your email and password are correct'
            )

        return user

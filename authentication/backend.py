import jwt

from rest_framework import exceptions
from rest_framework.authentication import get_authorization_header, BaseAuthentication

from authentication.models import User
from flight_booking.settings import SECRET_KEY


class JWTAuthentication(BaseAuthentication):

    def authenticate(self, request, **kwargs):
        token = JWTAuthentication.get_token(request, kwargs)

        if not token:
            return None
        try:
            decoded = jwt.decode(token, SECRET_KEY)
            user_id = decoded["id"]
            first_name = decoded["first_name"]

            user = User.objects.get(id=user_id, first_name=first_name)
            return user, token

        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed("User not found, Invalid token")
        except jwt.InvalidTokenError or jwt.DecodeError:
            raise exceptions.AuthenticationFailed("Invalid token Please check your headers an provide the correct token")
        except jwt.ExpiredSignature:
            raise exceptions.AuthenticationFailed("Token expired Login again to get new token")

    @staticmethod
    def get_token(request, kwargs):

        if "token" in kwargs:
            token = kwargs["token"]
        else:
            token = get_authorization_header(request)
        token = token.decode('utf-8')
        return token.replace('Bearer ', '')

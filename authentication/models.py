from datetime import datetime, timedelta

import jwt
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager

from flight_booking.settings import SECRET_KEY
from utils.base.model import BaseModel


class UserManager(BaseUserManager):

    def _validated_user(self, email, password, **kwargs):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **kwargs):
        kwargs.setdefault('is_superuser', True)
        return self._validated_user(email, password, **kwargs)

    def create_user(self, email, password, **kwargs):
        kwargs.setdefault('is_superuser', False)
        return self._validated_user(email, password, **kwargs)


class User(BaseModel, AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100, null=True)
    image_url = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=100, null=True)
    phone = models.CharField(max_length=30, null=True)

    USERNAME_FIELD = 'email'

    objects = UserManager()

    @property
    def token(self):
        payload = {
            "id": str(self.id),
            "first_name": self.first_name,
            "exp": datetime.now() + timedelta(days=1)
        }
        return jwt.encode(payload, SECRET_KEY)

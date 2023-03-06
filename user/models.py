import uuid

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    unique_id = models.CharField(max_length=255, default=uuid.uuid4)
    phone = models.CharField(max_length=191, unique=True, null=True)
    email = models.EmailField(max_length=191, unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_verified = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, help_text="The register time")

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class LoginLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.deletion.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    ip = models.CharField(max_length=91)

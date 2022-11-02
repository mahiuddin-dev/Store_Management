from django.contrib.auth.models import AbstractUser
from django.db import models

from account.manager import UserManager


# Create your models here.
class User(AbstractUser):
    username = None
    unique_id = models.CharField(max_length=16)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    address = models.CharField(max_length=255)

    objects = UserManager()
    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'

from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    username = None
    email = models.EmailField('email address', blank=False, unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

# Create your models here.

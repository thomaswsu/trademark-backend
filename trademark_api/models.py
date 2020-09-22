from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    username = None
    email = models.EmailField('email address', blank=False, unique=True)
    # Note: Making the following two unique would be nice, but returning
    #       an error saying either is in use already would be insecure
    alpaca_key_id = models.CharField(max_length=64, blank=False, null=False)
    alpaca_secret_key = models.CharField(max_length=64, blank=False, null=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

# Create your models here.

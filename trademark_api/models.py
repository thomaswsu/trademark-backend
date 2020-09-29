from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    username = None
    email = models.EmailField('email address', blank=False, unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

class Order(models.Model):
    ACTION_TYPES = (
        ('B', 'Buy'),
        ('S', 'Sell'),
    )
    ORDER_TYPES = (
        ('M', 'Market'),
        ('L', 'Limit'),
    )
    TIF_TYPES = (
        ('GFD', 'Good For Day'),
        ('GTC', 'Good Till Cancelled'),
        ('IOC', 'Immediate or Cancel'),
        ('FOK', 'Fill or Kill'),
    )
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    action_type = models.CharField(max_length=1, choices=ACTION_TYPES, default='M', blank=False, null=False)
    order_type = models.CharField(max_length=1, choices=ORDER_TYPES, default='M', blank=False, null=False)
    execution_price = models.DecimalField(decimal_places=2, max_digits=16, blank=False, null=False)
    time_in_force = models.CharField(max_length=3, choices=TIF_TYPES, default='GFD', blank=False, null=False)
    filled = models.BooleanField(default=False, blank=False, null=False)
    filled_at = models.DateTimeField(default=None, blank=False, null=True)
    cancelled = models.BooleanField(default=False, blank=False, null=False)

    def updateOrderStatus(self):
        # if some call to api:
            # set filled to true
            # create a new Position in the user's portfolio
        return(self.filled)

    def cancelOrder(self):
        # call API to cancel
        self.cancelled = True

# Create your models here.

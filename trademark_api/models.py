from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    username = None
    email = models.EmailField('email address', blank=False, unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def getPortfolioValue(self):
        pass

    def increaseCashBalance(self, amount: int):
        self.investible_cash += amount
        # Check if decimals are fine?
        return(self.investible_cash)

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
    user = models.ForeignKey(get_user_model(), on_delete=models.PROTECT)
    ticker = models.CharField(max_length=5, default="NULL", blank=False, null=False)
    action_type = models.CharField(max_length=1, choices=ACTION_TYPES, default='M', blank=False, null=False)
    order_type = models.CharField(max_length=1, choices=ORDER_TYPES, default='M', blank=False, null=False)
    quantity = models.IntegerField(default=0, blank=False, null=False)
    execution_price = models.DecimalField(decimal_places=2, max_digits=16, blank=False, null=False)
    time_in_force = models.CharField(max_length=3, choices=TIF_TYPES, default='GFD', blank=False, null=False)
    filled = models.BooleanField(default=False, blank=False, null=False)
    filled_at = models.DateTimeField(default=None, blank=False, null=True)
    cancelled = models.BooleanField(default=False, blank=False, null=False)

    def updateOrderStatus(self) -> bool:
        # if some call to api:
            # set filled to true
            # create a new Position in the user's portfolio
        return(self.filled)

    def cancelOrder(self):
        self.updateOrderStatus()
        if not self.filled and not self.cancelled:
            # call API to cancel
            self.cancelled = True
            return True
        return False

class Position(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.PROTECT)
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    ticker = models.CharField(max_length=5)
    is_active = models.BooleanField(default=False, blank=False, null=False)
    # maybe current value for options

class Stock(models.Model):
    position = models.OneToOneField(Position, on_delete=models.PROTECT, primary_key=True)
    number_of_shares = models.IntegerField(blank=False, null=False)
    average_cost = models.DecimalField(decimal_places=2, max_digits=16, blank=False, null=False)
    dividend_yield = models.DecimalField(max_digits=4, decimal_places=2, null=True)

class Option(models.Model):
    OPTION_TYPES = (
        ('C', 'Call'),
        ('P', 'Put'),
    )
    position = models.ForeignKey(Position, on_delete=models.PROTECT)
    option_type = models.CharField(max_length=1, choices=OPTION_TYPES, blank=False, null=False)
    strike_price = models.IntegerField(blank=False, null=False)
    number_of_contracts = models.IntegerField(default=1, blank=False, null=False)
    expiration = models.DateField(blank=False, null=False)

    def getContractValue():
        # Need to hook this up to API
        pass

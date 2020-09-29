from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db.models.fields import BooleanField, CharField, DecimalField, FloatField, IntegerField

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

class Portfolio(models.Model):
    # This is like ___init___
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    username = CharField(max_length=30)
    currentBalance = DecimalField(max_digits=12, decimal_places=2)
    # stocks = {} # This dictionary is indexed by a ticker. The ticker points to an int signifying the amount of stocks that the portfolio contains
    securites = {} # This is a dictionary indexed by a ticker. The ticker points to a dictionary of stock or call or put. The stock key points to an integer. The call or put key the points to dictionary of strike prices. 
    #Example {AAPL : {stock : 100, call : {100 : positon}, put : {100 : positon}}, IBM : {call : {1 : positon, put : {1 : positon}}}} 
    
    def changeUsername(self, newUsername: str) -> str:
        self.username = newUsername
        return(self.username)

    def addBalance(self, amountToAdd: DecimalField) -> DecimalField:
        self.currentBalance += amountToAdd
        # Check if decimals are fine? 
        return(self.currentBalance)
    

    def addOption(self, ticker: CharField, securityType: str, strikePrice: DecimalField, price: FloatField, contracts: IntegerField) -> None: # We might not need price. We need to revise security type
        if ticker in self.securites.keys():
            if securityType in self.securites[ticker].keys():
                if strikePrice in self.securites[ticker][securityType].keys(): # We are now pointing at an options object
                    self.securites[ticker][securityType][strikePrice].addContracts()  
                else:
                    self.securites[ticker][securityType][strikePrice] = Position() # TODO: fill this out later 
            else:
                self.securites[ticker][securityType] = {}
                self.securites[ticker][securityType][strikePrice] = Position() # TODO: Fill this in 
        else:
            self.securites[ticker] = {}
            self.securites[ticker][securityType] = {}
            self.securites[ticker][securityType][strikePrice] = Position() # TODO: fill this in
                

class Position(models.Model):
    ticker = models.CharField(max_length=5)
    price = -1 # TODO: this needs to be hooked up to an API
    amount = 0 

    def addAmount(self, amountToAdd: IntegerField) -> int:
        self.amount += amountToAdd
        return(self.amount)

class Stock(models.Model):
    position = models.OneToOneField(Position, on_delete=models.CASCADE, primary_key=True)
    dividendYield = DecimalField(max_digits=4, decimal_places=2)

class Option(models.Model):
    position = models.OneToOneField(Position, on_delete=models.CASCADE,primary_key=True)
    isCall =  True # models.BooleanField() # Look up how this works
    isPut = not(isCall)
    strikePrice = -1 # Need to hook this up to API
    contractAmount = 0

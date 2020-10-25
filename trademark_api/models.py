from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db.models.fields import CharField
import alpaca_trade_api as tradeapi
import threading
import datetime
import time

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

class Portfolio(models.Model):
    # This is like ___init___
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    username = models.CharField(max_length=30)
    currentBalance = models.DecimalField(max_digits=12, decimal_places=2)
    securites = {} # This is a dictionary indexed by a ticker. 
    # Example {AAPL :  100, IBM : 100} 
    
    def changeUsername(self, newUsername: str) -> str:
        self.username = newUsername
        return(self.username)

    def addBalance(self, amountToAdd: models.DecimalField) -> models.DecimalField:
        self.currentBalance += amountToAdd
        # Check if decimals are fine? 
        return(self.currentBalance)
    
    def addStock(self, ticker: models.CharField, numSecurities: models.IntegerField):
        """
        Note that a ticker can only be 5 characters long 
        """
        if ticker in self.securites:
            self.securites[ticker] += numSecurities
        else:
            self.securites[ticker] = numSecurities

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

def stockAPI() -> None:
    def ___init___(self):
        ALPACA_API_KEY = "CONTACT THOMAS FOR KEY"
        ALPACA_SECRET_KEY = "CONTACT THOMAS FOR KEY"
        APCA_API_BASE_URL = "https://paper-api.alpaca.markets"
        
        self.alpaca = tradeapi.REST(ALPACA_API_KEY, ALPACA_SECRET_KEY, APCA_API_BASE_URL, 'v2')

    def awaitMarketOpen(self):
        isOpen = self.alpaca.get_clock().is_open
        while(not isOpen):
            clock = self.alpaca.get_clock()
            openingTime = clock.next_open.replace(tzinfo=datetime.timezone.utc).timestamp()
            currTime = clock.timestamp.replace(tzinfo=datetime.timezone.utc).timestamp()
            timeToOpen = int((openingTime - currTime) / 60)
            print(str(timeToOpen) + " minutes til market open.")
            time.sleep(60)
            isOpen = self.alpaca.get_clock().is_open

    def run(self) -> None:
        # Wait for market to open.
        print("Waiting for market to open...")
        tAMO = threading.Thread(target=self.awaitMarketOpen)
        tAMO.start()
        tAMO.join()
        print("Market opened.")

    def submitOrder(self, qty, stock, side, resp):
        "Thanks AlpacaAPI"
        if(qty > 0):
            try:
                self.alpaca.submit_order(stock, qty, side, "market", "day")
                print("Market order of | " + str(qty) + " " + stock + " " + side + " | completed.")
                resp.append(True)
            except:
                print("Order of | " + str(qty) + " " + stock + " " + side + " | did not go through.")
                resp.append(False)
            else:
                print("Quantity is 0, order of | " + str(qty) + " " + stock + " " + side + " | not completed.")
                resp.append(True)
    

        

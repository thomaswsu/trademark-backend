from django.db import models

# Create your models here.
class Portfolio(models.Model):
    # This is like ___init___
    username = models.CharField(max_length=30)
    currentBalance = models.DecimalField(max_digits=12, decimal_places=2)
    stocks = {} # This dictionary is indexed by a ticker. The ticker points to an int signifying the amount of stocks that the portfolio contains
    options = {} # This is a dictionary indexed by a ticker. The ticker points to an array of options
    
    def changeUsername(self, newUsername: str) -> str:
        self.username = newUsername
        return(self.username)

    def addBalance(self, amountToAdd: models.DecimalField) -> models.DecimalField:
        self.currentBalance += amountToAdd
        # Check if decimals are fine? 
        return(self.currentBalance)

class Stock(models.Model):
    ticker = models.CharField(max_length=5)
    price = -1 # this needs to be hooked up to an API
    amountShares = 0

class Option(models.Model):
    ticker = models.CharField(max_length=5)
    isCall =  True # models.BooleanField() # Look up how this works
    isPut = not(isCall)
    price = -1 # TODO: Hook this up to an API
    strikePrice = -1 # Need to hook this up to API
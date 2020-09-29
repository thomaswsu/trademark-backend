from django.db import models
from django.db.models.fields import BooleanField, CharField, DecimalField, FloatField, IntegerField

# Create your models here.
class Portfolio(models.Model):
    # This is like ___init___
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
    position = models.OneToOneField(Position, on_delete=models.CASCADE,primary_key=True)
    dividendYield = DecimalField(max_digits=4, decimal_places=2)

class Option(models.Model):
    position = models.OneToOneField(Position, on_delete=models.CASCADE,primary_key=True)
    isCall =  True # models.BooleanField() # Look up how this works
    isPut = not(isCall)
    strikePrice = -1 # Need to hook this up to API
    contractAmount = 0

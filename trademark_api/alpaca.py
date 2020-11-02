import alpaca_trade_api as tradeapi

def stockAPI() -> None:
    """
    Code taken from: 
    https://github.com/alpacahq/alpaca-trade-api-python/blob/master/examples/long-short.py 
    https://github.com/alpacahq/alpaca-trade-api-python/blob/master/examples/martingale.py
    https://alpaca.markets/docs/api-documentation/how-to/market-data/
    https://pypi.org/project/alpaca-trade-api/
    https://algotrading101.com/learn/alpaca-trading-api-guide/
    """
    def ___init___(self):
        ALPACA_API_KEY = "CONTACT THOMAS FOR KEY"
        ALPACA_SECRET_KEY = "CONTACT THOMAS FOR KEY"
        APCA_API_BASE_URL = "https://paper-api.alpaca.markets"
        
        self.alpaca = tradeapi.REST(ALPACA_API_KEY, ALPACA_SECRET_KEY, APCA_API_BASE_URL, 'v2')


        # Figure out how much money we have to work with, accounting for margin
        account_info = self.api.get_account()
        self.equity = float(account_info.equity)
        self.margin_multiplier = float(account_info.multiplier)
        total_buying_power = self.margin_multiplier * self.equity
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
    
    def getCurrentPositions(self) -> None:
        """
        Displays current positions
        """
        self.alpaca.list_positions()
    
    def getPriceData(self, tickers: list, numDays: int):
        """
        Get daily price data for a ticker over the last "n" trading days.
        tsla = api.get_barset(‘TSLA’, ’1Min’)
        tickers is a list of ticker strings [AAPL, GOOG]
        We can get a data frame by returning barset.df
        """
        barset = self.alpaca.get_barset(tickers, 'day', limit=days)
        return(barset)



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

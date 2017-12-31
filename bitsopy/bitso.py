from bitsopy.markets import Market


class Bitso(object):

    def __init__(self, key=None, secret=None):
        self.api_key = key
        self.api_secret = secret
        self.api_base = 'https://api.bitso.com/v3/'
        self.name = 'Bitso'
        self.market = Market(self.api_base)

    def ticker(self, symbol):
        return self.market.get_ticker(symbol)

    def orderbook(self, symbol):
        return self.market.get_orderbook(symbol)

    def trades(self, symbol):
        return self.market.get_trades(symbol)

    def symbols(self):
        return self.market.get_symbols()

    def symbol_details(self):
        return self.market.get_symbol_details()

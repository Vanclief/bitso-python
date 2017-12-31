from bitsopy.requester import Requester
import bitsopy.helpers as helpers

TICKER_URL = "ticker/"
ORDERS_URL = "order_book/"
TRADES_URL = "trades/"
SYMBOL_DETAILS = "available_books/"


class Market(object):

    def __init__(self, api_base):
        self.r = Requester(api_base)

    def get_ticker(self, symbol):
        """
        METHOD: Get
        PARAMS: symbol
        MODEL:
        {
        "mid":"244.755",
        "bid":"244.75",
        "ask":"244.76",
        "last_price":"244.82",
        "low":"244.2",
        "high":"248.19",
        "volume":"7842.11542563",
        "timestamp":"1444253422.348340958"
        }
        """

        endpoint = TICKER_URL + helpers.parse_symbol(symbol)
        status, response = self.r.get(endpoint)

        if status != 200:
            return status, response['error']

        return status, helpers.dict_to_float(response['payload'])

    def get_orderbook(self, symbol):
        """
        METHOD: Get
        PARAMS: symbol
        MODEL:
        {
            "bids":[{
                "price":"574.61",
                "amount":"0.1439327",
                "timestamp":"1472506127.0"
            }],
            "asks":[{
                "price":"574.62",
                "amount":"19.1334",
                "timestamp":"1472506126.0"
            }]
        }
        """

        endpoint = ORDERS_URL + symbol
        status, response = self.r.get(endpoint)

        if status != 200:
            return status, response

        for order_type in response.keys():
            for order in response[order_type]:
                for key, value in order.items():
                    order[key] = float(value)

        return status, response

    def get_trades(self, symbol):
        """
        METHOD: Get
        PARAMS: symbol
        MODEL:
        [{
            "timestamp":1444266681,
            "tid":11988919,
            "price":"244.8",
            "amount":"0.03297384",
            "exchange":"bitfinex",
            "type":"sell"
         }]
        """

        endpoint = TRADES_URL + symbol
        status, response = self.r.get(endpoint)

        if status != 200:
            return status, response

        return status, helpers.list_dict_to_float(response)

    def get_symbols(self):
        """
        METHOD: Get
        MODEL:
        [
            "btcusd",
            "ltcusd",
            "ltcbtc",
            ...
        ]
        """

        endpoint = SYMBOL_DETAILS
        return self.r.get(endpoint)

    def get_symbol_details(self):
        """
        METHOD: Get
        PARAMS:
        MODEL:
        [{
            "pair":"btcusd",
            "price_precision":5,
            "initial_margin":"30.0",
            "minimum_margin":"15.0",
            "maximum_order_size":"2000.0",
            "minimum_order_size":"0.01",
            "expiration":"NA"
        },
        ...
        ]
        """

        endpoint = SYMBOL_DETAILS
        status, response = self.r.get(endpoint)

        if status != 200:
            return status, response

        return status, helpers.list_dict_to_float(response['payload'])
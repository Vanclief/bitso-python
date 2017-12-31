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

        endpoint = ORDERS_URL + helpers.parse_symbol(symbol)
        status, response = self.r.get(endpoint)

        if status != 200:
            return status, response

        parsed_response = {'asks': [], 'bids': []}

        timestamp = helpers.str_to_timestamp(response['payload']['updated_at'])

        for key, values in response['payload'].items():
            for value in values:
                if key in ['bids', 'asks']:

                    ask = {}
                    ask['price'] = float(value['price'])
                    ask['amount'] = float(value['amount'])
                    ask['timestamp'] = timestamp

                    if key == 'asks':
                        parsed_response['asks'].append(ask)
                    elif key == 'bids':
                        parsed_response['bids'].append(ask)

        return status, parsed_response

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

        endpoint = TRADES_URL + helpers.parse_symbol(symbol)
        status, response = self.r.get(endpoint)

        if status != 200:
            return status, response

        parsed_response = []

        for trades in response['payload']:
            trades = helpers.dict_to_float(trades)
            p = {}
            p['timestamp'] = helpers.str_to_timestamp(trades['created_at'])
            p['tid'] = trades['tid']
            p['price'] = trades['price']
            p['amount'] = trades['amount']
            p['exchange'] = 'bitso'
            p['type'] = trades['maker_side']

            parsed_response.append(p)

        return status, parsed_response

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
        status, response = self.r.get(endpoint)

        if status != 200:
            return status, response['error']

        parsed_response = []

        for s in response['payload']:
            symbol = helpers.unparse_symbol(s['book'])
            parsed_response.append(symbol)

        return status, parsed_response

    def get_symbol_details(self):
        """
        METHOD: Get
        PARAMS:
        MODEL:
        [{
            "pair":"btcusd",
            "price_precision":5,
            "maximum_order_size":"2000.0",
            "minimum_order_size":"0.01",
            "expiration":"NA"
        },
        ]
        """

        endpoint = SYMBOL_DETAILS
        status, response = self.r.get(endpoint)

        if status != 200:
            return status, response['error']

        parsed_response = []

        for symbol in response['payload']:
            s = helpers.dict_to_float(symbol)
            p = {}
            p['pair'] = helpers.unparse_symbol(s['book'])
            p['price_precision'] = 5
            p['maximum_order_size'] = s['maximum_amount']
            p['minimum_order_size'] = s['minimum_amount']
            p['expiration'] = "NA"
            parsed_response.append(p)

        return status, parsed_response

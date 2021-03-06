from bitsopy.bitso import Bitso
import httpretty

client = Bitso()

TICKER_URL = 'https://api.bitso.com/v3/ticker/'
ORDERS_URL = 'https://api.bitso.com/v3/order_book/'
TRADES_URL = 'https://api.bitso.com/v3/trades/'
SYMBOL_DETAILS = 'https://api.bitso.com/v3/available_books/'


def test_should_have_correct_url():
    b = Bitso()
    assert b.api_base == 'https://api.bitso.com/v3/'


def test_should_have_api_key():
    b = Bitso('974554aed089', '2976be9e189d')
    assert b.api_key == '974554aed089'


def test_should_have_secret_key():
    b = Bitso('974554aed089', '2976be9e189d')
    assert b.api_secret == '2976be9e189d'


@httpretty.activate
def test_should_return_ticker():

    mock_symbol = 'btcmxn'
    mock_body = (
            '{"success": true, "payload": { "book": "btc_mxn",' +
            '"volume": "22.31349615","high": "5750.00", "last": "5633.98",' +
            '"low": "5450.00","vwap": "5393.45","ask": "5632.24",' +
            '"bid": "5520.01","created_at": "2016-04-08T17:52:31.000+00:00"}' +
            '}'
            )
    mock_url = TICKER_URL + '?book=btc_mxn'
    mock_status = 200

    httpretty.register_uri(
            httpretty.GET, mock_url, body=mock_body, status=mock_status
            )

    expected_response = {
            "mid": 5576.125,
            "bid": 5520.01,
            "ask": 5632.24,
            "last_price": 5633.98,
            "low": 5450.0,
            "high": 5750.0,
            "volume": 22.31349615,
            "timestamp": 1460137951.0
            }

    response = client.ticker(mock_symbol)
    assert expected_response == response[1]


@httpretty.activate
def test_should_return_orderbook():

    mock_symbol = 'btcmxn'
    mock_body = (
            '{"success": true,"payload": {"asks": [{"book": "btc_mxn",' +
            '"price": "5632.24","amount": "1.34491802"}, {"book": "btc_mxn",' +
            '"price": "5633.44","amount": "0.4259"}],"bids": [{' +
            '"book": "btc_mxn", "price": "6123.55", "amount": "1.12560000"' +
            '}, { "book": "btc_mxn", "price": "6121.55","amount": "2.23976"' +
            '}], "updated_at": "2016-04-08T17:52:31.000+00:00",' +
            '"sequence": "27214"}}'
            )

    mock_url = ORDERS_URL + '?book=btc_mxn'
    mock_status = 200

    httpretty.register_uri(
            httpretty.GET, mock_url, body=mock_body, status=mock_status
            )

    expected_response = {
            "bids": [
                {
                    "price": 6123.55,
                    "amount": 1.1256,
                    "timestamp": 1460137951.0
                },
                {
                    "price": 6121.55,
                    "amount": 2.23976,
                    "timestamp": 1460137951.0
                }],
            "asks": [
                {
                    "price": 5632.24,
                    "amount": 1.34491802,
                    "timestamp": 1460137951.0
                },
                {
                    "price": 5633.44,
                    "amount": 0.4259,
                    "timestamp": 1460137951.0
                }
                ]
            }

    response = client.orderbook(mock_symbol)
    assert expected_response == response[1]


@httpretty.activate
def test_should_return_trades():

    mock_symbol = 'btcmxn'
    mock_body = (
            '{"success": true,"payload": [{ "book": "btc_mxn",' +
            '"created_at": "2016-04-08T17:52:31.000+00:00",' +
            '"amount": "0.02000000", "maker_side": "buy","price": "5545.01",' +
            '"tid": 55845}]}'
            )

    mock_url = TRADES_URL + '?book=btc_mxn'
    mock_status = 200

    httpretty.register_uri(
            httpretty.GET, mock_url, body=mock_body, status=mock_status
            )

    expected_response = [
            {
                "timestamp": 1460137951.0,
                "tid": 55845,
                "price": 5545.01,
                "amount": 0.02,
                "exchange": "bitso",
                "type": "buy"
                }
            ]

    response = client.trades(mock_symbol)
    assert expected_response == response[1]


@httpretty.activate
def test_should_return_symbols():

    mock_body = (
            '{"success": true, "payload": [{ "book": "btc_mxn",' +
            '"minimum_amount": ".003", "maximum_amount": "1000.00",' +
            '"minimum_price": "100.00", "maximum_price": "1000000.00",' +
            '"minimum_value": "25.00", "maximum_value": "1000000.00"' +
            '}, {"book": "eth_mxn", "minimum_amount": ".003",' +
            '"maximum_amount": "1000.00", "minimum_price": "100.0",' +
            '"maximum_price": "1000000.0", "minimum_value": "25.0",' +
            '"maximum_value": "1000000.0"}]}'
        )

    mock_url = SYMBOL_DETAILS
    mock_status = 200

    httpretty.register_uri(
            httpretty.GET, mock_url, body=mock_body, status=mock_status
            )

    expected_response = ["btcmxn", "ethmxn"]

    response = client.symbols()
    assert expected_response == response[1]


@httpretty.activate
def test_should_return_symbol_details():

    mock_body = (
            '{"success": true, "payload": [{ "book": "btc_mxn",' +
            '"minimum_amount": ".003", "maximum_amount": "1000.00",' +
            '"minimum_price": "100.00", "maximum_price": "1000000.00",' +
            '"minimum_value": "25.00", "maximum_value": "1000000.00"' +
            '}, {"book": "eth_mxn", "minimum_amount": ".003",' +
            '"maximum_amount": "1000.00", "minimum_price": "100.0",' +
            '"maximum_price": "1000000.0", "minimum_value": "25.0",' +
            '"maximum_value": "1000000.0"}]}'
        )

    mock_url = SYMBOL_DETAILS
    mock_status = 200

    httpretty.register_uri(
            httpretty.GET, mock_url, body=mock_body, status=mock_status
            )

    expected_response = [
            {
                "pair": "btcmxn", "price_precision": 5,
                "maximum_order_size": 1000.0, "minimum_order_size": 0.003,
                "expiration": "NA"
                },
            {
                "pair": "ethmxn", "price_precision": 5,
                "maximum_order_size": 1000.0, "minimum_order_size": 0.003,
                "expiration": "NA"
                },
            ]
    response = client.symbol_details()
    assert expected_response == response[1]

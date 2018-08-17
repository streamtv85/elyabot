import datetime
import ccxt
import requests
import logging
import numpy as np
import pandas as pd

logger = logging.getLogger('bot-service.exchange')


def get_data_from_api(base_url, path):
    response = requests.get(base_url + path)
    assert response.status_code == 200, logger.error(
        "Status code was {0} when accessing {1}".format(response.status_code, base_url + path))
    logger.debug("response from " + base_url + path)
    # logger.debug(response.json())
    return response.json()


def update_ma(new_value, old_value, period):
    if old_value == 0:
        old_value = new_value
    return (new_value + period * old_value) / (period + 1)


class ExchangeWatcher:
    def __init__(self, exchange, symbol):
        self.price = 0
        self.volume = 0
        self.bid = 0
        self.ask = 0
        self.spread = 0
        self.ex = getattr(ccxt, exchange)({'enableRateLimit': True, 'verbose': False})
        assert self.ex.has['publicAPI'], "Exchange {0} doesn't have public API!".format(self.ex.name)
        assert self.ex.has['fetchTicker'], "Exchange {0} doesn't have ticker API!".format(self.ex.name)
        self.symbol = None
        # we do it this way because on Bitfinex there is no BTC/USD pair but BTC/USDT
        for key in sorted(self.ex.load_markets().keys()):
            if symbol in key:
                self.symbol = key
                break
        if not self.symbol:
            raise ValueError("symbol {0} hasn't been found on {1} exchange!".format(symbol, exchange))

    def update(self):
        ticker = self.ex.fetch_ticker(self.symbol)
        self.price = ticker['last']
        self.ask = ticker['ask']
        self.bid = ticker['bid']
        self.spread = self.ask - self.bid
        self.volume = ticker['baseVolume']


class StocksExchangeWatcher:
    def __init__(self):
        self.price = 0
        self.timestamp = datetime.datetime.timestamp()
        pass

    def get_price(self):

        pass


if __name__ == "__main__":
    pass
# bitfin_watcher = ExchangeWatcher('bitfinex', 'BTC/USDT')
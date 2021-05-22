# keys
import config

# libraries
import ta
import ccxt
import pandas as pd

class Data:

	def __init__(self):
		self.exchange = self.exchange_instance(config.exchange)
		self.pair = config.pair

	def exchange_instance(self, exchange):
		if exchange == 'binance':

			exchange = ccxt.binance({
					'apiKey' : config.API_KEY,
					'secret' : config.SECRET_KEY,
					'enableRateLimit': True,
					'timeout' : 15000 ,
					'options': { 'adjustForTimeDifference': True }
				})

		return exchange
		
	def get_balance(self, coin): 
		balance = self.exchange.fetch_balance()
		balance = balance[coin]
		
		return balance

	def get_candle_data(self, period=300, timeframe='5m'):
		candles = self.exchange.fetch_ohlcv(self.pair, limit = period, timeframe = timeframe)
		df = pd.DataFrame(candles, columns = ['unix', 'open', 'high', 'low', 'close', 'volume'])

		return df




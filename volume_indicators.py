
from exchange import Data
from ta.volume import VolumeWeightedAveragePrice

class Volume:

	# basic strength
	def create_bs_signal(self, df, window):
		df['vol_SMA'] = df['volume'].rolling(window = window).mean()
		
		# above average -> buy/sell
		if df['volume'].iloc[-1] > df['vol_SMA'].iloc[-1]:

			return 1

		# bad volume -> wait / do nothing
		else: 

			return -1

class VWAP:

	def calculate_vwap(self, df, window):
		vwap = VolumeWeightedAveragePrice(df['high'], df['low'], df['close'], df['volume'], window = window)
		df['vwap'] = vwap.volume_weighted_average_price()

		return df

	def create_signal(self, df):
		if df['close'].iloc[-1] < df['vwap'].iloc[-1]:
			return 1

		else: 
			return -1




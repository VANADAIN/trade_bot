
from exchange import Data

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

# volume = Volume()
# signal = volume.create_bs_signal(df, 20)
# print(signal)

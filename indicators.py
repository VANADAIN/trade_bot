
from ta.volatility import AverageTrueRange
from ta.momentum import RSIIndicator  
from ta.trend import CCIIndicator
from exchange import Data 
import warnings
warnings.filterwarnings('ignore')

class SuperTrend:

	def average_true_range(self, df, atr_window = 50):
		atr_ta = AverageTrueRange(df['high'], df['low'], df['close'], window = atr_window)
		df['atr'] = atr_ta.average_true_range()

		return df

	def supertrend(self, df, multiplier = 1):
		hl2 = (df['high'] + df['low']) / 2 
		df['upperband'] = hl2 + (multiplier * df['atr'])
		df['lowerband'] = hl2 - (multiplier * df['atr'])
		df['in_uptrend'] = True

		for current in range(1, len(df.index)):
			previous = current - 1
			if df['close'][current] > df['upperband'][previous]:
				df['in_uptrend'][current] = True  
			elif df['close'][current] < df['lowerband'][previous]:
				df['in_uptrend'][current] = False
			else:
				df['in_uptrend'][current] = df['in_uptrend'][previous]

				if df['in_uptrend'][current] and df['lowerband'][current] < df['lowerband'][previous]:
					df['lowerband'][current] = df['lowerband'][previous]

				if not df['in_uptrend'][current] and df['upperband'][current] > df['upperband'][previous]:
					df['upperband'][current] = df['upperband'][previous]

		return df


	def create_signal(self, df):

		if not df['in_uptrend'].iloc[-2] and df['in_uptrend'].iloc[-1]:

			# buy signal 
			return 1
		
		if df['in_uptrend'].iloc[-2] and not df['in_uptrend'].iloc[-1]:

			# sell signal
			return -1

		else:
			if df['in_uptrend'].iloc[-2] and df['in_uptrend'].iloc[-1]:

			# (True - True) -> in a buy trend  
				return 0.5

			if not df['in_uptrend'].iloc[-2] and not df['in_uptrend'].iloc[-1]:

			# (False - False) -> in a sell trend 
				return -0.5

class CCI :

	def calculate_cci(self, df):
		cci = CCIIndicator(df['high'], df['low'], df['close'], window = 10)
		df['cci'] = cci.cci()

		return df 

	def create_signal(self, df):

		if df['cci'].iloc[-1] > 100:
			# if current is less then previous (cci downtrend)
			if df['cci'].iloc[-1] < df['cci'].iloc[-2]:

				return 0 

			else: 

				return 1

		elif df['cci'].iloc[-1] < -100:

			return -1

		# in channel
		else:

			return 0



# data = Data()
# df = data.get_candle_data()
# st = SuperTrend()
# df = st.average_true_range(df, 10)
# df = st.supertrend(df)
# print(df)



# signal = st.create_signal(df)
# print(signal)


import json
import time
import schedule
from datetime import datetime 
from colorama import Fore
from telegram import Notifier
from exchange import Data
from indicators import SuperTrend, CCI
from volume_indicators import Volume

class Trader:

	def __init__(self):
		self.data = Data()
		self.notifier = Notifier()
		self.st_ind = SuperTrend()
		self.volume_ind = Volume()
		self.cci_ind = CCI()
		self.signals = {}

		self.bought_amount = 0
		self.bought_for = 0
		self.sold_for = 0

		self.IN_POSITION = False

	def get_signals(self):
		df = self.data.get_candle_data(200, '5m')
		df = self.st_ind.average_true_range(df, 50)
		df = self.st_ind.supertrend(df)
		df = self.cci_ind.calculate_cci(df)

		# print("-----------\n")
		# print(df.tail(12))
		# print("-----------\n")

		st_signal = self.st_ind.create_signal(df)
		vbs_signal = self.volume_ind.create_bs_signal(df, 30)
		cci_signal = self.cci_ind.create_signal(df)

		self.signals['supertrend'] = st_signal
		self.signals['volume_bs'] = vbs_signal
		self.signals['cci'] = cci_signal

		return df

	def get_available_amount(self, df):
		actual_price = df['close'].iloc[-1] 
		price_for_amount = actual_price + 15.0
		usdt_data = trader.data.get_balance('USDT')
		usdt_free = usdt_data['free']
		amount = usdt_free / price_for_amount

		return actual_price, amount

	def decision_maker(self):
		
		if self.signals['supertrend'] == 1 and self.signals['volume_bs'] == 1 and self.signals['cci'] == 1: 

			return 'buy'

		elif  self.signals['supertrend'] == -1 :
		
			return 'sell'

		else: 

			return 'wait'

	def trade(self, decision, price, amount): 

		# add in_position bool !!!!!!!!!!
		if decision == 'buy' and self.IN_POSITION == False:

			self.buy(price, amount)
			self.IN_POSITION = True
			
		elif decision == 'sell' and self.IN_POSITION == True:

			self.sell(price)
			self.IN_POSITION = False

		else:

			pass

	def buy(self, price, amount): 
		# order = data.exchange.create_market_buy_order('ETH/USDT', amount)
		
		# # save order
		# self.write_order(order, "Buy_")

		# write amount of coin 
		self.bought_amount = amount
		self.bought_for = price

		print(self.signals)

		# notify
		self.notifier.send_message(f'Bought {amount} ETH for {price} $\nTime : {str(datetime.now())}')

	def sell(self, price):
		# order = self.data.create_market_sell_order('ETH/USDT', self.bought_amount)

		# self.write_order(order, "Sell_")

		self.sold_for = price

		print(self.signals)

		self.notifier.send_message(f'Sold {amount} ETH for {price} $\nTime : {str(datetime.now())}')

		self.estimated_income_notifier()


	def write_order(self, order, order_type):
		path = 'trade_data/'
		now = str(datetime.now())
		filename = path + order_type + now + ".json"
		out_file = open(filename, "w")
		json.dump(order, out_file, indent = 4)
		out_file.close() 

	def estimated_income_notifier(self):
		# price in usdt
		buy = self.bought_for
		sell = self.sold_for
		income = sell - buy
		income_rub = income * 75

		if sell > buy:
			text = f'Ммм, чувствую запах денег...\n + {income} $\n + {income_rub} Р. (примерно)'
		else:
			text = f'Бляяяяя, проебался\n - {income} $\n - {income_rub} Р. (примерно)'

		self.notifier.send_message(text)


trader = Trader()
print('Trading now...')

def run():
	# to run on schedule  
	df = trader.get_signals()
	price, amount = trader.get_available_amount(df)
	decision = trader.decision_maker()
	trader.trade(decision, price, amount)


schedule.every(5).minutes.do(run)

while True:
    schedule.run_pending()
    time.sleep(1)







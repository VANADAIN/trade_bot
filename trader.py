
import json
import time
import schedule
from datetime import datetime
from colorama import Fore
from telegram import Notifier
from exchange import Data
from indicators import SuperTrend, CCI, RSI, ROC, S_RSI, EMA
from volume_indicators import Volume, VWAP


class Trader:

    def __init__(self):
        self.data = Data()
        self.notifier = Notifier()

        # self.volume_ind = Volume()
        # self.vwap_ind = VWAP()

        # self.st_ind = SuperTrend()
        # self.ema_ind = EMA()
        # self.srsi_ind = S_RSI()

        # self.cci_ind = CCI()
        self.rsi_ind = RSI()
        # self.roc_ind = ROC()

        self.signals = {}

        self.bought_amount = 0
        self.bought_for = 0
        self.sold_for = 0

        self.IN_POSITION = False

    def get_signals(self, period, frame):
        df = self.data.get_candle_data(period, frame)

        # df, atr_1 = self.st_ind.average_true_range(df, 12)
        # df = self.st_ind.supertrend(df, atr_1, multiplier=3)
        # df = self.cci_ind.calculate_cci(df)
        # df = self.roc_ind.calculate_roc(df, 10)
        # df = self.vwap_ind.calculate_vwap(df, 50)

        df = self.rsi_ind.calculate_rsi(df, 10)
        df = self.rsi_ind.calculate_smas(df, 3, 10)

        # st_signal_1 = self.st_ind.create_signal(df, atr_1)
        # st_signal_2 = self.st_ind.create_signal(df, atr_2)
        # st_signal_3 = self.st_ind.create_signal(df, atr_3)
        # ema_signal = self.ema_ind.create_signal(df)
        # srsi_signal = self.srsi_ind.create_signal(df)
        # vbs_signal = self.volume_ind.create_bs_signal(df, 20)
        # cci_signal = self.cci_ind.create_signal(df)
        # roc_signal = self.roc_ind.create_delta_signal(df)
        # vwap_signal = self.vwap_ind.create_signal(df)

        rsi_ma_signal = self.rsi_ind.create_ma_signal(df)

        # self.signals['supertrend_12_3'] = st_signal_1
        # self.signals['supertrend_11_2'] = st_signal_2
        # self.signals['supertrend_10_1'] = st_signal_3
        # self.signals['ema'] = ema_signal
        # self.signals['srsi'] = srsi_signal
        # self.signals['volume_bs'] = vbs_signal
        # self.signals['cci'] = cci_signal

        self.signals['rsi_ma'] = rsi_ma_signal

        # self.signals['roc_delta'] = roc_signal
        # self.signals['vwap'] = vwap_signal

        return df

    def get_available_amount(self, df):
        actual_price = df['close'].iloc[-1]
        price_for_amount = actual_price + 20.0
        usdt_data = trader.data.get_balance('USDT')
        usdt_free = usdt_data['free']
        amount = usdt_free / price_for_amount
        amount = 100

        return actual_price, amount

    def decision_maker(self):

        if self.signals['rsi_ma'] == 1:

            return 'buy'

        elif self.signals['rsi_ma'] == -1:

            return 'sell'

        else:

            return 'wait'

    def trade(self, decision, price, amount):

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

        # save order
        # self.write_order(order, "Buy_")

        # write amount of coin
        self.bought_amount = amount
        self.bought_for = price

        print(self.signals)

        # notify
        self.notifier.send_message(
            f'Bought {amount} ETH for {price} $\nTime : {str(datetime.now())}')

    def sell(self, price):
        # order = self.data.create_market_sell_order('ETH/USDT', self.bought_amount)

        # self.write_order(order, "Sell_")

        self.sold_for = price

        print(self.signals)

        self.notifier.send_message(
            f'Sold {self.bought_amount} ETH for {price} $\nTime : {str(datetime.now())}')

        self.estimated_income_notifier()

    # def write_order(self, order, order_type):
    # 	path = 'trade_data/'
    # 	now = str(datetime.now())
    # 	filename = path + order_type + now + ".json"
    # 	out_file = open(filename, "w")
    # 	json.dump(order, out_file, indent = 4)
    # 	out_file.close()

    def estimated_income_notifier(self):
        # price in usdt
        buy = self.bought_for
        sell = self.sold_for
        income_pure = sell - buy
        income = income_pure * self.bought_amount
        income_rub = income * 75

        if sell > buy:
            text = f'Ммм, чувствую запах денег...\n + {income} $\n + {income_rub} Р. (примерно)'
        else:
            text = f'Ошибочка :(\n  {income} $\n  {income_rub} Р. (примерно)'

        self.notifier.send_message(text)


trader = Trader()
print('Trading now...')


def run():
    # to run on schedule

    try:

        df = trader.get_signals(50, '5m')
        print(df.tail(5))
        print(f'Time: {str(datetime.now().time())}\n  sig: {trader.signals}\n')
        price, amount = trader.get_available_amount(df)
        decision = trader.decision_maker()
        trader.trade(decision, price, amount)

    except Exception as e:
        trader.notifier.send_message("Exception in code occured:")
        trader.notifier.send_message(e)
        trader.notifier.send_message("Check exchange manually")
        print(e)
        exit()


# for 5 mins
schedule.every(5).minutes.at(":07").do(run)
# schedule.every().minute.at(":05").do(run)

while True:
    schedule.run_pending()
    time.sleep(1)

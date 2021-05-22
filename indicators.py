
from ta.volatility import AverageTrueRange
from ta.momentum import RSIIndicator, ROCIndicator, StochRSIIndicator
from ta.trend import CCIIndicator, EMAIndicator
from exchange import Data
import warnings
warnings.filterwarnings('ignore')


class SuperTrend:

    def average_true_range(self, df, atr_window=50):
        atr_ta = AverageTrueRange(df['high'], df['low'],
                                  df['close'], window=atr_window)

        name = "atr_" + str(atr_window)
        df[name] = atr_ta.average_true_range()

        return df, atr_window

    def supertrend(self, df, atr, multiplier=1):
        hl2 = (df['high'] + df['low']) / 2
        atr_name = "atr_" + str(atr)

        uband = "uband_" + str(atr)
        lband = "lband_" + str(atr)
        uptrend = "in_uptrend_" + str(atr)

        df[uband] = hl2 + (multiplier * df[atr_name])
        df[lband] = hl2 - (multiplier * df[atr_name])
        df[uptrend] = True

        for current in range(1, len(df.index)):
            previous = current - 1
            if df['close'][current] > df[uband][previous]:
                df[uptrend][current] = True
            elif df['close'][current] < df[lband][previous]:
                df[uptrend][current] = False
            else:
                df[uptrend][current] = df[uptrend][previous]

                if df[uptrend][current] and df[lband][current] < df[lband][previous]:
                    df[lband][current] = df[lband][previous]

                if not df[uptrend][current] and df[uband][current] > df[uband][previous]:
                    df[uband][current] = df[uband][previous]

        df.drop([uband, lband], axis=1, inplace=True)

        return df

    def create_signal(self, df, atr):

        uptrend = "in_uptrend_" + str(atr)

        if not df[uptrend].iloc[-2] and df[uptrend].iloc[-1]:

            # buy signal
            return 1

        if df[uptrend].iloc[-2] and not df[uptrend].iloc[-1]:

            # sell signal
            return -1

        else:
            if df[uptrend].iloc[-2] and df[uptrend].iloc[-1]:

                # (True - True) -> in a buy trend
                return 0.5

            if not df[uptrend].iloc[-2] and not df[uptrend].iloc[-1]:

                # (False - False) -> in a sell trend
                return -0.5


class CCI:

    def calculate_cci(self, df):
        cci = CCIIndicator(
            df['high'], df['low'], df['close'], window=10)
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


class RSI:

    def calculate_rsi(self, df, period):
        rsi_ind = RSIIndicator(df['close'], window=period)
        rsi = rsi_ind.rsi()
        df['rsi'] = rsi

        return df

    def calculate_smas(self, df, w1, w2):
        # short ma
        df['rsi_short'] = df['rsi'].rolling(window=w1).mean()

        # long ma
        df['rsi_long'] = df['rsi'].rolling(window=w2).mean()

        return df

    def create_ma_signal(self, df):

        s1 = df['rsi_short'].iloc[-1]
        l1 = df['rsi_long'].iloc[-1]

        s2 = df['rsi_short'].iloc[-1]
        l2 = df['rsi_long'].iloc[-1]

        uptrend = self.average_trend(df)

        # cross down -> sell
        if s2 > l2 and s1 < l1:
            return -1

        elif uptrend == True and s1 > l1 and s2 < l2:
            return 1

        else:
            return 0

    def average_trend(self, df):

        previous = df['rsi_long'].iloc[-11:-6]
        now = df['rsi_long'].iloc[-5:-1]

        print(f' PRev sum : {previous.sum()}')
        print(f' Now sum : {now.sum()}')

        if previous.sum() > now.sum():
            return False
        else:
            return True


class ROC:

    def calculate_roc(self, df, window):

        roc = ROCIndicator(df['close'], window=window)
        df['roc'] = roc.roc()

        return df

    def create_delta_signal(self, df):

        treshold = 1
        delta = df['roc'].iloc[-1] - df['roc'].iloc[-2]

        if delta > treshold:
            return 1
        else:
            return -1


class S_RSI:

    def calculate(self, df, window, sm1, sm2):

        srsi = StochRSIIndicator(
            df['close'], window=14, smooth1=sm1, smooth2=sm2)
        df['s_rsi_d'] = srsi.stochrsi_d()
        df['s_rsi_k'] = srsi.stochrsi_k()

        return df

    def create_signal(self, df):
        ob_level = 0.80
        os_level = 0.20

        d = df['s_rsi_d'].iloc[-1]
        k = df['s_rsi_k'].iloc[-1]

        d2 = df['s_rsi_d'].iloc[-2]
        k2 = df['s_rsi_k'].iloc[-2]

        # k must cross d -> cross from above
        if d > ob_level and k > ob_level and k2 > d2 and k1 < d1:

            return -1

        elif d < os_level and k < os_level and k2 < d2 and k1 > d1:

            return 1

        else:
            return 0


class EMA:

    def calculate(self, df, window):
        ema = EMAIndicator(df['close'], window=window)

        df['ema'] = ema.ema_indicator()

        return df

    def create_signal(self, df):

        if df['close'].iloc[-1] > df['ema'].iloc[-1]:
            return 1

        else:
            return -1

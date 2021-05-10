
import warnings
warnings.filterwarnings('ignore')

import config 
from exchange import Data

import numpy as np
import pandas as pd

from sklearn.preprocessing import MinMaxScaler

import keras
from keras.models import Sequential
from keras.layers import Dense, SimpleRNN, GRU
from keras.optimizers import SGD
from keras.layers import Dropout
from keras.metrics import MeanSquaredError

class GRU_model:

	def __init__(self, path):
		self.path = path
		self.model = keras.models.load_model(self.path)

	def get_closes(self):
		data = Data()
		df = data.get_candle_data(period=60, timeframe='5m')
		df = df[['close']]

		return df

	def prepare_dataset(self, df):
		# copied from training session 
		ts_test = df.values
		sc = MinMaxScaler(feature_range=(0, 1))
		inputs = ts_test.reshape(-1, 1) 
		inputs  = sc.fit_transform(inputs)
		X_test = np.reshape(inputs, (1, inputs.shape[0], inputs.shape[1]))

		return X_test, sc

	def evaluate(self, X_test, sc):
		predictions = self.model.predict(X_test)
		predictions = sc.inverse_transform(predictions)

		return predictions 

	def create_signal(self, df, predictions):
		last_pred = predictions[-1][-1]

		if last_pred  > df['close'].iloc[-1]:

			return 1

		else: 

			return -1

gru = GRU_model('models/ethusdt5m_5.h5')
df = gru.get_closes()
X_test, scaler = gru.prepare_dataset(df)
preds = gru.evaluate(X_test, scaler)
signal = gru.create_signal(df, preds)
print(df.tail(5))
print(f'Preds : {preds}')
print(f'signal : {signal}')



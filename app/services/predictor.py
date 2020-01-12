from .. import logger
import os
import numpy as np
import tensorflow as tf
from tensorflow import keras
import pandas as pd
import seaborn as sns
from pylab import rcParams
import matplotlib.pyplot as plt
from matplotlib import rc
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.layers import Bidirectional, Dropout, Activation, Dense, LSTM
from tensorflow.python.keras.layers import CuDNNLSTM
from tensorflow.keras.models import Sequential

RANDOM_SEED = 42

def by_weeks(weeks):
  days = {
    'date': [],
    'contributions': []
  }
  for week in weeks:
    for day in week['contributionDays']:
      days['date'].append(day['date'])
      days['contributions'].append(day['contributionCount'])

  logger.info(days)
  
  # np.random.seed(RANDOM_SEED)

  # df = pd.DataFrame.from_dict(days, parse_dates=['date'])
  # df = df.sort_values('date')

  # app.logger.info(df.shape())

  # # Normalization
  # scaler = MinMaxScaler()
  # close_price = df.Close.values.reshape(-1, 1)
  # scaled_close = scaler.fit_transform(close_price)

  # app.logger.info(np.isnan(scaled_close).any())

  # scaled_close = scaled_close[~np.isnan(scaled_close)]
  # scaled_close = scaled_close.reshape(-1, 1)

  # app.logger.info(np.isnan(scaled_close).any())

  # Preprocessing

  return days

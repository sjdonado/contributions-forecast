from .. import logger
import os
import numpy as np
import pandas as pd
import seaborn as sns
import tensorflow as tf
import matplotlib.pyplot as plt
from tensorflow import keras
from pylab import rcParams
from matplotlib import rc
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.layers import Bidirectional, Dropout, Activation, Dense, LSTM
from tensorflow.keras.models import Sequential

tf.config.optimizer.set_jit(True)

RANDOM_SEED = 42

# Preprocessing
SEQ_LEN = 8

# Model
DROPOUT = 0.2
WINDOW_SIZE = SEQ_LEN - 1

# Training
EPOCHS = 30
BATCH_SIZE = 16

def to_sequences(data, seq_len):
  d = []
  for index in range(len(data) - seq_len):
    d.append(data[index: index + seq_len])

  return np.array(d)

def preprocess(data_raw, seq_len, train_split):
  data = to_sequences(data_raw, seq_len)
  num_train = int(train_split * data.shape[0])

  X_train = data[:num_train, :-1, :]
  y_train = data[:num_train, -1, :]

  X_test = data[num_train:, :-1, :]
  y_test = data[num_train:, -1, :]

  return X_train, y_train, X_test, y_test

def execute(weeks):
  np.random.seed(RANDOM_SEED)

  # Parsing data
  contributions = []
  for week in weeks:
    for day in week['contributionDays']:
      contributions.append(day['contributionCount'])

  days = np.arange(0, len(contributions), 1)
  df = pd.DataFrame(dict(contributions=contributions), index=days, columns=['contributions'])
  # df = df.sort_values('Date')

  # logger.info(df.shape)

  # Normalization
  scaler = MinMaxScaler()
  contributions = df.contributions.values.reshape(-1, 1)
  scaled_contributions = scaler.fit_transform(contributions)

  # logger.info(np.isnan(scaled_contributions).any())

  # scaled_contributions = scaled_contributions[~np.isnan(scaled_contributions)]
  # scaled_contributions = scaled_contributions.reshape(-1, 1)

  # logger.info(np.isnan(scaled_contributions).any())

  # Preprocessing
  X_train, y_train, X_test, y_test = preprocess(scaled_contributions, SEQ_LEN, train_split = 0.98)

  # logger.info(y_test)
  # logger.info(X_train.shape)
  # logger.info(X_test.shape)

  # Model
  model = keras.Sequential()

  model.add(Bidirectional(LSTM(WINDOW_SIZE, return_sequences = True, activation='tanh', recurrent_activation='sigmoid'),
                          input_shape = (WINDOW_SIZE, X_train.shape[-1])))
  model.add(Dropout(rate = DROPOUT))

  model.add(Bidirectional(LSTM((WINDOW_SIZE * 2), return_sequences = True, activation='tanh', recurrent_activation='sigmoid')))
  model.add(Dropout(rate = DROPOUT))

  model.add(Bidirectional(LSTM(WINDOW_SIZE, return_sequences = False)))

  model.add(Dense(units = 1))

  model.add(Activation('linear'))

  # Training
  model.compile(
    loss = 'mean_squared_error', 
    optimizer = 'adam'
  )

  model.fit(
    X_train, 
    y_train, 
    epochs = EPOCHS, 
    batch_size = BATCH_SIZE, 
    shuffle = False,
    validation_split = 0.1
  )

  model.evaluate(X_test, y_test)

  # Prediction
  y_hat = model.predict(X_test)
  y_hat_inverse = scaler.inverse_transform(y_hat)

  return y_hat_inverse.tolist()

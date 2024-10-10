from utils import *
import time
import numpy as np
import pandas as pd
import datetime
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
import math
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler
import xgboost as xgb
from sklearn.metrics import accuracy_score
import warnings
warnings.filterwarnings("ignore")


start = '2022-09-27'
end = '2023-01-01'

tickers = ['MSFT']
thelen = len(tickers)


price_data = []
for ticker in tickers:
    data = yf.download(ticker, start, end)
    data = data.reset_index()
    prices = data.loc[:,['Date','Adj Close']]
    price_data.append(prices.assign(ticker=ticker)[['ticker', 'Date', 'Adj Close']])
data = pd.concat(price_data)

data = data.reset_index()
data

data.dtypes


# re-name field from 'Adj Close' to 'Adj_Close'
data = data.rename(columns={"Adj Close": "Adj_Close"})
data


data = data.loc[:,['Date','Adj_Close']]
       

# Plot all the close prices
# ((data.pct_change()+1).cumprod()).plot(figsize=(10, 7))


plt.figure(figsize=(14, 5), dpi=100)
plt.plot(data['Date'], data['Adj_Close'], label='Starbucks Stock Price')
plt.xlabel('Date')
plt.ylabel('USD')
plt.title('Figure 2: Starbucks Stock Price')
plt.legend()
plt.show()


num_training_days = int(data.shape[0]*.7)
print('Number of training days: {}. Number of test days: {}.'.format(num_training_days, data.shape[0]-num_training_days))


# TECHNICAL INDICATORS
#def get_technical_indicators(dataset):
# Create 7 and 21 days Moving Average
data['ma7'] = data['Adj_Close'].rolling(window=7).mean()
data['ma21'] = data['Adj_Close'].rolling(window=21).mean()


# Create exponential weighted moving average
data['26ema'] = data['Adj_Close'].ewm(span=26).mean()
data['12ema'] = data['Adj_Close'].ewm(span=12).mean()
data['MACD'] = (data['12ema']-data['26ema'])

# Create Bollinger Bands
data['20sd'] = data['Adj_Close'].rolling(window=20).std() 
data['upper_band'] = data['ma21'] + (data['20sd']*2)
data['lower_band'] = data['ma21'] - (data['20sd']*2)

# Create Exponential moving average
data['ema'] = data['Adj_Close'].ewm(com=0.5).mean()

# Create Momentum
data['momentum'] = data['Adj_Close']-1
    

dataset_TI_df = data
dataset = data


def plot_technical_indicators(dataset, last_days):
    plt.figure(figsize=(16, 10), dpi=100)
    shape_0 = dataset.shape[0]
    xmacd_ = shape_0-last_days
    
    dataset = dataset.iloc[-last_days:, :]
    x_ = range(3, dataset.shape[0])
    x_ =list(dataset.index)
    
    # Plot first subplot
    plt.subplot(2, 1, 1)
    plt.plot(dataset['ma7'],label='MA 7', color='g',linestyle='--')
    plt.plot(dataset['Adj_Close'],label='Closing Price', color='b')
    plt.plot(dataset['ma21'],label='MA 21', color='r',linestyle='--')
    plt.plot(dataset['upper_band'],label='Upper Band', color='c')
    plt.plot(dataset['lower_band'],label='Lower Band', color='c')
    plt.fill_between(x_, dataset['lower_band'], dataset['upper_band'], alpha=0.35)
    plt.title('Technical indicators for Starbucks - last {} days.'.format(last_days))
    plt.legend()

    # Plot second subplot
    plt.subplot(2, 1, 2)
    plt.title('MACD')
    plt.plot(dataset['MACD'],label='MACD', linestyle='-.')
    plt.hlines(15, xmacd_, shape_0, colors='g', linestyles='--')
    plt.hlines(-15, xmacd_, shape_0, colors='g', linestyles='--')
    # plt.plot(dataset['log_momentum'],label='Momentum', color='b',linestyle='-')

    plt.legend()
    plt.show()

plot_technical_indicators(dataset_TI_df, 250)
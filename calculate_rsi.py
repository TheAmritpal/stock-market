import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
# ticker_symbol = "^NSEBANK"
# ticker_symbol = input("Enter YFinance Ticker Name: ")
ticker_symbol = "OLAELEC.NS"

if ticker_symbol == "":
    print('Stock Name is required')
    exit(1)

# Specify the date range
# start_date = input("Enter Start Date (yyyy-mm-dd): ")
start_date = "2024-10-08"

if start_date == "":
    print('Start date is required')
    exit(1)    

# end_date = input("Enter End Date (yyyy-mm-dd): ")
end_date = "2024-10-09"

if end_date == "":
    print('End Date is required')
    exit(1)

# interval = input("Enter Interval: ")
interval = "1m"

if interval == "":
    print('Interval is required')
    exit(1)

# Fetch the data
data = yf.download(ticker_symbol, start=start_date, end=end_date, interval=interval)

Open = []
Close = []
Datetime = []
High = []
Low = []
Adj_close = []
Volume = []
Gain = []
Loss = []

def addCustomData(data, gain, loss):
    Open.append(data['Open'])
    Close.append(data['Close'])
    Datetime.append(data['Datetime'])
    High.append(data['High'])
    Low.append(data['Low'])
    Adj_close.append(data['Adj_close'])
    Volume.append(data['Volume'])
    Gain.append(gain)
    Loss.append(loss)

for i in range(len(data.index)):
    dist = {
        'Open': data.at[data.index[i], 'Open'],
        'Close': data.at[data.index[i], 'Close'],
        'Datetime': data.index[i],
        'High': data.at[data.index[i], 'High'],
        'Low': data.at[data.index[i], 'Low'],
        'Adj_close': data.at[data.index[i], 'Adj Close'],
        'Volume': data.at[data.index[i], 'Volume'],
    }
    
    if i == 0:
        addCustomData(dist, 0, 0)
        continue
    
    previousClose = data.at[data.index[i - 1], 'Open']
    
    if dist['Close'] >= previousClose:
        addCustomData(dist, dist['Close'] - previousClose, 0)
    elif dist['Close'] < previousClose:
        addCustomData(dist, 0, previousClose - dist['Close'])
    else:
        addCustomData(dist, 0, 0)

dict = {'Datetime': Datetime, 'Open': Open, 'Close': Close, 'High': High, 'Low': Low, 'Adj Close': Adj_close, 'Volume': Volume, 'Gain': Gain, 'Loss': Loss} 

df = pd.DataFrame(dict)
   
def get_average_gains(df, period):
    for i in range(len(df)):
        n, up, down = 0, 0, 0
        if i == period:
            while n < period:
                if df.iloc[i-n]['Gain'] > 0:
                    up += df.iloc[i-n]['Gain']
                elif df.iloc[i-n]['Loss'] > 0:
                    down += df.iloc[i-n]['Loss']
                else:
                    up += 0
                    down += 0
                n += 1
            df.at[i, 'Average Gain'] = up/period
            df.at[i, 'Average Loss'] = down/period
        elif i > period:
            df.at[i, 'Average Gain'] = (df.iloc[i-1]['Average Gain'] * (period - 1) + df.iloc[i]['Gain'])/period
            df.at[i, 'Average Loss'] = (df.iloc[i-1]['Average Loss'] * (period - 1) + df.iloc[i]['Loss'])/period
            df['Average Gain'] = df['Average Gain'].fillna(0)
            df['Average Loss'] = df['Average Loss'].fillna(0)
    return df

def get_relative_strength(df, period):
    for i in range(len(df)):
        if i >= period:
            df.at[i, 'Relative Strength'] = df.iloc[i]['Average Gain']/df.iloc[i]['Average Loss']
            df.at[i, 'Relative Strength Index'] = (100-(100/(1+df.iloc[i]['Relative Strength'])))
    return df

df = get_average_gains(df, 14)
df = get_relative_strength(df, 14)

# if df is not None:
#     df.to_csv("banknifty_data_with_rsi.csv")
#     print("Data saved to banknifty_data_with_rsi.csv")

def chart_rsi(ticker, df):
    plt.figure()
    fig, ax = plt.subplots()
    ax.set_title(ticker)
    fig.subplots_adjust(bottom=0.2)
    ax.plot(df.index, df['Relative Strength Index'])
    ax.set_ylim(0, 100)
    ax.axhline(y=70, color='r', linestyle='-')
    ax.axhline(y=30, color='r', linestyle='-')
    ax.grid(True)
    ax.set_ylabel(r'RSI')
    for label in ax.get_xticklabels(which='major'):
        label.set(rotation=30, horizontalalignment='right')
    plt.show()
    
chart_rsi(ticker_symbol, df)
import yfinance as yf

# ticker_symbol = "^NSEBANK"
ticker_symbol = "OLAELEC.NS"

def get_banknifty_data(start_date, end_date):
    try:
        banknifty_data = yf.download(ticker_symbol, start=start_date, end=end_date, interval="1m")
        
        print(f"Downloaded {len(banknifty_data)} rows of data.")
        return banknifty_data
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Specify the date range
start_date = "2024-10-01"
end_date = "2024-10-04"

# Fetch the data
data = get_banknifty_data(start_date, end_date)
print(data)
# Save to a CSV file if data is available
# if data is not None:
#     data.to_csv("banknifty_data.csv")
#     print("Data saved to banknifty_data.csv")


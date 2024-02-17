import datetime
from pandas_datareader import data as pdr
import yfinance as yfin
import matplotlib.pyplot as plt


end_time = datetime.datetime.now()
start_time = end_time - datetime.timedelta(days=365)

yfin.pdr_override()

df = pdr.get_data_yahoo('^GSPC', start=start_time.strftime('%Y-%m-%d'), end=end_time.strftime('%Y-%m-%d'))
df.reset_index(inplace=True)
df.set_index("Date", inplace=True)

print(df.head())
# Adjusted Close takes dividends, stock splits and new stock offerings into account
df['Adj Close'].plot()
plt.show()

#high low average between time period
highest = max(df['High'])
lowest = min(df['Low'])
avg_high = sum(df['High']) / len(df['High'])
avg_low = sum(df['Low']) / len(df['Low'])
avg_adj_close = sum(df['Adj Close']) / len(df['Adj Close'])

print(f"{highest=} {lowest=} {avg_high=} {avg_low=} {avg_adj_close=}")


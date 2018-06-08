# alpha_vantage_downloader

An simple wrapper around Alpha Vantage financial data API. Multithreaded call
is implemented in calling Alpha Vantage API to speed up downloading process when
downloading multiple security data.  

Currently only support downloading equity data.

## Install

```
$ pip install alpha_vantage_downloader
```

## Usage

```
from alpha_vantage_downloader.downloader import downloader

# supply your api key to intialize an instance, 
# wait_time is the number of seconds in between each API call
worker = downloader(key='your-api-key-here', wait_time=0.5)   
tickers = ['AAPL', 'MSFT']

daily_price = worker.daily(tickers)
type(daily_price)      # print out dict
daily_price.keys()     # print out dict_keys(['AAPL', 'MSFT'])
daily_price['AAPL']    # print out the daily price dataframe from calling daily price API

```

## Supported Methods

```
worker.daily(tickers)           # daily price
worker.adjusted_daily(tickers)  # adjusted daily price
worker.weekly(tickers)          # weekly price
worker.adjusted_weekly(tickers) # adjusted weekly price

worker.intraday(symbols=tickers, granularity='1min')   # supports the granularity listed on alpha vantage doc page

```
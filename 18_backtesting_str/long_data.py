api_key='PKCGQ99MC5FQA1P8ZSRE'
secret_key='rkWLI1F2poiTbuERdzozfOLgVV6mrFKTH27Ugvb1'
from alpaca.data.historical.stock import StockHistoricalDataClient

# setup stock historical data client
stock_historical_data_client = StockHistoricalDataClient(api_key, secret_key)

from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame, TimeFrameUnit
import pendulum as dt
timez_zone="America/New_York"
current_time=dt.now(tz=timez_zone)
print(current_time)
import time

ct=time.time()
req = StockBarsRequest(
    symbol_or_symbols = 'AMZN',
    timeframe=TimeFrame(amount = 1, unit = TimeFrameUnit.Minute), # specify timeframe
    start = current_time-dt.duration(days=500),                          # specify start datetime, default=the beginning of the current day.
    end_date=current_time,                                        # specify end datetime, default=now
    # limit = 2,                                               # specify limit
)

history1=stock_historical_data_client.get_stock_bars(req).df
history1.to_csv('AMZN.csv')
print('time taken',time.time()-ct)


# from alpaca.data.historical.crypto import CryptoHistoricalDataClient
# from alpaca.data.requests import CryptoBarsRequest
# from alpaca.data.timeframe import TimeFrame, TimeFrameUnit

# crypto_historical_data_client = CryptoHistoricalDataClient()
# req = CryptoBarsRequest(
#     symbol_or_symbols = 'ETH/USD',
#     timeframe=TimeFrame(amount = 1, unit = TimeFrameUnit.Day), # specify timeframe
#     start = dt.datetime(2024,1,1,1,1,1,tz=timez_zone),                          # specify start datetime, default=the beginning of the current day.
#     end=dt.datetime(2024,12,30,1,1,1,tz=timez_zone),                                        # specify end datetime, default=now
#     # limit = 2,                                               # specify limit
# )

# history_df2=crypto_historical_data_client.get_crypto_bars(req).df
# history_df2

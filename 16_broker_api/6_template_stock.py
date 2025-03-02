

import pendulum as dt
import pandas as pd
from datetime import datetime,timedelta

import time
import logging
import pandas_ta as ta


from alpaca.trading.requests import GetOrdersRequest,MarketOrderRequest
from alpaca.trading.enums import OrderSide, QueryOrderStatus,TimeInForce
from zoneinfo import ZoneInfo
from alpaca.data.timeframe import TimeFrame, TimeFrameUnit
from alpaca.data.historical.stock import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest

from alpaca.trading.client import TradingClient
from credentials import api_key,secret_key
trading_client = TradingClient(api_key, secret_key, paper=True)

list_of_tickers=["TSLA","AMZN"]
time_zone='America/New_York'
strategy_name='crypto_sma'
logging.basicConfig(level=logging.INFO, filename=f'{strategy_name}_{dt.now(tz=time_zone).date()}.log',filemode='a',format="%(asctime)s - %(message)s")
logging.info(f'starting {strategy_name} strategy file')








def get_historical_crypto_data(ticker,duration,time_frame_unit):
    # setup stock historical data client
    stock_historical_data_client = StockHistoricalDataClient(api_key, secret_key)
    current_time=dt.now(tz=time_zone)
   
    req = StockBarsRequest(
        symbol_or_symbols = ticker,
        timeframe=TimeFrame(amount = 1, unit = time_frame_unit), # specify timeframe
        start = current_time-dt.duration(days=duration),                          # specify start datetime, default=the beginning of the current day.
        # end_date=current_time-dt.duration(days=10),                                        # specify end datetime, default=now
        # limit = 2,                                               # specify limit
    )

    history_df1=stock_historical_data_client.get_stock_bars(req).df
    sdata=history_df1.reset_index().drop('symbol',axis=1)
    sdata['timestamp']=sdata['timestamp'].dt.tz_convert('America/New_York')
    sdata=sdata.set_index('timestamp')
    sdata['ema']=ta.ema(sdata['close'],length=10)
    sdata['super']=ta.supertrend(sdata.high,sdata.low,sdata.close,length=10)['SUPERTd_10_3.0']
    sdata['atr']=ta.atr(sdata.high, sdata.low, sdata.close, length=14)
    return sdata

# print(dt.now(tz=time_zone))
# df=get_historical_crypto_data('TSLA',10,TimeFrameUnit.Minute)
# print(df)


def get_all_open_orders():
    # params to filter orders by
    request_params = GetOrdersRequest(
                        status=QueryOrderStatus.OPEN
                    )

    # orders that satisfy params
    orders = trading_client.get_orders(filter=request_params)
    new_order=[]
    for elem in orders:
        new_order.append(dict(elem))

    order_df=pd.DataFrame(new_order)
    order_df.to_csv('orders.csv')
    l=[i for i in list_of_tickers]
    order_df=order_df[order_df['symbol'].isin(l)]
    return order_df

def get_all_position():

    pos=trading_client.get_all_positions()
    new_pos=[]
    for elem in pos:
        new_pos.append(dict(elem))

    pos_df=pd.DataFrame(new_pos)
    pos_df.to_csv('pos.csv')
    # filter pos that are in list_of_tickers
    l=[i.replace("/","") for i in list_of_tickers]
    pos_df=pos_df[pos_df['symbol'].str.replace('/','').isin(l)]
    return pos_df

pos_df=get_all_position()
print(pos_df)

ord_df=get_all_open_orders()
print(ord_df)



def close_this_position(ticker_name):
    ticker_name=ticker_name.replace('/','')
    print(ticker_name)
    try:
        # p = trading_client.get_open_position(ticker_name)
        # print(p)
        c=trading_client.close_position(ticker_name)
        print(c)
        print('position closed')
    except:
        print('position does not exist')

def close_this_order(tickera_name):
    try:
        for i in trading_client.get_orders():
            if i.symbol==tickera_name:
                id1=i.id
        trading_client.cancel_order_by_id(id1)
    except:
        print('order does not exist')

close_this_position('TSLA')
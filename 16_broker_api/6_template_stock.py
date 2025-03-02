

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
strategy_name='stock_sma'
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
    sdata['sma_20']=ta.sma(sdata['close'],length=20)
    sdata['sma_50']=ta.sma(sdata['close'],length=50)
    return sdata

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

def close_all_position():
    #close everything
    for ticker1 in list_of_tickers:
        close_this_position(ticker1)
        print('position closed for ',ticker1)

def close_all_orders():
    #close all open orders
    for ticker1 in list_of_tickers:
        close_this_order(ticker1)
        print('order closed for ',ticker1)

def trade_buy_stocks(ticker,closing_price):

    print('placing market order')
    # preparing orders

    market_order_data = MarketOrderRequest(
                        symbol=ticker,
                        qty=1,
                        side=OrderSide.BUY,
                        time_in_force=TimeInForce.DAY
                        )

    # Market order
    market_order = trading_client.submit_order(
                    order_data=market_order_data
                )
    market_order
    print(market_order)
    print('done placing market order buy for ',ticker)

def trade_sell_stocks(ticker,closing_price):
    print('placing market order')
    # preparing orders

    market_order_data = MarketOrderRequest(
                        symbol=ticker,
                        qty=1,
                        side=OrderSide.SELL,
                        time_in_force=TimeInForce.DAY
                        )

    # Market order
    market_order = trading_client.submit_order(
                    order_data=market_order_data
                )
    market_order
    print(market_order)
    print('done placing market order sell for ',ticker)

def strategy(hist_df,ticker):
    print('inside strategy conditional code ')
    # print(hist_df)
    print(ticker)
    buy_condition=(hist_df['sma_20'].iloc[-1]>hist_df['sma_50'].iloc[-1]) and (hist_df['sma_20'].iloc[-2]<hist_df['sma_50'].iloc[-2])
    sell_condition=(hist_df['sma_20'].iloc[-1]<hist_df['sma_50'].iloc[-1]) and (hist_df['sma_20'].iloc[-2]>hist_df['sma_50'].iloc[-2])
                
    money=float(trading_client.get_account().cash)
    money=money/3
    print(money)
    closing_price=hist_df['close'].iloc[-1]
    if money>closing_price:
        if buy_condition:
            print('buy condition satisfied')
            trade_buy_stocks(ticker,closing_price)
        if sell_condition:
            print('sell conditoin satisfied')
            trade_sell_stocks(ticker,closing_price)
        else:
            print('no condition satisfied')
    else:
        print('we dont have enough money to trade')



def main_strategy_code():
    print('we are running strategy ')
    ord_df=get_all_open_orders()
    pos_df=get_all_position()
    print(ord_df)
    print(pos_df)

    for ticker in list_of_tickers:
        print(ticker)
        #fetch historical data and indicators
        hist_df=get_historical_crypto_data(ticker,2,TimeFrameUnit.Minute)
        print(hist_df)

        money=float(trading_client.get_account().cash)
        money=money/3
        print(money)
        ltp=hist_df['close'].iloc[-1]
        print(ltp)
        quantity=money//ltp
        print(quantity)

        if quantity==0:
            continue
        
        if pos_df.empty:
            print('we dont have any position')
            strategy(hist_df,ticker)

        elif len(pos_df)!=0 and ticker.replace('/','') not in pos_df['symbol'].to_list():
            print('we have some position but ticker is not in pos')
            strategy(hist_df,ticker)

        elif len(pos_df)!=0 and ticker.replace('/','')  in pos_df['symbol'].to_list():
            print('we have some pos and ticker is in pos')
            curr_quant=float(pos_df[pos_df['symbol']==ticker.replace('/','')]['qty'].iloc[-1])
            print(curr_quant)

            if curr_quant==0:
                print('my quantity is 0')
                strategy(hist_df,ticker)
            elif curr_quant>0:
                print('we are already long')
                sell_condition=(hist_df['sma_20'].iloc[-1]<hist_df['sma_50'].iloc[-1]) and (hist_df['sma_20'].iloc[-2]>hist_df['sma_50'].iloc[-2])
                if sell_condition:
                    print('sell condition is satisfied ')
                    close_this_position(ticker.replace('/',''))
                    trade_sell_stocks(ticker,ltp)

                else:
                    print('sell condition not satisfied')
            elif curr_quant<0:
                print('we are already short')
                buy_condition=(hist_df['sma_20'].iloc[-1]>hist_df['sma_50'].iloc[-1]) and (hist_df['sma_20'].iloc[-2]<hist_df['sma_50'].iloc[-2])
                if buy_condition:
                    print('buy condition is satisfied ')
                    close_this_position(ticker.replace('/',''))
                    trade_buy_stocks(ticker,ltp)
                else:
                    print('buy condition not satisfied')




current_time=dt.now(tz=time_zone)
print(current_time)

start_hour,start_min=4,36
end_hour,end_min=5,30

start_time=dt.datetime(current_time.year,current_time.month,current_time.day,start_hour,start_min,tz=time_zone)
end_time=dt.datetime(current_time.year,current_time.month,current_time.day,end_hour,end_min,tz=time_zone)

print(start_time)
print(end_time)

#this code will execute before the start time
while dt.now(tz=time_zone)<start_time:
    print(dt.now(tz=time_zone))
    time.sleep(1)
print('we have reached start time')



while True:
    if dt.now(tz=time_zone)>end_time:
        break
    ct=dt.now(tz=time_zone)
    print(ct)
    
    if ct.second==2: #and ct.minute in range(0,60,5):#[0,5,10,15..55]
        main_strategy_code()
    time.sleep(1)
print('strategy stopped')

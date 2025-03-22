
# Supertrend and EMA Strategy
# Calculate the Supertrend on daily candles.
# Calculate the EMA (Exponential Moving Average) on hourly candles.
# Go Long:When the daily Supertrend gives a long signal and the closing price is greater than the hourly EMA.
# Go Short:When the daily Supertrend gives a short signal.The closing price is less than the hourly EMA.


from credentials import api_key,secret_key
from alpaca.data.historical.stock import StockHistoricalDataClient
import pendulum as dt
import pandas as pd
import pandas_ta as ta
import time
import logging


from datetime import datetime,timedelta
from zoneinfo import ZoneInfo
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame, TimeFrameUnit

from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.requests import StopOrderRequest

from alpaca.trading.client import TradingClient
from alpaca.trading.requests import GetOrdersRequest
from alpaca.trading.enums import OrderSide, QueryOrderStatus,TimeInForce

api_key='PKCGQ99MC5FQA1P8ZSRE'
secret_key='rkWLI1F2poiTbuERdzozfOLgVV6mrFKTH27Ugvb1'
list_of_tickers=['TSLA','AMZN','GOOG','NVDA','AAPL','MSFT','NFLX','AMD']


#timframe is 1 min
time_frame=1
time_frame_unit=TimeFrameUnit.Minute
days=20
start_hour,start_min=9,30
end_hour,end_min=15,45
time_zone='America/New_York'
strategy_name='supertrend_ema_strategy'
stop_perc=1


#logging to file
logging.basicConfig(level=logging.INFO, filename=f'{strategy_name}_{dt.now(time_zone).date()}.log',filemode='a',format="%(asctime)s - %(message)s")


trading_client = TradingClient(api_key, secret_key, paper=True)
# setup stock historical data client
stock_historical_data_client = StockHistoricalDataClient(api_key, secret_key)





def get_historical_stock_data(ticker,duration,time_frame_unit):
    """extracts historical data and outputs in the form of dataframe"""
    now = datetime.now(ZoneInfo("America/New_York"))
    req = StockBarsRequest(
        symbol_or_symbols = ticker,
        timeframe=TimeFrame(amount = 1, unit = time_frame_unit), # specify timeframe
        start = now - timedelta(days = duration),                          # specify start datetime, default=the beginning of the current day.
        # end_date=None,                                        # specify end datetime, default=now
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

def get_open_position():

    pos=trading_client.get_all_positions()
    new_pos=[]
    for elem in pos:
        new_pos.append(dict(elem))

    pos_df=pd.DataFrame(new_pos)
    #filter pos that are in list_of_tickers
    pos_df=pos_df[pos_df['symbol'].isin(list_of_tickers)]
    return pos_df

def get_open_orders():
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
    #filter orders that are in list_of_tickers
    if not order_df.empty:
        order_df=order_df[order_df['symbol'].isin(list_of_tickers)]
    return order_df




def close_this_stock_position(ticker_name):
    try:
        position = trading_client.get_open_position(ticker_name)
        print(position)
        logging.info(f'Closing position for {ticker_name}')
        c=trading_client.close_position(ticker_name)
        print(c)
        print('position closed')
    except:
        print('position does not exist')

def close_this_order_for_stock(ticker_name):
    order_df=get_open_orders()
    if not order_df.empty:
        order_df=order_df[order_df['symbol']==ticker_name]
        print(order_df)
        if not order_df.empty:
            for id in order_df['id'].to_list():
                try:
                    logging.info(f'Closing order for {ticker_name}')
                    response = trading_client.cancel_order_by_id(id)
                    print(response)
                except:
                    print('order does not exist',ticker_name)
                

def check_market_order_placed(ticker):
    order_df=get_open_orders()
    if not order_df.empty:
        order_df=order_df[order_df['order_type']=='market']
        if not order_df.empty and (ticker in order_df['symbol'].to_list()):
            return 0
        else:
            return 1
    else:
        return 1



def trade_sell_stocks(symbol,stock_price,stop_price,quantity=1):
    logging.info(f'Selling {quantity} of {symbol} at {stock_price}')
    if check_market_order_placed(symbol):

        market_order_data = MarketOrderRequest(
                            symbol=symbol,
                            qty=quantity,
                            side=OrderSide.SELL,
                            time_in_force=TimeInForce.GTC
                            )

        # Market order
        market_order = trading_client.submit_order(
                        order_data=market_order_data
                    )
        print(market_order)





def trade_buy_stocks(symbol,stock_price,stop_price,quantity=1):
    logging.info(f'Buying {quantity} of {symbol} at {stock_price}')

    if check_market_order_placed(symbol):

        market_order_data = MarketOrderRequest(
                            symbol=symbol,
                            qty=quantity,
                            side=OrderSide.BUY,
                            time_in_force=TimeInForce.GTC
                            )

        # Market order
        market_order = trading_client.submit_order(
                        order_data=market_order_data
                    )
        print(market_order)



def place_stop_order_stock(symbol,stop_price,quantity,side):
    logging.info(f'Placing stop order for {quantity} of {symbol} at {stop_price}')
    print('placing stop order')
    stop_order_data=StopOrderRequest(
                        symbol=symbol,
                        stop_price=int(stop_price),
                        qty=quantity,
                        side=side,
                        time_in_force=TimeInForce.DAY
    )

    stop_market_order = trading_client.submit_order(
                    order_data=stop_order_data
                )
    print(stop_market_order)


def check_and_place_stop_order(pos_df,order_df):

        if not pos_df.empty:
            l1=pos_df['symbol'].to_list()
            #common stock in l1 and list_of_tickers
            l1=list(set(l1).intersection(set(list_of_tickers)))
            for ticker in l1:
                #check if stop order exist
                try:
                        t=trading_client.get_open_position(ticker)
                        buy_price=float(t.avg_entry_price)
                        quantity=abs(int(t.qty))
                        s=t.side
                        if s==OrderSide.BUY:
                            s=OrderSide.SELL
                            stop_price=buy_price-buy_price*(1-(stop_perc/100))
                        else:
                            s=OrderSide.BUY
                            stop_price=buy_price+buy_price*(1-(stop_perc/100))
                        if order_df.empty or (ticker not in order_df['symbol'].to_list()):
                            place_stop_order_stock(ticker,stop_price,quantity,s)
                        print('stop order already placed')
                except Exception as e:
                    print(e)
                    print('stop order cannot be placed')
                    logging.info(f'Stop order cannot be placed for {ticker}')


def strategy_condition(hist_df_hourly,hist_df_daily,ticker):
    print('inside strategy conditional code ')
    # print(hist_df)
    print(ticker)
    buy_condition=hist_df_hourly['super'].iloc[-1]>0 and hist_df_daily['ema'].iloc[-1]<hist_df_hourly['close'].iloc[-1]
    # buy_condition=True
    sell_condition=hist_df_hourly['super'].iloc[-1]<0 and hist_df_daily['ema'].iloc[-1]>hist_df_hourly['close'].iloc[-1]
    # sell_condition=True


    hourly_closing_price=hist_df_hourly['close'].iloc[-1]
    atr_value=hist_df_daily['atr'].iloc[-1]

    if buy_condition:
        print('buy condition satisfied')
        trade_buy_stocks(ticker,hourly_closing_price,hourly_closing_price-atr_value)
    elif sell_condition:
        print('sell condition satisfied')
        trade_sell_stocks(ticker,hourly_closing_price,hourly_closing_price+atr_value)
    else:
        print('no condition satisfied')

def main_strategy():
    pos_df= get_open_position()
    ord_df= get_open_orders()
    print(pos_df)
    print(ord_df)
    ord_df.to_csv('orders.csv')

    for ticker in list_of_tickers:
        print(ticker)
        #historical data with indicator data
        hist_df=get_historical_stock_data(ticker,days,time_frame_unit)
        print(hist_df)
        hist_df_hourly=get_historical_stock_data(ticker,10,TimeFrameUnit.Hour)
        hist_df_daily=get_historical_stock_data(ticker,50,TimeFrameUnit.Day)
        print(hist_df_hourly)
        print(hist_df_daily)

        #get current money
        money=trading_client.get_account().cash
        print(money)
        money=500
        closing_price=hist_df['close'].iloc[-1]
        print(closing_price)
        quantity=money/closing_price
        print(quantity)


        if quantity<1:
            continue
        


        elif (pos_df.empty )  or (len(pos_df)!=0 and ticker not in pos_df['symbol'].to_list()):
            print('we have some position but ticker is not in pos')
            strategy_condition(hist_df_hourly,hist_df_daily,ticker)


        
        elif len(pos_df)!=0 and ticker in pos_df['symbol'].to_list():
            print('we have some pos and ticker is in pos')
            curr_quant=float(pos_df[pos_df['symbol']==ticker]['qty'].iloc[-1])
            print(curr_quant)

            if curr_quant==0:
                print('my quantity is 0')
                strategy_condition(hist_df,ticker)

            elif curr_quant>0:


                print('we have current ticker in position and is long')
                sell_condition=hist_df_hourly['super'].iloc[-1]<0 and hist_df_daily['ema'].iloc[-1]>hist_df_hourly['close'].iloc[-1]

                if sell_condition:
                            hourly_closing_price=hist_df_hourly['close'].iloc[-1]
                            atr_value=hist_df_daily['atr'].iloc[-1]
                            print('sell condition satisfied')
                            logging.info(f'Sell condition satisfied for {ticker}')
                            close_this_order_for_stock(ticker)
                            time.sleep(1)
                            close_this_stock_position(ticker)
                            time.sleep(1)
                            trade_sell_stocks(ticker,hourly_closing_price,hourly_closing_price+atr_value)

            elif curr_quant<0:
                print('we have current ticker in position and is short')

                hourly_closing_price=hist_df_hourly['close'].iloc[-1]
                atr_value=hist_df_daily['atr'].iloc[-1]
                buy_condition=hist_df_hourly['super'].iloc[-1]>0 and hist_df_daily['ema'].iloc[-1]<hist_df_hourly['close'].iloc[-1]

                if buy_condition:
                            print('buy condiiton satisfied')
                            logging.info(f'Buy condition satisfied for {ticker}')
                            close_this_order_for_stock(ticker)
                            time.sleep(1)
                            close_this_stock_position(ticker)    
                            time.sleep(1)            
                            trade_buy_stocks(ticker,hourly_closing_price,hourly_closing_price-atr_value)
    time.sleep(1)
    check_and_place_stop_order(pos_df,ord_df)



current_time=dt.now(time_zone)
print(current_time)
start_time=dt.datetime(current_time.year,current_time.month,current_time.day,start_hour,start_min,tz=time_zone)
end_time=dt.datetime(current_time.year,current_time.month,current_time.day,end_hour,end_min,tz=time_zone)
print('start time:', start_time)
print('end time:', end_time)


#pre hour and post hour

while dt.now(time_zone)<start_time :
    print(dt.now(time_zone))
    time.sleep(1)

print('we have reached start time ')
print('we are running our strategy now')


while True:
    if dt.now(time_zone)>end_time:
        break
    ct=dt.now(time_zone)
    print(ct)
    if ct.second in range(2,3) and ct.minute in range(0,60,time_frame):
        main_strategy()
    time.sleep(1)





print('we have reached end time')


#close all orders
for ticker in list_of_tickers:
    close_this_order_for_stock(ticker)
    print('order closed')

#close all positions
for ticker in list_of_tickers:
    close_this_stock_position(ticker)
    print('position closed')


print('strategy stopped')
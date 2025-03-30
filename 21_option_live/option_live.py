# @title
#python 3.12.8
#pip3 install alpaca-py
#pip3 install pandas
#pip3 install setuptools
#pip3 install pendulum

# Iron Condor with Adjustment to Butterfly (SPY - 600)
# Get ATM price from spot → 600
# Buy 12 points OTM call and put for hedge → Buy 588 put and 612 call
# Sell 6 points OTM call and put → Sell 594 put and 606 call
# Adjustments:
# If spot moves by 3 points (e.g., 603)

# Book profit-making leg → Close 612 call and 606 call
# Sell 3 points OTM call with a hedge → Sell 603 call and Buy 606 call
# If spot moves by another 3 points (e.g., 600)

# Close profit-making leg → Close 603 call and 606 call
# Sell ATM call and buy hedge → Sell 600 call and Buy 603 call
# At this point, the Iron Condor is converted into an Iron Butterfly.

# Exit Strategy:
# Close everything at 15:15.


# Replace these values with your actual API credentials

strategy_name='iron_condor'

#strategy parameters

ticker="SPY"
strike_count=25
strike_diff=1
account_type='PAPER'
time_zone="America/New_York"


start_hour,start_min=9,30
end_hour,end_min=15,30
quantity=100

buy_points=8
sell_points=4
spot_move=2

# Import the required module from the fyers_apiv3 package
import datetime as dt
api_key='PKCGQ99MC5FQA1P8ZSRE'
secret_key='rkWLI1F2poiTbuERdzozfOLgVV6mrFKTH27Ugvb1'
import json
import pickle
import sys
from zoneinfo import ZoneInfo
from alpaca.data.live.option import *
from alpaca.data.live.stock import *
from alpaca.data.historical.option import *
from alpaca.data.historical.stock import *
from alpaca.data.requests import *
from alpaca.data.timeframe import *
from alpaca.trading.client import *
from alpaca.trading.stream import *
from alpaca.trading.requests import *
from alpaca.trading.enums import *
from alpaca.common.exceptions import APIError

from alpaca.data.models import OptionsSnapshot
paper = True # Please do not modify this. This example is for paper trading only.
trade_api_url = None
trade_api_wss = None
data_api_url = None
option_stream_data_wss = None


import pandas as pd
import pendulum as dt
import asyncio
import pickle
import time
import webbrowser
import os
import sys
import certifi



#for windows ssl error
os.environ['SSL_CERT_FILE'] = certifi.where()


#disable fyersApi and Fyers Request logs
import logging



#logging to file
logging.basicConfig(level=logging.INFO, filename=f'{strategy_name}_{dt.now(time_zone).date()}.log',filemode='a',format="%(asctime)s - %(message)s")




print('current time is',dt.now(time_zone))

# Get the current time
current_time=dt.now(time_zone)
start_time=dt.datetime(current_time.year,current_time.month,current_time.day,start_hour,start_min,tz=time_zone)
end_time=dt.datetime(current_time.year,current_time.month,current_time.day,end_hour,end_min,tz=time_zone)
print('start time:', start_time)
print('end time:', end_time)



# setup clients
trade_client = TradingClient(api_key=api_key, secret_key=secret_key, paper=paper, url_override=trade_api_url)
acct = trade_client.get_account()


option_data_client = OptionHistoricalDataClient(api_key=api_key,secret_key=secret_key)


# setup clients
stock_historical_data_client = StockHistoricalDataClient(api_key, secret_key, url_override = data_api_url)
StockLatestTradeRequest = StockLatestTradeRequest(symbol_or_symbols=[ticker])
d=stock_historical_data_client.get_stock_latest_trade(StockLatestTradeRequest)
print(d)

spot_price=round(d[ticker].price)
print(spot_price)



expiry=(dt.now(time_zone) + dt.Duration(days=1)).date()
# expiry=(dt.now(time_zone)).date()
print(expiry)

def get_option_data(current_price):

    # setup option historical data client
    option_historical_data_client = OptionHistoricalDataClient(api_key, secret_key, url_override = data_api_url)

    # get option chain by underlying_symbol
    req = OptionChainRequest(underlying_symbol = ticker,
                            expiration_date=expiry,
                            strike_price_gte=current_price-strike_count,
                            strike_price_lte=current_price+strike_count
                            )
    response=option_historical_data_client.get_option_chain(req)
    # print(response)
    data = []
    for symbol, details in response.items():
        
        details=dict(details)
        # print(symbol)
        # print(details['greeks'])
        if not details['greeks']: continue
        row = {
            'symbol': symbol,
            'delta': dict(details['greeks'])['delta'],
            'gamma': dict(details['greeks'])['gamma'],
            'rho': dict(details['greeks'])['rho'],
            'theta': dict(details['greeks'])['theta'],
            'vega': dict(details['greeks'])['vega'],
            'implied_volatility': float(details['implied_volatility']),
            'ask_exchange': dict(details['latest_quote'])['ask_exchange'],
            'ask_price': dict(details['latest_quote'])['ask_price'],
            'ask_size': dict(details['latest_quote'])['ask_size'],
            'bid_exchange': dict(details['latest_quote'])['bid_exchange'],
            'bid_price': dict(details['latest_quote'])['bid_price'],
            'bid_size': dict(details['latest_quote'])['bid_size'],
            # 'quote_conditions': dict(details['latest_quote'])['conditions'],
            # 'quote_timestamp': dict(details['latest_quote'])['timestamp'],
            # 'trade_conditions': dict(details['latest_trade'])['conditions'],
            # 'trade_exchange': dict(details['latest_trade'])['exchange'],
            'trade_price': dict(details['latest_trade'])['price'],
            'trade_size': dict(details['latest_trade'])['size'],
            'trade_timestamp': dict(details['latest_trade'])['timestamp']
        }
        data.append(row)


    df = pd.DataFrame(data)
    # print(df)
    df['strike']=df['symbol'].str[-6:-3]


    df['strike']=df['strike'].astype(int)

    df['right']=df['symbol'].str[-9]
    df.sort_values(by=['strike', 'right'], inplace=True)
    df.set_index('symbol', inplace=True)
    df['right']=df['right'].str.replace("C",'CE')
    df['right']=df['right'].str.replace("P",'PE')

    return df

option_chain=get_option_data(spot_price)

option_chain.reset_index(inplace=True)
print(option_chain)
option_chain.to_csv('option_chain.csv')


# # Function to get the OTM option based on spot price and side (CE/PE)
def get_otm_option(spot_price, side, points=100):
    strikes=option_chain['strike'].unique()
    # print(strikes)
    if side == 'CE':
        otm_strike = (round(spot_price / strike_diff) * strike_diff) + points
    else:
        otm_strike = (round(spot_price / strike_diff) * strike_diff) - points
    otm_strike = min(strikes, key=lambda x:abs(x-otm_strike))
    otm_option = option_chain[(option_chain['strike'] == otm_strike) & (option_chain['right'] == side)]['symbol'].squeeze()
    # print(otm_option)
    return otm_option, otm_strike

# Get the options to sell and hedge
sell_call_option, call_sell_strike = get_otm_option(spot_price, 'CE', sell_points)
sell_put_option, put_sell_strike = get_otm_option(spot_price, 'PE', sell_points)
print('sell call option:', sell_call_option)
print('sell put option:', sell_put_option)

hedge_call_option, call_buy_strike = get_otm_option(spot_price, 'CE', buy_points)
hedge_put_option, put_buy_strike = get_otm_option(spot_price, 'PE', buy_points)
print('hedge call option:', hedge_call_option)
print('hedge put option:', hedge_put_option)

# Log the start of the strategy
logging.info('started')

# Function to store data using pickle
def store(data, account_type):
    pickle.dump(data, open(f'data-{dt.now(time_zone).date()}-{account_type}.pickle', 'wb'))

# Function to load data using pickle
def load(account_type):
    return pickle.load(open(f'data-{dt.now(time_zone).date()}-{account_type}.pickle', 'rb'))

# Function to place a limit order
def take_limit_position(ticker, action, quantity, limit_price):
    try:
        if action==-1:
            direction=OrderSide.SELL
        else:
            direction=OrderSide.BUY
        
        # place market order
        req = MarketOrderRequest(
            symbol = ticker,
            qty = quantity,
            side = direction,
            type = OrderType.MARKET,
            time_in_force = TimeInForce.DAY
        )
        res = trade_client.submit_order(req)
        print(res)

    except Exception as e:
        logging.info(e)
        print(e)
        print('unable to place order for some reason')

# Load or initialize paper trading information
if account_type == 'PAPER':
    try:
        paper_info = load(account_type)
    except:
        column_names = ['time', 'ticker', 'price', 'action', 'stop_price', 'take_profit', 'spot_price', 'quantity']
        filled_df = pd.DataFrame(columns=column_names)
        filled_df.set_index('time', inplace=True)
        paper_info = {
            'call_buy': {'name': hedge_call_option, 'flag': 0, 'buy_price': 0, 'stop_price': 0, 'profit_price': 0, 'filled_df': filled_df.copy(), 'spot': 0, 'quantity': 0, 'strike': 0},
            'put_buy': {'name': hedge_put_option, 'flag': 0, 'buy_price': 0, 'stop_price': 0, 'profit_price': 0, 'filled_df': filled_df.copy(), 'spot': 0, 'quantity': 0, 'strike': 0},
            'call_sell': {'name': sell_call_option, 'flag': 0, 'sell_price': 0, 'stop_price': 0, 'profit_price': 0, 'filled_df': filled_df.copy(), 'spot': 0, 'quantity': 0, 'strike': 0},
            'put_sell': {'name': sell_put_option, 'flag': 0, 'sell_price': 0, 'stop_price': 0, 'profit_price': 0, 'filled_df': filled_df.copy(), 'spot': 0, 'quantity': 0, 'strike': 0},
            "main_flag": 0,
            'enter_spot_price': 0,
            'initial_spot_price': 0,
            'filled_df': filled_df
        }

# Load or initialize live trading information
else:
    try:
        real_info = load(account_type)
    except:
        column_names = ['time', 'ticker', 'price', 'action', 'stop_price', 'take_profit', 'spot_price', 'quantity']
        filled_df = pd.DataFrame(columns=column_names)
        filled_df.set_index('time', inplace=True)
        real_info = {
            'call_buy': {'name': hedge_call_option, 'flag': 0, 'buy_price': 0, 'stop_price': 0, 'profit_price': 0, 'filled_df': filled_df.copy(), 'spot': 0, 'quantity': 0, 'strike': 0},
            'put_buy': {'name': hedge_put_option, 'flag': 0, 'buy_price': 0, 'stop_price': 0, 'profit_price': 0, 'filled_df': filled_df.copy(), 'spot': 0, 'quantity': 0, 'strike': 0},
            'call_sell': {'name': sell_call_option, 'flag': 0, 'sell_price': 0, 'stop_price': 0, 'profit_price': 0, 'filled_df': filled_df.copy(), 'spot': 0, 'quantity': 0, 'strike': 0},
            'put_sell': {'name': sell_put_option, 'flag': 0, 'sell_price': 0, 'stop_price': 0, 'profit_price': 0, 'filled_df': filled_df.copy(), 'spot': 0, 'quantity': 0, 'strike': 0},
            "main_flag": 0,
            'enter_spot_price': 0,
            'initial_spot_price': 0,
            'filled_df': filled_df
        }




def paper_order(spot_price,df):
    global quantity
    global paper_info
 
  

    ct = dt.now(time_zone)  # Get the current time

    if ct > start_time:  # Check if the current time is after the start time

        # Get the option names from paper_info
        call_buy_name = paper_info.get('call_buy').get('name')
        put_buy_name = paper_info.get('put_buy').get('name')
        call_sell_name = paper_info.get('call_sell').get('name')
        put_sell_name = paper_info.get('put_sell').get('name')

        # Get the flags for each option
        call_buy_flag = paper_info.get('call_buy').get('flag')
        put_buy_flag = paper_info.get('put_buy').get('flag')
        call_sell_flag = paper_info.get('call_sell').get('flag')
        put_sell_flag = paper_info.get('put_sell').get('flag')

        # Get the buy and sell prices for each option
        call_buy_price = paper_info.get('call_buy').get('buy_price')
        put_buy_price = paper_info.get('put_buy').get('buy_price')
        call_sell_price = paper_info.get('call_sell').get('sell_price')
        put_sell_price = paper_info.get('put_sell').get('sell_price')

        # Get the current prices for each option
        call_buy_current_price = df.loc[call_buy_name, 'trade_price']
        put_buy_current_price = df.loc[put_buy_name, 'trade_price']
        call_sell_current_price = df.loc[call_sell_name, 'trade_price']
        put_sell_current_price = df.loc[put_sell_name, 'trade_price']

        print(call_buy_current_price,put_buy_current_price,call_sell_current_price,put_sell_current_price)

        # Get the main flag and enter spot price from paper_info
        main_flag = paper_info['main_flag']
        enter_spot_price = paper_info['enter_spot_price']

        if ct > end_time:  # Check if the current time is after the end time
            logging.info('closing everything')

            # Close call buy position
            if call_buy_flag == 1:
                a = [call_buy_name, call_buy_current_price, 'SELL', 0, 0, spot_price, 0]
                paper_info['filled_df'].loc[dt.now(time_zone)] = a
                paper_info['call_buy']['flag'] = 5
                paper_info['call_buy']['quantity'] = 0
                logging.info(f'Closed call buy position: {call_buy_name} at {call_buy_current_price}')


            # Close put buy position
            if put_buy_flag == 1:
                a = [put_buy_name, put_buy_current_price, 'SELL', 0, 0, spot_price, 0]
                paper_info['filled_df'].loc[dt.now(time_zone)] = a
                paper_info['put_buy']['flag'] = 5
                paper_info['put_buy']['quantity'] = 0
                logging.info(f'Closed put buy position: {put_buy_name} at {put_buy_current_price}')


            # Close call sell position
            if call_sell_flag == 1:
                a = [call_sell_name, call_sell_current_price, 'BUY', 0, 0, spot_price, 0]
                paper_info['filled_df'].loc[dt.now(time_zone)] = a
                paper_info['call_sell']['flag'] = 5
                paper_info['call_sell']['quantity'] = 0
                logging.info(f'Closed call sell position: {call_sell_name} at {call_sell_current_price}')


            # Close put sell position
            if put_sell_flag == 1:
                a = [put_sell_name, put_sell_current_price, 'BUY', 0, 0, spot_price, 0]
                paper_info['filled_df'].loc[dt.now(time_zone)] = a
                paper_info['put_sell']['flag'] = 5
                paper_info['put_sell']['quantity'] = 0
                logging.info(f'Closed put sell position: {put_sell_name} at {put_sell_current_price}')


        if main_flag == 0:  # Check if the main flag is 0
            logging.info('placing iron condor')

            # Buy hedge options first
            call_buy_name, strike = get_otm_option(spot_price, 'CE', buy_points)
            paper_info['call_buy'].update({'name': call_buy_name, 'quantity': quantity, 'strike': strike})

            put_buy_name, strike = get_otm_option(spot_price, 'PE', buy_points)
            paper_info['put_buy'].update({'name': put_buy_name, 'quantity': quantity, 'strike': strike})

            call_buy_current_price = df.loc[call_buy_name, 'trade_price']
            put_buy_current_price = df.loc[put_buy_name, 'trade_price']

            paper_info['call_buy']['buy_price'] = call_buy_current_price
            paper_info['put_buy']['buy_price'] = put_buy_current_price

            # Log the buy positions
            a = [call_buy_name, call_buy_current_price, 'BUY', 0, 0, spot_price, quantity]
            paper_info['filled_df'].loc[dt.now(time_zone)] = a
            paper_info['call_buy']['flag'] = 1
            logging.info(f'Bought call hedge: {call_buy_name} at {call_buy_current_price}')

            b = [put_buy_name, put_buy_current_price, 'BUY', 0, 0, spot_price, quantity]
            paper_info['filled_df'].loc[dt.now(time_zone)] = b
            paper_info['put_buy']['flag'] = 1
            logging.info(f'Bought put hedge: {put_buy_name} at {put_buy_current_price}')



            # Sell the legs
            call_sell_name, strike = get_otm_option(spot_price, 'CE', sell_points)
            paper_info['call_sell'].update({'name': call_sell_name, 'quantity': quantity, 'strike': strike})

            put_sell_name, strike = get_otm_option(spot_price, 'PE', sell_points)
            paper_info['put_sell'].update({'name': put_sell_name, 'quantity': quantity, 'strike': strike})

            call_sell_current_price = df.loc[call_sell_name, 'trade_price']
            put_sell_current_price = df.loc[put_sell_name, 'trade_price']

            paper_info['call_sell']['sell_price'] = call_sell_current_price
            paper_info['put_sell']['sell_price'] = put_sell_current_price

            # Log the sell positions
            a = [call_sell_name, call_sell_current_price, 'SELL', 0, 0, spot_price, quantity]
            paper_info['filled_df'].loc[dt.now(time_zone)] = a
            paper_info['call_sell']['flag'] = 1
            logging.info(f'Sold call leg: {call_sell_name} at {call_sell_current_price}')

            b = [put_sell_name, put_sell_current_price, 'SELL', 0, 0, spot_price, quantity]
            paper_info['filled_df'].loc[dt.now(time_zone)] = b
            paper_info['put_sell']['flag'] = 1
            logging.info(f'Sold put leg: {put_sell_name} at {put_sell_current_price}')

            # Update the enter spot price, initial spot price, and main flag in paper_info
            paper_info.update({'enter_spot_price': spot_price, 'initial_spot_price': spot_price, 'main_flag': 1})
            logging.info('done placing condor')

        elif main_flag == 1:  # Check if the main flag is 1

            if spot_price < enter_spot_price - spot_move:
                # Close call buy position
                a = [call_buy_name, call_buy_current_price, 'SELL', 0, 0, spot_price, quantity]
                paper_info['filled_df'].loc[dt.now(time_zone)] = a
                logging.info(f'Closed call buy position: {call_buy_name} at {call_buy_current_price}')


                # Close call sell position
                a = [call_sell_name, call_sell_current_price, 'BUY', 0, 0, spot_price, quantity]
                paper_info['filled_df'].loc[dt.now(time_zone)] = a
                logging.info(f'Closed call sell position: {call_sell_name} at {call_sell_current_price}')


                # Open new call buy position
                s = paper_info['call_buy']['strike'] - spot_move * 2
                call_buy_name = option_chain[(option_chain['strike_price'] == s) & (option_chain['option_type'] == 'CE')]['symbol'].squeeze()
                paper_info['call_buy'].update({'name': call_buy_name, 'quantity': quantity, 'strike': s})
                call_buy_current_price = df.loc[call_buy_name, 'trade_price']
                paper_info['call_buy']['buy_price'] = call_buy_current_price
                a = [call_buy_name, call_buy_current_price, 'BUY', 0, 0, spot_price, quantity]
                paper_info['filled_df'].loc[dt.now(time_zone)] = a
                paper_info['call_buy']['flag'] = 1
                logging.info(f'Opened new call buy position: {call_buy_name} at {call_buy_current_price}')


                # Open new call sell position
                s = paper_info['call_sell']['strike'] - spot_move * 2
                call_sell_name = option_chain[(option_chain['strike_price'] == s) & (option_chain['option_type'] == 'CE')]['symbol'].squeeze()
                paper_info['call_sell'].update({'name': call_sell_name, 'quantity': quantity, 'strike': s})
                call_sell_current_price = df.loc[call_sell_name, 'trade_price']
                paper_info['call_sell']['sell_price'] = call_sell_current_price
                a = [call_sell_name, call_sell_current_price, 'SELL', 0, 0, spot_price, quantity]
                paper_info['filled_df'].loc[dt.now(time_zone)] = a
                paper_info['call_sell']['flag'] = 1
                logging.info(f'Opened new call sell position: {call_sell_name} at {call_sell_current_price}')

                # Update the enter spot price and main flag in paper_info
                paper_info.update({'enter_spot_price': spot_price, 'main_flag': 2})
                logging.info('done doing adjustment')

            elif spot_price > enter_spot_price + spot_move:
                # Close put buy position
                a = [put_buy_name, put_buy_current_price, 'SELL', 0, 0, spot_price, quantity]
                paper_info['filled_df'].loc[dt.now(time_zone)] = a
                logging.info(f'Closed put buy position: {put_buy_name} at {put_buy_current_price}')

                # Close put sell position
                a = [put_sell_name, put_sell_current_price, 'BUY', 0, 0, spot_price, quantity]
                paper_info['filled_df'].loc[dt.now(time_zone)] = a
                logging.info(f'Closed put sell position: {put_sell_name} at {put_sell_current_price}')

                # Open new put buy position
                s = paper_info['put_buy']['strike'] + spot_move * 2
                put_buy_name = option_chain[(option_chain['strike_price'] == s) & (option_chain['option_type'] == 'PE')]['symbol'].squeeze()
                paper_info['put_buy'].update({'name': put_buy_name, 'quantity': quantity, 'strike': s})
                put_buy_current_price = df.loc[put_buy_name, 'trade_price']
                paper_info['put_buy']['buy_price'] = put_buy_current_price
                a = [put_buy_name, put_buy_current_price, 'BUY', 0, 0, spot_price, quantity]
                paper_info['filled_df'].loc[dt.now(time_zone)] = a
                paper_info['put_buy']['flag'] = 1
                logging.info(f'Opened new put buy position: {put_buy_name} at {put_buy_current_price}')

                # Open new put sell position
                s = paper_info['put_sell']['strike'] + spot_move * 2
                put_sell_name = option_chain[(option_chain['strike_price'] == s) & (option_chain['option_type'] == 'PE')]['symbol'].squeeze()
                paper_info['put_sell'].update({'name': put_sell_name, 'quantity': quantity, 'strike': s})
                put_sell_current_price = df.loc[put_sell_name, 'trade_price']
                paper_info['put_sell']['sell_price'] = put_sell_current_price
                a = [put_sell_name, put_sell_current_price, 'SELL', 0, 0, spot_price, quantity]
                paper_info['filled_df'].loc[dt.now(time_zone)] = a
                paper_info['put_sell']['flag'] = 1
                logging.info(f'Opened new put sell position: {put_sell_name} at {put_sell_current_price}')

                # Update the enter spot price and main flag in paper_info
                paper_info.update({'enter_spot_price': spot_price, 'main_flag': 2})
                logging.info('done doing adjustment')

        elif main_flag == 2:  # Check if the main flag is 2

            if spot_price < enter_spot_price - spot_move:
                # Close call buy position
                a = [call_buy_name, call_buy_current_price, 'SELL', 0, 0, spot_price, quantity]
                paper_info['filled_df'].loc[dt.now(time_zone)] = a
                logging.info(f'Closed call buy position: {call_buy_name} at {call_buy_current_price}')


                # Close call sell position
                a = [call_sell_name, call_sell_current_price, 'BUY', 0, 0, spot_price, quantity]
                paper_info['filled_df'].loc[dt.now(time_zone)] = a
                logging.info(f'Closed call sell position: {call_sell_name} at {call_sell_current_price}')


                # Open new call buy position
                s = paper_info['call_buy']['strike'] - spot_move * 2
                call_buy_name = option_chain[(option_chain['strike_price'] == s) & (option_chain['option_type'] == 'CE')]['symbol'].squeeze()
                paper_info['call_buy'].update({'name': call_buy_name, 'quantity': quantity, 'strike': s})
                call_buy_current_price = df.loc[call_buy_name, 'trade_price']
                paper_info['call_buy']['buy_price'] = call_buy_current_price
                a = [call_buy_name, call_buy_current_price, 'BUY', 0, 0, spot_price, quantity]
                paper_info['filled_df'].loc[dt.now(time_zone)] = a
                paper_info['call_buy']['flag'] = 1
                logging.info(f'Opened new call buy position: {call_buy_name} at {call_buy_current_price}')


                # Open new call sell position
                s = paper_info['call_sell']['strike'] - spot_move * 2
                call_sell_name = option_chain[(option_chain['strike_price'] == s) & (option_chain['option_type'] == 'CE')]['symbol'].squeeze()
                paper_info['call_sell'].update({'name': call_sell_name, 'quantity': quantity, 'strike': s})
                call_sell_current_price = df.loc[call_sell_name, 'trade_price']
                paper_info['call_sell']['sell_price'] = call_sell_current_price
                a = [call_sell_name, call_sell_current_price, 'SELL', 0, 0, spot_price, quantity]
                paper_info['filled_df'].loc[dt.now(time_zone)] = a
                paper_info['call_sell']['flag'] = 1
                logging.info(f'Opened new call sell position: {call_sell_name} at {call_sell_current_price}')

                # Update the enter spot price and main flag in paper_info
                paper_info.update({'enter_spot_price': spot_price, 'main_flag': 3})
                logging.info('done doing adjustment')

            elif spot_price > enter_spot_price + spot_move:
                # Close put buy position
                a = [put_buy_name, put_buy_current_price, 'SELL', 0, 0, spot_price, quantity]
                paper_info['filled_df'].loc[dt.now(time_zone)] = a
                logging.info(f'Closed put buy position: {put_buy_name} at {put_buy_current_price}')

                # Close put sell position
                a = [put_sell_name, put_sell_current_price, 'BUY', 0, 0, spot_price, quantity]
                paper_info['filled_df'].loc[dt.now(time_zone)] = a
                logging.info(f'Closed put sell position: {put_sell_name} at {put_sell_current_price}')

                # Open new put buy position
                s = paper_info['put_buy']['strike'] + spot_move * 2
                put_buy_name = option_chain[(option_chain['strike_price'] == s) & (option_chain['option_type'] == 'PE')]['symbol'].squeeze()
                paper_info['put_buy'].update({'name': put_buy_name, 'quantity': quantity, 'strike': s})
                put_buy_current_price = df.loc[put_buy_name, 'trade_price']
                paper_info['put_buy']['buy_price'] = put_buy_current_price
                a = [put_buy_name, put_buy_current_price, 'BUY', 0, 0, spot_price, quantity]
                paper_info['filled_df'].loc[dt.now(time_zone)] = a
                paper_info['put_buy']['flag'] = 1
                logging.info(f'Opened new put buy position: {put_buy_name} at {put_buy_current_price}')

                # Open new put sell position
                s = paper_info['put_sell']['strike'] + spot_move * 2
                put_sell_name = option_chain[(option_chain['strike_price'] == s) & (option_chain['option_type'] == 'PE')]['symbol'].squeeze()
                paper_info['put_sell'].update({'name': put_sell_name, 'quantity': quantity, 'strike': s})
                put_sell_current_price = df.loc[put_sell_name, 'trade_price']
                paper_info['put_sell']['sell_price'] = put_sell_current_price
                a = [put_sell_name, put_sell_current_price, 'SELL', 0, 0, spot_price, quantity]
                paper_info['filled_df'].loc[dt.now(time_zone)] = a
                paper_info['put_sell']['flag'] = 1
                logging.info(f'Opened new put sell position: {put_sell_name} at {put_sell_current_price}')

                # Update the enter spot price and main flag in paper_info
                paper_info.update({'enter_spot_price': spot_price, 'main_flag': 3})
                logging.info('done doing adjustment')

        elif main_flag == 3:  # Check if the main flag is 3

            if (spot_price < paper_info['initial_spot_price'] - (3 * spot_move)) or (spot_price > paper_info['initial_spot_price'] + (3 * spot_move)):
                logging.info('closing everything')

                # Close call buy position
                if call_buy_flag == 1:
                    a = [call_buy_name, call_buy_current_price, 'SELL', 0, 0, spot_price, 0]
                    paper_info['filled_df'].loc[dt.now(time_zone)] = a
                    paper_info['call_buy']['flag'] = 5
                    paper_info['call_buy']['quantity'] = 0
                    logging.info(f'Closed call buy position: {call_buy_name} at {call_buy_current_price}')


                # Close put buy position
                if put_buy_flag == 1:
                    a = [put_buy_name, put_buy_current_price, 'SELL', 0, 0, spot_price, 0]
                    paper_info['filled_df'].loc[dt.now(time_zone)] = a
                    paper_info['put_buy']['flag'] = 5
                    paper_info['put_buy']['quantity'] = 0
                    logging.info(f'Closed put buy position: {put_buy_name} at {put_buy_current_price}')


                # Close call sell position
                if call_sell_flag == 1:
                    a = [call_sell_name, call_sell_current_price, 'BUY', 0, 0, spot_price, 0]
                    paper_info['filled_df'].loc[dt.now(time_zone)] = a
                    paper_info['call_sell']['flag'] = 5
                    paper_info['call_sell']['quantity'] = 0
                    logging.info(f'Closed call sell position: {call_sell_name} at {call_sell_current_price}')


                # Close put sell position
                if put_sell_flag == 1:
                    a = [put_sell_name, put_sell_current_price, 'BUY', 0, 0, spot_price, 0]
                    paper_info['filled_df'].loc[dt.now(time_zone)] = a
                    paper_info['put_sell']['flag'] = 5
                    paper_info['put_sell']['quantity'] = 0
                    logging.info(f'Closed put sell position: {put_sell_name} at {put_sell_current_price}')


        # Save the filled_df to a CSV file if it's not empty
        if not paper_info['filled_df'].empty:
            paper_info['filled_df'].to_csv(f'trades_{strategy_name}_{dt.now(time_zone).date()}.csv')

        # Store the paper_info using pickle
        store(paper_info, account_type)


def real_order(spot_price,df):
    global quantity
    global real_info
 
  

    ct = dt.now(time_zone)  # Get the current time

    if ct > start_time:  # Check if the current time is after the start time

        # Get the option names from real_info
        call_buy_name = real_info.get('call_buy').get('name')
        put_buy_name = real_info.get('put_buy').get('name')
        call_sell_name = real_info.get('call_sell').get('name')
        put_sell_name = real_info.get('put_sell').get('name')

        # Get the flags for each option
        call_buy_flag = real_info.get('call_buy').get('flag')
        put_buy_flag = real_info.get('put_buy').get('flag')
        call_sell_flag = real_info.get('call_sell').get('flag')
        put_sell_flag = real_info.get('put_sell').get('flag')

        # Get the buy and sell prices for each option
        call_buy_price = real_info.get('call_buy').get('buy_price')
        put_buy_price = real_info.get('put_buy').get('buy_price')
        call_sell_price = real_info.get('call_sell').get('sell_price')
        put_sell_price = real_info.get('put_sell').get('sell_price')

        # Get the current prices for each option
        call_buy_current_price = df.loc[call_buy_name, 'trade_price']
        put_buy_current_price = df.loc[put_buy_name, 'trade_price']
        call_sell_current_price = df.loc[call_sell_name, 'trade_price']
        put_sell_current_price = df.loc[put_sell_name, 'trade_price']

        print(call_buy_current_price,put_buy_current_price,call_sell_current_price,put_sell_current_price)

        # Get the main flag and enter spot price from real_info
        main_flag = real_info['main_flag']
        enter_spot_price = real_info['enter_spot_price']

        if ct > end_time:  # Check if the current time is after the end time
            logging.info('closing everything')

            # Close call buy position
            if call_buy_flag == 1:
                a = [call_buy_name, call_buy_current_price, 'SELL', 0, 0, spot_price, 0]
                real_info['filled_df'].loc[dt.now(time_zone)] = a
                real_info['call_buy']['flag'] = 5
                real_info['call_buy']['quantity'] = 0
                logging.info(f'Closed call buy position: {call_buy_name} at {call_buy_current_price}')
                trade_client.close_position(call_buy_name)


            # Close put buy position
            if put_buy_flag == 1:
                a = [put_buy_name, put_buy_current_price, 'SELL', 0, 0, spot_price, 0]
                real_info['filled_df'].loc[dt.now(time_zone)] = a
                real_info['put_buy']['flag'] = 5
                real_info['put_buy']['quantity'] = 0
                logging.info(f'Closed put buy position: {put_buy_name} at {put_buy_current_price}')
                trade_client.close_position(put_buy_name)


            # Close call sell position
            if call_sell_flag == 1:
                a = [call_sell_name, call_sell_current_price, 'BUY', 0, 0, spot_price, 0]
                real_info['filled_df'].loc[dt.now(time_zone)] = a
                real_info['call_sell']['flag'] = 5
                real_info['call_sell']['quantity'] = 0
                logging.info(f'Closed call sell position: {call_sell_name} at {call_sell_current_price}')
                trade_client.close_position(call_sell_name)


            # Close put sell position
            if put_sell_flag == 1:
                a = [put_sell_name, put_sell_current_price, 'BUY', 0, 0, spot_price, 0]
                real_info['filled_df'].loc[dt.now(time_zone)] = a
                real_info['put_sell']['flag'] = 5
                real_info['put_sell']['quantity'] = 0
                logging.info(f'Closed put sell position: {put_sell_name} at {put_sell_current_price}')
                trade_client.close_position(put_sell_name)


        if main_flag == 0:  # Check if the main flag is 0
            logging.info('placing iron condor')

            # Buy hedge options first
            call_buy_name, strike = get_otm_option(spot_price, 'CE', buy_points)
            real_info['call_buy'].update({'name': call_buy_name, 'quantity': quantity, 'strike': strike})

            put_buy_name, strike = get_otm_option(spot_price, 'PE', buy_points)
            real_info['put_buy'].update({'name': put_buy_name, 'quantity': quantity, 'strike': strike})

            call_buy_current_price = df.loc[call_buy_name, 'trade_price']
            put_buy_current_price = df.loc[put_buy_name, 'trade_price']

            real_info['call_buy']['buy_price'] = call_buy_current_price
            real_info['put_buy']['buy_price'] = put_buy_current_price

            # Log the buy positions
            a = [call_buy_name, call_buy_current_price, 'BUY', 0, 0, spot_price, quantity]
            real_info['filled_df'].loc[dt.now(time_zone)] = a
            real_info['call_buy']['flag'] = 1
            logging.info(f'Bought call hedge: {call_buy_name} at {call_buy_current_price}')

            b = [put_buy_name, put_buy_current_price, 'BUY', 0, 0, spot_price, quantity]
            real_info['filled_df'].loc[dt.now(time_zone)] = b
            real_info['put_buy']['flag'] = 1
            logging.info(f'Bought put hedge: {put_buy_name} at {put_buy_current_price}')

            take_limit_position(call_buy_name, 1, quantity, call_buy_current_price)
            take_limit_position(put_buy_name, 1, quantity, put_buy_current_price)

            # Sell the legs
            call_sell_name, strike = get_otm_option(spot_price, 'CE', sell_points)
            real_info['call_sell'].update({'name': call_sell_name, 'quantity': quantity, 'strike': strike})

            put_sell_name, strike = get_otm_option(spot_price, 'PE', sell_points)
            real_info['put_sell'].update({'name': put_sell_name, 'quantity': quantity, 'strike': strike})

            call_sell_current_price = df.loc[call_sell_name, 'trade_price']
            put_sell_current_price = df.loc[put_sell_name, 'trade_price']

            real_info['call_sell']['sell_price'] = call_sell_current_price
            real_info['put_sell']['sell_price'] = put_sell_current_price

            # Log the sell positions
            a = [call_sell_name, call_sell_current_price, 'SELL', 0, 0, spot_price, quantity]
            real_info['filled_df'].loc[dt.now(time_zone)] = a
            real_info['call_sell']['flag'] = 1
            logging.info(f'Sold call leg: {call_sell_name} at {call_sell_current_price}')

            b = [put_sell_name, put_sell_current_price, 'SELL', 0, 0, spot_price, quantity]
            real_info['filled_df'].loc[dt.now(time_zone)] = b
            real_info['put_sell']['flag'] = 1
            logging.info(f'Sold put leg: {put_sell_name} at {put_sell_current_price}')

            # Update the enter spot price, initial spot price, and main flag in real_info
            real_info.update({'enter_spot_price': spot_price, 'initial_spot_price': spot_price, 'main_flag': 1})
            logging.info('done placing condor')
            
            take_limit_position(call_sell_name, -1, quantity, call_sell_current_price)
            take_limit_position(put_sell_name, -1, quantity, put_sell_current_price)


        elif main_flag == 1:  # Check if the main flag is 1

            if spot_price < enter_spot_price - spot_move:
                # Close call buy position
                a = [call_buy_name, call_buy_current_price, 'SELL', 0, 0, spot_price, quantity]
                real_info['filled_df'].loc[dt.now(time_zone)] = a
                logging.info(f'Closed call buy position: {call_buy_name} at {call_buy_current_price}')
                trade_client.close_position(call_buy_name)


                # Close call sell position
                a = [call_sell_name, call_sell_current_price, 'BUY', 0, 0, spot_price, quantity]
                real_info['filled_df'].loc[dt.now(time_zone)] = a
                logging.info(f'Closed call sell position: {call_sell_name} at {call_sell_current_price}')
                trade_client.close_position(call_sell_name)


                # Open new call buy position
                s = real_info['call_buy']['strike'] - spot_move * 2
                call_buy_name = option_chain[(option_chain['strike_price'] == s) & (option_chain['option_type'] == 'CE')]['symbol'].squeeze()
                real_info['call_buy'].update({'name': call_buy_name, 'quantity': quantity, 'strike': s})
                call_buy_current_price = df.loc[call_buy_name, 'trade_price']
                real_info['call_buy']['buy_price'] = call_buy_current_price
                a = [call_buy_name, call_buy_current_price, 'BUY', 0, 0, spot_price, quantity]
                real_info['filled_df'].loc[dt.now(time_zone)] = a
                real_info['call_buy']['flag'] = 1
                logging.info(f'Opened new call buy position: {call_buy_name} at {call_buy_current_price}')
                take_limit_position(call_buy_name, 1, quantity, call_buy_current_price)


                # Open new call sell position
                s = real_info['call_sell']['strike'] - spot_move * 2
                call_sell_name = option_chain[(option_chain['strike_price'] == s) & (option_chain['option_type'] == 'CE')]['symbol'].squeeze()
                real_info['call_sell'].update({'name': call_sell_name, 'quantity': quantity, 'strike': s})
                call_sell_current_price = df.loc[call_sell_name, 'trade_price']
                real_info['call_sell']['sell_price'] = call_sell_current_price
                a = [call_sell_name, call_sell_current_price, 'SELL', 0, 0, spot_price, quantity]
                real_info['filled_df'].loc[dt.now(time_zone)] = a
                real_info['call_sell']['flag'] = 1
                logging.info(f'Opened new call sell position: {call_sell_name} at {call_sell_current_price}')
                take_limit_position(call_sell_name, -1, quantity, call_sell_current_price)

                # Update the enter spot price and main flag in real_info
                real_info.update({'enter_spot_price': spot_price, 'main_flag': 2})
                logging.info('done doing adjustment')

            elif spot_price > enter_spot_price + spot_move:
                # Close put buy position
                a = [put_buy_name, put_buy_current_price, 'SELL', 0, 0, spot_price, quantity]
                real_info['filled_df'].loc[dt.now(time_zone)] = a
                logging.info(f'Closed put buy position: {put_buy_name} at {put_buy_current_price}')
                trade_client.close_position(put_buy_name)

                # Close put sell position
                a = [put_sell_name, put_sell_current_price, 'BUY', 0, 0, spot_price, quantity]
                real_info['filled_df'].loc[dt.now(time_zone)] = a
                logging.info(f'Closed put sell position: {put_sell_name} at {put_sell_current_price}')
                trade_client.close_position(put_sell_name)

                # Open new put buy position
                s = real_info['put_buy']['strike'] + spot_move * 2
                put_buy_name = option_chain[(option_chain['strike_price'] == s) & (option_chain['option_type'] == 'PE')]['symbol'].squeeze()
                real_info['put_buy'].update({'name': put_buy_name, 'quantity': quantity, 'strike': s})
                put_buy_current_price = df.loc[put_buy_name, 'trade_price']
                real_info['put_buy']['buy_price'] = put_buy_current_price
                a = [put_buy_name, put_buy_current_price, 'BUY', 0, 0, spot_price, quantity]
                real_info['filled_df'].loc[dt.now(time_zone)] = a
                real_info['put_buy']['flag'] = 1
                logging.info(f'Opened new put buy position: {put_buy_name} at {put_buy_current_price}')
                take_limit_position(put_buy_name, 1, quantity, put_buy_current_price)

                # Open new put sell position
                s = real_info['put_sell']['strike'] + spot_move * 2
                put_sell_name = option_chain[(option_chain['strike_price'] == s) & (option_chain['option_type'] == 'PE')]['symbol'].squeeze()
                real_info['put_sell'].update({'name': put_sell_name, 'quantity': quantity, 'strike': s})
                put_sell_current_price = df.loc[put_sell_name, 'trade_price']
                real_info['put_sell']['sell_price'] = put_sell_current_price
                a = [put_sell_name, put_sell_current_price, 'SELL', 0, 0, spot_price, quantity]
                real_info['filled_df'].loc[dt.now(time_zone)] = a
                real_info['put_sell']['flag'] = 1
                logging.info(f'Opened new put sell position: {put_sell_name} at {put_sell_current_price}')
                take_limit_position(put_sell_name, -1, quantity, put_sell_current_price)

                # Update the enter spot price and main flag in real_info
                real_info.update({'enter_spot_price': spot_price, 'main_flag': 2})
                logging.info('done doing adjustment')

        elif main_flag == 2:  # Check if the main flag is 2

            if spot_price < enter_spot_price - spot_move:
                # Close call buy position
                a = [call_buy_name, call_buy_current_price, 'SELL', 0, 0, spot_price, quantity]
                real_info['filled_df'].loc[dt.now(time_zone)] = a
                logging.info(f'Closed call buy position: {call_buy_name} at {call_buy_current_price}')
                trade_client.close_position(call_buy_name)


                # Close call sell position
                a = [call_sell_name, call_sell_current_price, 'BUY', 0, 0, spot_price, quantity]
                real_info['filled_df'].loc[dt.now(time_zone)] = a
                logging.info(f'Closed call sell position: {call_sell_name} at {call_sell_current_price}')
                trade_client.close_position(call_sell_name)


                # Open new call buy position
                s = real_info['call_buy']['strike'] - spot_move * 2
                call_buy_name = option_chain[(option_chain['strike_price'] == s) & (option_chain['option_type'] == 'CE')]['symbol'].squeeze()
                real_info['call_buy'].update({'name': call_buy_name, 'quantity': quantity, 'strike': s})
                call_buy_current_price = df.loc[call_buy_name, 'trade_price']
                real_info['call_buy']['buy_price'] = call_buy_current_price
                a = [call_buy_name, call_buy_current_price, 'BUY', 0, 0, spot_price, quantity]
                real_info['filled_df'].loc[dt.now(time_zone)] = a
                real_info['call_buy']['flag'] = 1
                logging.info(f'Opened new call buy position: {call_buy_name} at {call_buy_current_price}')
                take_limit_position(call_buy_name, 1, quantity, call_buy_current_price)


                # Open new call sell position
                s = real_info['call_sell']['strike'] - spot_move * 2
                call_sell_name = option_chain[(option_chain['strike_price'] == s) & (option_chain['option_type'] == 'CE')]['symbol'].squeeze()
                real_info['call_sell'].update({'name': call_sell_name, 'quantity': quantity, 'strike': s})
                call_sell_current_price = df.loc[call_sell_name, 'trade_price']
                real_info['call_sell']['sell_price'] = call_sell_current_price
                a = [call_sell_name, call_sell_current_price, 'SELL', 0, 0, spot_price, quantity]
                real_info['filled_df'].loc[dt.now(time_zone)] = a
                real_info['call_sell']['flag'] = 1
                logging.info(f'Opened new call sell position: {call_sell_name} at {call_sell_current_price}')
                take_limit_position(call_sell_name, -1, quantity, call_sell_current_price)

                # Update the enter spot price and main flag in real_info
                real_info.update({'enter_spot_price': spot_price, 'main_flag': 3})
                logging.info('done doing adjustment')

            elif spot_price > enter_spot_price + spot_move:
                # Close put buy position
                a = [put_buy_name, put_buy_current_price, 'SELL', 0, 0, spot_price, quantity]
                real_info['filled_df'].loc[dt.now(time_zone)] = a
                logging.info(f'Closed put buy position: {put_buy_name} at {put_buy_current_price}')
                trade_client.close_position(put_buy_name)

                # Close put sell position
                a = [put_sell_name, put_sell_current_price, 'BUY', 0, 0, spot_price, quantity]
                real_info['filled_df'].loc[dt.now(time_zone)] = a
                logging.info(f'Closed put sell position: {put_sell_name} at {put_sell_current_price}')
                trade_client.close_position(put_sell_name)

                # Open new put buy position
                s = real_info['put_buy']['strike'] + spot_move * 2
                put_buy_name = option_chain[(option_chain['strike_price'] == s) & (option_chain['option_type'] == 'PE')]['symbol'].squeeze()
                real_info['put_buy'].update({'name': put_buy_name, 'quantity': quantity, 'strike': s})
                put_buy_current_price = df.loc[put_buy_name, 'trade_price']
                real_info['put_buy']['buy_price'] = put_buy_current_price
                a = [put_buy_name, put_buy_current_price, 'BUY', 0, 0, spot_price, quantity]
                real_info['filled_df'].loc[dt.now(time_zone)] = a
                real_info['put_buy']['flag'] = 1
                logging.info(f'Opened new put buy position: {put_buy_name} at {put_buy_current_price}')
                take_limit_position(put_buy_name, 1, quantity, put_buy_current_price)

                # Open new put sell position
                s = real_info['put_sell']['strike'] + spot_move * 2
                put_sell_name = option_chain[(option_chain['strike_price'] == s) & (option_chain['option_type'] == 'PE')]['symbol'].squeeze()
                real_info['put_sell'].update({'name': put_sell_name, 'quantity': quantity, 'strike': s})
                put_sell_current_price = df.loc[put_sell_name, 'trade_price']
                real_info['put_sell']['sell_price'] = put_sell_current_price
                a = [put_sell_name, put_sell_current_price, 'SELL', 0, 0, spot_price, quantity]
                real_info['filled_df'].loc[dt.now(time_zone)] = a
                real_info['put_sell']['flag'] = 1
                logging.info(f'Opened new put sell position: {put_sell_name} at {put_sell_current_price}')
                take_limit_position(put_sell_name, -1, quantity, put_sell_current_price)

                # Update the enter spot price and main flag in real_info
                real_info.update({'enter_spot_price': spot_price, 'main_flag': 3})
                logging.info('done doing adjustment')

        elif main_flag == 3:  # Check if the main flag is 3

            if (spot_price < real_info['initial_spot_price'] - (3 * spot_move)) or (spot_price > real_info['initial_spot_price'] + (3 * spot_move)):
                logging.info('closing everything')

                # Close call buy position
                if call_buy_flag == 1:
                    a = [call_buy_name, call_buy_current_price, 'SELL', 0, 0, spot_price, 0]
                    real_info['filled_df'].loc[dt.now(time_zone)] = a
                    real_info['call_buy']['flag'] = 5
                    real_info['call_buy']['quantity'] = 0
                    logging.info(f'Closed call buy position: {call_buy_name} at {call_buy_current_price}')
                    trade_client.close_position(call_buy_name)


                # Close put buy position
                if put_buy_flag == 1:
                    a = [put_buy_name, put_buy_current_price, 'SELL', 0, 0, spot_price, 0]
                    real_info['filled_df'].loc[dt.now(time_zone)] = a
                    real_info['put_buy']['flag'] = 5
                    real_info['put_buy']['quantity'] = 0
                    logging.info(f'Closed put buy position: {put_buy_name} at {put_buy_current_price}')
                    trade_client.close_position(put_buy_name)


                # Close call sell position
                if call_sell_flag == 1:
                    a = [call_sell_name, call_sell_current_price, 'BUY', 0, 0, spot_price, 0]
                    real_info['filled_df'].loc[dt.now(time_zone)] = a
                    real_info['call_sell']['flag'] = 5
                    real_info['call_sell']['quantity'] = 0
                    logging.info(f'Closed call sell position: {call_sell_name} at {call_sell_current_price}')
                    trade_client.close_position(call_sell_name)


                # Close put sell position
                if put_sell_flag == 1:
                    a = [put_sell_name, put_sell_current_price, 'BUY', 0, 0, spot_price, 0]
                    real_info['filled_df'].loc[dt.now(time_zone)] = a
                    real_info['put_sell']['flag'] = 5
                    real_info['put_sell']['quantity'] = 0
                    logging.info(f'Closed put sell position: {put_sell_name} at {put_sell_current_price}')
                    trade_client.close_position(put_sell_name)


        # Save the filled_df to a CSV file if it's not empty
        if not real_info['filled_df'].empty:
            real_info['filled_df'].to_csv(f'trades_{strategy_name}_{dt.now(time_zone).date()}.csv')

        # Store the real_info using pickle
        store(real_info, account_type)



# def chase_order(ord_df):
#     # Check if the order dataframe is not empty
#     if not ord_df.empty:
#         # Filter orders with status 6 (open orders)
#         ord_df = ord_df[ord_df['order_type'] == 'limit']
#         # Iterate through each order in the dataframe
#         for i, o1 in ord_df.iterrows():
#             # Get the symbol name from the order
#             symbol = o1['symbol']
#             # Get the current price of the symbol from the dataframe

#             try:

#                 if i.symbol==symbol:
#                     id1=i.id
#                     s=i.side
#                     print(s)
#                     #get current price of symbol
#                     request_params = OptionLatestQuoteRequest(symbol_or_symbols=symbol)
#                     latest_quote = option_data_client.get_option_latest_quote(request_params)
#                     current_price=(latest_quote.get(symbol).ask_price+latest_quote.get(symbol).bid_price)//2
#                     print(current_price)
#                     l_price=float(i.limit_price)
#                     print(l_price)
#                     q=i.qty
#                     t=i.time_in_force
#                     if current_price > l_price:
#                                     new_lmt_price = round(l_price + 1, 1)
#                     else:
#                                     new_lmt_price = round(l_price - 1, 1)

#                     new_limit_order_data = LimitOrderRequest(
#                                 symbol=symbol,
#                                 limit_price=new_lmt_price,
#                                 qty=q,
#                                 side=s,
#                                 time_in_force=t
#                             )
#                     print(new_limit_order_data)
#                     updated_order=trade_client.replace_order_by_id(id1,new_limit_order_data)
#                     print(f"Modified Order ID: {updated_order.limit_price}")



#             except:
#                 # Print an error message if there is an exception
#                 print('error in chasing order')





# # import time
# while True:

#     ct = dt.now(time_zone)  # Get the current time

#     if ct.second==1:
#         print(ct)
    
#         # get latest quotes by symbol
#         req = StockQuotesRequest(
#             symbol_or_symbols = [ticker],
#         )
#         res = stock_historical_data_client.get_stock_latest_quote(req)
#         print(res.get(ticker))
#         spot_price=(res.get(ticker).ask_price+res.get(ticker).bid_price)/2
#         print(spot_price)

#         df=get_option_data(spot_price)
#         print(df)

#         if account_type == 'PAPER':
#             paper_order(spot_price,df)
#         else:
#             real_order(spot_price,df)
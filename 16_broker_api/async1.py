import time

#sync 
#asynsc programing

#concurrent programing
#multi threading
#asyncio library

#co-routine

# def fun1():
#     print('fun1 first line')
#     time.sleep(1)
#     print('fun1 ends')

# def fun2():
#     print('fun2 first line')
#     time.sleep(1)
#     print('fun2 ends')

# fun1()
# fun2()

#blocking code

#non blocking code


# import asyncio
# async def fun1():
#     print('fun1 first line')
#     await asyncio.sleep(1)
#     print('fun1 ends')

# async def fun2():
#     print('fun2 first line')
#     await asyncio.sleep(1)
#     print('fun2 ends')

# async def fun3():
#     print('fun3 first line')
#     await asyncio.sleep(1)
#     print('fun3 ends')

# async def main():
#     # await fun1()
#     # await fun2()
#     await asyncio.gather(fun1(),fun2(),fun3())

# asyncio.run(main())

import os
import certifi
#for windows ssl error
os.environ['SSL_CERT_FILE'] = certifi.where()


import asyncio
from alpaca.data.historical.crypto import CryptoHistoricalDataClient
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from alpaca.data.timeframe import TimeFrame, TimeFrameUnit
from alpaca.data.requests import CryptoBarsRequest
from alpaca.data.live.crypto import CryptoDataStream
from credentials import api_key, secret_key

# Initialize Historical Data Client
crypto_historical_data_client = CryptoHistoricalDataClient()

# Historical Data Retrieval Function
async def get_history():
    while True:
        symbol = "BTC/USD"
        now = datetime.now(ZoneInfo("America/New_York"))
        req = CryptoBarsRequest(
            symbol_or_symbols=[symbol],
            timeframe=TimeFrame(amount=1, unit=TimeFrameUnit.Minute),
            start=now - timedelta(days=1),
        )
        history_df2 = crypto_historical_data_client.get_crypto_bars(req).df
        print("Historical Data:")
        print(history_df2)
        await asyncio.sleep(60)  # Wait for 10 seconds before fetching again

# Initialize Data Stream Client
crypto_data_stream_client = CryptoDataStream(api_key, secret_key)

# Live Data Stream Handler
async def crypto_data_stream_handler(data):
    print(data)

# Function to Start the Live Stream
async def start_crypto_stream():
    symbol = ['BTC/USD', 'ETH/USD']
    crypto_data_stream_client.subscribe_quotes(crypto_data_stream_handler, *symbol)
    print("Starting Live Data Stream...")
    
    await crypto_data_stream_client._run_forever()  # Await the internal run method

# Main Function to Run Both Tasks Concurrently
async def main():
    # Run both tasks concurrently
    await asyncio.gather(
        get_history(),            # Historical data retrieval every 10 seconds
        start_crypto_stream()     # Live data stream
    )

asyncio.run(main())


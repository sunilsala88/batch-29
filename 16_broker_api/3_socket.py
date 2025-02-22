from alpaca.data.live.crypto import CryptoDataStream

import os
import certifi
#for windows ssl error
os.environ['SSL_CERT_FILE'] = certifi.where()

import pendulum as dt
time_zone="UTC"
print(dt.now(time_zone))

from credentials import api_key,secret_key
crypto_data_stream_client=CryptoDataStream(api_key,secret_key)
async def sample(data):
    print(data)
    print(dt.now(time_zone))
# symbol=['BTC/USD','ETH/USD']
symbol=['BTC/USD','ETH/USD']
# crypto_data_stream_client.subscribe_trades(crypto_data_stream_handler, *symbol)

crypto_data_stream_client.subscribe_quotes(sample, *symbol)
crypto_data_stream_client.run()
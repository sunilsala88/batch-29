

import pendulum as dt
import time
import logging

strategy_name='crypto_sma'
logging.basicConfig(level=logging.INFO, filename=f'{strategy_name}_{dt.now().date()}.log',filemode='a',format="%(asctime)s - %(message)s")

i=10
while True:
    print(dt.now())
    time.sleep(0.1)
    logging.info(dt.now())
    logging.info(str(i))
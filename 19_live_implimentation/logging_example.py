
import datetime
import time
import logging


logging.basicConfig(level=logging.INFO, filename=f'demo.log',filemode='a',format="%(asctime)s - %(message)s")

i=1
while True:
    print(datetime.datetime.now())
    print(i)
    logging.info(i)
    time.sleep(0.2)
    if datetime.datetime.now().minute==42:
        break
    i=i+100




import datetime as dt
import pendulum as pdt1
import pytz

tz1='US/Eastern'
print(dt.datetime.now(tz=pytz.timezone(tz1))+dt.timedelta(days=1))
print(pdt1.now(tz=tz1)+pdt1.duration(days=10))
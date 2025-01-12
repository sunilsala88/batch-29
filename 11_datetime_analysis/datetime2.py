import datetime as dt
import time

ct=dt.datetime.now()
print(ct)

def strategy():
    print("checking strategy condition")

start_hour,start_min=15,23
end_hour,end_min=15,42

start_time=dt.datetime(ct.year,ct.month,ct.day,start_hour,start_min,0)
end_time=dt.datetime(ct.year, ct.month, ct.day, end_hour, end_min, 0)

print(start_time)
print(end_time)

while True:
    ct=dt.datetime.now()
    if start_time<ct<end_time:
        if ct.second==1 and ct.minute in range(0,60,5):#[0,5,10,15...55]
            strategy()
    else:
        break

    time.sleep(1)
    print(dt.datetime.now())

print('we have reached end time')
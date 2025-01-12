# import datetime
# import datetime as dt
from datetime import datetime,timedelta


dt1=datetime(2023,12,12,23,33,44)
print(dt1)

u1=timedelta(days=1)

t=dt1.time()
d=dt1.date()
print(t)
print(d)
print(dt1+u1)

print(dt1.day)
print(dt1.minute)
print(dt1.weekday())


# get all thursdays of 2025 jan
thurdays=[]
current_day=datetime(2025,1,1)
while True:
    if current_day.day==31:
        break
    if current_day.weekday()==3:
        thurdays.append(current_day)
        print(current_day)
    # print(current_day)
    current_day=current_day+timedelta(days=1)




#date
#time
#datetime 
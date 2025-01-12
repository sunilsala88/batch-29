# import datetime
# import datetime as dt
from datetime import datetime,timedelta,date,time


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
        print(current_day.date())
    # print(current_day)
    current_day=current_day+timedelta(days=1)




#date
#time
#datetime 


#datetime to epoch
print(dt1.timestamp())

#epoch time to datetime
n=1736674158
dt2=datetime.fromtimestamp(n)
print(dt2)

current_time=datetime.now()
print(current_time)

#convert string to datetime
s="24 Jan 2025"
f='%d %b %Y'
dt3=datetime.strptime(s,f)
print(dt3)

#datetime to string
s=dt1.strftime("%Y %B")
print(s)


s='30-05-03 00 2024-Jan/23'
f='%M-%H-%S 00 %Y-%b/%d'
dt4=datetime.strptime(s, f)
print(dt4.timestamp())
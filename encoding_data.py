'''
need to install holidays
pip install holidays

https://github.com/dr-prodigy/python-holidays
'''

import numpy as np
import pandas as pd
import datetime as dt
import holidays

from taxi_pakage import haversine_np

datezero = dt.datetime(2016, 1, 1, 0, 0, 1) # 기준

def strptime(x):
    return dt.datetime.strptime(x, "%Y-%m-%d %H:%M:%S")
def date_to_zero(x):
    return int((x-datezero).days)
def time_to_zero(x):
    return int((x-datezero).seconds)
def week_num(x):
    return int(x.weekday())

us_holidays = holidays.US(state='NY', years=2016)

def holiday(x):
    if x in us_holidays:
        return 1
    else:
        x = x.weekday()
    if x > 4:
        return 1
    else:
        return 0

def holiday_Fri(x): #with Friday
    if x in us_holidays:
        return 1
    else:
        x = x.weekday()
    if x > 3:
        return 1
    else:
        return 0


taxi = pd.read_csv('train.csv')
taxi['dist'] = haversine_np(taxi['pickup_longitude'], taxi['pickup_latitude'], taxi['dropoff_longitude'], taxi['dropoff_latitude'])

taxi['id'] = taxi['id'].apply(lambda x: x[2:])
taxi['store_and_fwd_flag'] = taxi['store_and_fwd_flag'].apply(lambda x: 0 if x == 'N' else 1)
taxi['pickup_datetime'] = taxi['pickup_datetime'].apply(strptime)
taxi['dropoff_datetime'] = taxi['dropoff_datetime'].apply(strptime)
taxi['pick_date'] = taxi['pickup_datetime'].apply(date_to_zero)
taxi['pick_time'] = taxi['pickup_datetime'].apply(time_to_zero)
taxi['drop_time'] = taxi['dropoff_datetime'].apply(time_to_zero)

taxi['holiday'] = taxi['pickup_datetime'].apply(holiday)
taxi['holiday_Fri'] = taxi['pickup_datetime'].apply(holiday_Fri)
taxi['weekday'] = taxi['pickup_datetime'].apply(week_num)


temp = taxi['trip_duration'] # for easy slicing
taxi = taxi.drop(['pickup_datetime', 'dropoff_datetime', 'trip_duration'], axis=1)
taxi['trip_duration'] = temp

taxi.to_csv("edited_taxi.csv", index = False)

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
    return int(x.weekday()) + 1 # erase 0

us_holidays = holidays.US(state='NY', years=2016)

def holiday(x):
    if x in us_holidays:
        return 1
    else:
        x = x.weekday()
    if x > 4:
        return 0
    else:
        return 0

taxi = pd.read_csv('train.csv')
taxi['dist'] = haversine_np(taxi['pickup_longitude'], taxi['pickup_latitude'], taxi['dropoff_longitude'], taxi['dropoff_latitude'])

taxi['id'] = taxi['id'].apply(lambda x: x[2:])
taxi['store_and_fwd_flag'] = taxi['store_and_fwd_flag'].apply(lambda x: 0 if x == 'N' else 1)

taxi['pickup_datetime2'] = taxi['pickup_datetime'].astype('datetime64[ns]')
taxi['dropoff_datetime2'] = taxi['dropoff_datetime'].astype('datetime64[ns]')
taxi["year"] = taxi['pickup_datetime2'].dt.year
taxi["month"] = taxi['pickup_datetime2'].dt.month
taxi["day"] = taxi['pickup_datetime2'].dt.day
taxi["hour"] = taxi['pickup_datetime2'].dt.hour

taxi['pickup_datetime'] = taxi['pickup_datetime'].apply(strptime)
taxi['dropoff_datetime'] = taxi['dropoff_datetime'].apply(strptime)
taxi['pick_date'] = taxi['pickup_datetime'].apply(date_to_zero)
taxi['pick_time'] = taxi['pickup_datetime'].apply(time_to_zero)

taxi['holiday'] = taxi['pickup_datetime'].apply(holiday)
taxi['weekday'] = taxi['pickup_datetime'].apply(week_num)


temp = taxi['trip_duration'] # for easy slicing

taxi = taxi.drop(['pickup_datetime', 'dropoff_datetime', 'pickup_datetime2', 'dropoff_datetime2', 'trip_duration'], axis=1)

taxi['trip_duration'] = temp

taxi.to_csv("edited_taxi.csv", index = False)

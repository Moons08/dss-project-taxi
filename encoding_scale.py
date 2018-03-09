from taxi_pakage import *

taxi = pd.read_csv('edited_taxi.csv')

# for scaled data
feature_n, features = get_features(taxi)
test = dmatrix("{}".format(features), taxi, return_type ="dataframe")
test = test.drop(["id", "store_and_fwd_flag", "holiday_Fri"], axis = 1)
feature_n, features = get_features(test, 2, -3, scale=True)
test = dmatrix("trip_duration + vendor_id +weekday + holiday + {}".format(features), test, return_type ="dataframe")
test = test.rename(index=str,
            columns={'scale(passenger_count)':'passenger_count',
                         'scale(pickup_longitude)':'pickup_longitude',
                         'scale(pickup_latitude)':'pickup_latitude',
                         'scale(dropoff_longitude)':'dropoff_longitude',
                         'scale(dropoff_latitude)':'dropoff_latitude',
                         'scale(dist)':'dist',
                         'scale(pick_date)' : 'pick_date',
                         'scale(pick_time)'  : 'pick_time',
                         'scale(drop_time)' : 'drop_time',
                    }
           )

test.to_csv("scaled_taxi.csv", index = False)

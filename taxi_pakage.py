import pandas as pd
import numpy as np
import scipy as sp

import statsmodels.api as sm
import statsmodels.formula.api as smf
import statsmodels.stats.api as sms
import sklearn as sk

import datetime as dt
from patsy import dmatrix

import matplotlib.pylab as plt
from mpl_toolkits.mplot3d import Axes3D

import seaborn as sns
sns.set()
sns.set_style("whitegrid")
sns.set_color_codes(palette="muted")

def get_features(data, start_num=0, end_num=None, scale=False):
    """
    from data, choose the columns to use OLS
    (default is all columns)

    """
    features = list(data.columns)[start_num:end_num]
    feature_n = len(features)

    if scale:
        features = list(map(lambda x: "scale({})".format(x), features))
        features = " + ".join(features)

    else:
        features = " + ".join(features)

    return feature_n, features

def erase_outlier_np(result, data, total_feature, category=False, dropped=False):
    """
    get the fitted model result, then erase outliers in data,
    by Fox' Outlier Recommendation.

    print the number of erased outlier
    return arranged data, dropped data(when True)
    """

    influence = result.get_influence()

    if category:
        fox_cr = 4 / (len(data) - total_feature)
    else:
        fox_cr = 4 / (len(data) - total_feature - 1)

    cooks_d2, pvals = influence.cooks_distance
    idx = np.where(cooks_d2 > fox_cr)[0]

    dropped_data = data.iloc[idx]
    data.drop(data.index[idx])
    data.reset_index(drop=True, inplace=True)

    if dropped:

        return data, dropped_data

    return data

def haversine_np(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)

    All args must be of equal length.

    """

    lon1, lat1, lon2, lat2 = map(np.radians, [lon1, lat1, lon2, lat2])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = np.sin(dlat/2.0)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2.0)**2

    c = 2 * np.arcsin(np.sqrt(a))
    km = 6367 * c

    return km

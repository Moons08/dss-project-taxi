def get_features(data, start_num=0, end_num=None):
    """
    from data, choose the columns to use OLS
    (default is all columns)

    """
    features = list(data.columns)[start_num:end_num]
    feature_n, features = len(features), " + ".join(features)

    return feature_n, features

def erase_outlier_np(result, data, total_feature, category=False):
    """
    get the fitted model result,
    then erase outliers in data,
    by Fox' Outlier Recommendation.

    print the number of erased outlier
    return arranged data

    need to import numpy as np
    """
    influence = result.get_influence()

    if category:
        fox_cr = 4 / (len(data) - (total_feature) -1)
    else:
        fox_cr = 4 / (len(data) - (total_feature + 1) - 1)

    cooks_d2, pvals = influence.cooks_distance
    idx = np.where(cooks_d2 > fox_cr)[0]

    data = data.drop(idx)
    data.reset_index(drop=True, inplace=True)

    print(len(idx))

    return data

def haversine_np(lon1, lat1, lon2, lat2):
    import numpy as np
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

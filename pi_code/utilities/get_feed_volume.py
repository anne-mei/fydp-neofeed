import os
import numpy as np
import pandas as pd

curr_folder = os.path.dirname(os.path.abspath(__file__))
feed_csv_folder = os.path.join(curr_folder, '..', 'feed_volume_charts')

feed_range_dict = {
    0: [400, 499],
    1: [500, 599],
    2: [600, 699],
    3: [700, 799],
    4: [800, 999],
    5: [1000, 1249],
    6: [1250, 1499],
    7: [1500, 1749],
    8: [1750, 1999],
    9: [2000, 2249]
}


def getIndex(a):
    ranges = list(feed_range_dict.values())
    r = [i for i, r in enumerate(ranges) if np.logical_and(a>=r[0], a<=r[1])]    
    return r[0] if r else -1


def get_feed_volume(weight, session_num, day_num):
    """
    weight: in kg
    """
    weight_g = weight * 1000  # convert weight from kg to g

    # find range the weight is in
    r = getIndex(weight_g)
    if r == -1:
        print('weight is out of range')
        return r
    
    feed_range = feed_range_dict[r]

    # find appropriate csv file name
    csv_name = 'feed_vol_' + str(feed_range[0]) + '-' + str(feed_range[1]) + '.csv'
    print('accessing', csv_name)

    # access csv file for feed volume
    df = pd.read_csv(os.path.join(feed_csv_folder, csv_name), index_col=0)
    feed_volume = df.loc[day_num, 'feedsession' + str(int(session_num))]

    return feed_volume

# example on how to call
# feed_volume = get_feed_volume(0.5, 7, 6)
# print(feed_volume)


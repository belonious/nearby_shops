import os
import pandas as pd
import numpy as np
path = os.path.join(os.path.dirname(__file__), '..', 'data')


try:
    SHOPS = pd.read_csv('{}/shops.csv'.format(path))
    PRODUCTS = pd.read_csv('{}/products.csv'.format(path))
    TAGS = pd.read_csv('{}/tags.csv'.format(path))
    TAGGINGS = pd.read_csv('{}/taggings.csv'.format(path))
    tags_df = pd.merge(TAGS, TAGGINGS, 'inner', left_on='id', right_on='tag_id')
    shops_with_tags_df = pd.merge(tags_df, SHOPS, 'inner', left_on='shop_id', right_on='id')
except Exception as e:
    print 'Failed to load data'
    print e.message
    exit(0)


def haversine_np(lon1, lat1, lon2, lat2):
    """
    link : https://stackoverflow.com/questions/29545704/fast-haversine-approximation-python-pandas
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    lon1, lat1, lon2, lat2 = map(np.radians, [lon1, lat1, lon2, lat2])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = np.sin(dlat/2.0)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2.0)**2

    c = 2 * np.arcsin(np.sqrt(a))
    km = 6367 * c
    return km


def get_shops_with_tags(tag_list):
    '''
    filtering shops such as at least having one tag
    :param tag_list:
    :return: df
    '''
    return shops_with_tags_df[shops_with_tags_df['tag'].isin(tag_list)]


def query_data(count, lat, lng, radius, tags):
    '''
    Queries the data according to params
    note: quantity filter for available products?
    :param count: int
    :param lat: float
    :param lng: float
    :param radius: int
    :param tags: list
    :return: df
    '''
    shops = SHOPS.copy()
    if len(tags) > 0:
        shops = get_shops_with_tags(tags)
    shops['dist'] = shops.apply(lambda row: haversine_np(lng,
                                                         lat,
                                                         row['lng'],
                                                         row['lat']),
                                axis=1)
    near_shops = shops[shops.dist < radius]
    return pd.merge(near_shops,
                    PRODUCTS,
                    'inner',
                    left_on='id',
                    right_on='shop_id') \
        .sort_values('popularity',
                     ascending=False) \
        .head(count)

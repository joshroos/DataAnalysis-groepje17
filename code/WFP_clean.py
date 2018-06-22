# wfp_clean.py

# Joshua de Roos
# Data Visualisation - week 1
# 5 juni 2018

# This program contains functions for cleaning the data of
# the World Food Prices database.

import matplotlib as plt
import pandas as pd
import numpy as np
from pandas import ExcelWriter


# adds missing data and changes inconsistent names
def data_clean(data):
    # replaces 'NaN values with logical data from Wikipedia
    replace = ['National Average', 'Jammu Kasjmir']
    data[data["mkt_name"] == 'National Average'] = data[data["mkt_name"] ==
                                        'National Average'].fillna(replace[0])
    data[data["mkt_name"] == 'Jammu'] = data[data["mkt_name"] ==
                                        'Jammu'].fillna(replace[1])
    data[data["mkt_name"] == 'Srinagar'] = data[data["mkt_name"] ==
                                        'Srinagar'].fillna(replace[1])

    # removes or replaces minor inconsistencies
    data["mkt_name"].replace('m. Kyiv', 'Kyiv')
    data[(data["cur_name"] == 'AFN') &
         (data["mp_year"] < 2003)].replace('AFN', 'AFA')
    data.adm1_name = [x.strip('$') for x in data.adm1_name]
    data.adm1_name = [x.strip('#') for x in data.adm1_name]
    data.adm1_name = [x.replace('_', ' ') for x in data.adm1_name]
    data.mkt_name = [x.replace('_', ' ') for x in data.mkt_name]
    data.mkt_name = [x.replace('-', ' ') for x in data.mkt_name]
    data["cur_name"] = data["cur_name"].replace('Somaliland Shilling', 'SOS')

    # removes column with source of each data point
    data = data.drop(columns=['mp_commoditysource'])

    return data


# removes small inconsistencies in product names
def data_aggregate(data):
    # some manual changes
    data.loc[data['cm_name'].str.contains('meal'), 'cm_name'] = 'Flour'
    data.loc[data['cm_name'].str.contains('flour'), 'cm_name'] = 'Flour'
    data.loc[data['cm_name'].str.contains('Ghee'), 'cm_name'] = 'Butter'
    data.loc[data['cm_name'].str.contains('Peanut'), 'cm_name'] = 'Groundnuts'
    data.loc[data['cm_name'].str.contains('Tamarillo'), 'cm_name'] = 'Tomatoes'
    data.loc[data['cm_name'].str.contains('Poultry'), 'cm_name'] = 'Meat'

    categories = ['Apples', 'Bananas', 'Beans', 'Bread', 'Cassava', 'Cheese',
                'Chickpeas', 'Chili', 'Coffee', 'Cowpeas', 'Cucumbers', 'Eggs',
                'Exchange Rate', 'Fish', 'Gari', 'Garlic', 'Groundnuts',
                'Lentils', 'Livestock', 'Maize', 'Meat', 'Milk', 'Millet',
                'Noodles', 'Oil', 'Onions', 'Oranges', 'Peas', 'Plantains',
                'Potatoes', 'Salt', 'Sorghum', 'Sugar', 'Tea', 'Tomatoes',
                'Wage', 'Water', 'Wheat flour', 'Yam', 'Rice']

    # changes all products to names from list 'categories'
    for category in categories:
        data.loc[data['cm_name'].str.contains(category), 'cm_name'] = category

    return data

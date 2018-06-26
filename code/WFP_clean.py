# Joshua de Roos en Ellen Bogaards
# 5 juni 2018
# Dit programma maakt van het csv-bestand van de WFP een overzichtelijke tabel

import matplotlib as plt
import pandas as pd
import numpy as np
from pandas import ExcelWriter

# maakt de data schoon
def data_clean(data):
    # vult de 'NaN' waarden met verschillende invoeren
    data[data["mkt_name"] == 'National Average'] = data[data["mkt_name"] == 'National Average'].fillna('National Average')
    data[data["mkt_name"] == 'Jammu'] = data[data["mkt_name"] == 'Jammu'].fillna('Jammu Kasjmir')
    data[data["mkt_name"] == 'Srinagar'] = data[data["mkt_name"] == 'Srinagar'].fillna('Jammu Kasjmir')

    # verandert inconsistencies
    data["mkt_name"] = data["mkt_name"].replace('m. Kyiv', 'Kyiv')
    data[(data["cur_name"] == 'AFN') & (data["mp_year"] < 2003)] = data[(data["cur_name"] == 'AFN') & (data["mp_year"] < 2003)].replace('AFN', 'AFA')
    data.adm1_name = [x.strip('$') for x in data.adm1_name]
    data.adm1_name = [x.strip('#') for x in data.adm1_name]
    data.adm1_name = [x.replace('_', ' ') for x in data.adm1_name]
    data.mkt_name = [x.replace('_', ' ') for x in data.mkt_name]
    data.mkt_name = [x.replace('-', ' ') for x in data.mkt_name]
    data["cur_name"] = data["cur_name"].replace('Somaliland Shilling', 'SOS')

    # verwijdert source van metingen 
    data = data.drop(columns=['mp_commoditysource'])

    return data

# functie die data samenvoegt
def data_aggregate(data):
    data.loc[data['cm_name'].str.contains('meal'), 'cm_name'] = 'Flour'
    data.loc[data['cm_name'].str.contains('flour'), 'cm_name'] = 'Flour'
    data.loc[data['cm_name'].str.contains('Ghee'), 'cm_name'] = 'Butter'
    data.loc[data['cm_name'].str.contains('Peanut'), 'cm_name'] = 'Groundnuts'
    #data.loc[data['cm_name'].str.contains('oes (paste)'), 'cm_name'] = 'Paste (tomato)'
    #data.loc[data['cm_name'].str.contains('oes (paste)'), 'cm_name'] = 'Paste (tomato)'
    data.loc[data['cm_name'].str.contains('Tamarillos'), 'cm_name'] = 'Tomatoes'
    data.loc[data['cm_name'].str.contains('Poultry'), 'cm_name'] = 'Meat'

    
    categories = ['Apples', 'Bananas', 'Beans', 'Bread', 'Cassava', 'Cheese', 'Chickpeas',
    'Chili', 'Coffee', 'Cowpeas','Cucumbers', 'Eggs', 'Exchange Rate', 'Fish', 'Gari',
    'Garlic', 'Groundnuts', 'Lentils', 'Livestock', 'Maize', 'Meat', 'Milk', 'Millet',
    'Noodles', 'Oil', 'Onions', 'Oranges', 'Peas', 'Plantains', 'Potatoes',
    'Salt', 'Sorghum', 'Sugar', 'Tea', 'Tomatoes', 'Wage', 'Water', 'Wheat flour', 'Yam', 'Rice']

    for category in categories:
        data.loc[data['cm_name'].str.contains(category), 'cm_name'] = category

    return data


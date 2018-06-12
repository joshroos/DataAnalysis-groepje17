# 12-06-2018
# Joshua de Roos
# Dit programma normaliseert de waarden van de eenheden en valuta van het
# pandas dataframe van de WFP database.

import matplotlib as plt
import pandas as pd
import numpy as np
from pandas import ExcelWriter
import re

import WFP_clean

# lees bestand in
data_WFP = pd.read_csv('../data/WFPVAM_FoodPrices_05-12-2017.csv', encoding='latin-1')

data_WFP = WFP_clean.data_clean(data_WFP)
#data_WFP = WFP_clean.data_aggregate(data_WFP)

def data_normalise(data):
    units = data["um_name"].unique()
    gram_to_kg = []
    kg_to_kg = []
    liter_to_liter = []
    ml_to_liter = []

    for value in units:
        if ' G' in value:
            gram_to_kg.append(value)
        elif ' KG' in value:
            kg_to_kg.append(value)
        elif ' L' in value:
            liter_to_liter.append(value)
        elif ' ML' in value:
            ml_to_liter.append(value)

    for unit in gram_to_kg:
        grams = int(re.search(r'\d+', unit).group())
        prices = data.loc[data['um_name'].str.contains(unit), 'mp_price']
        prices = prices * (1000/grams)
        data.loc[data['um_name'].str.contains(unit), 'mp_price'] = prices
        data.loc[data['um_name'].str.contains(unit), 'um_name'] = 'KG'

    for unit in kg_to_kg:
        kg = int(re.search(r'\d+', unit).group())
        prices = data.loc[data['um_name'].str.contains(unit), 'mp_price']
        prices = prices / kg
        data.loc[data['um_name'].str.contains(unit), 'mp_price'] = prices
        data.loc[data['um_name'].str.contains(unit), 'um_name'] = 'KG'

    for unit in liter_to_liter:
        liter = int(re.search(r'\d+', unit).group())
        prices = data.loc[data['um_name'].str.contains(unit), 'mp_price']
        prices = prices / liter
        data.loc[data['um_name'].str.contains(unit), 'mp_price'] = prices
        data.loc[data['um_name'].str.contains(unit), 'um_name'] = 'L'
    
    for unit in ml_to_liter:
        ml = int(re.search(r'\d+', unit).group())
        prices = data.loc[data['um_name'].str.contains(unit), 'mp_price']
        prices = prices * (1000/ml)
        data.loc[data['um_name'].str.contains(unit), 'mp_price'] = prices
        data.loc[data['um_name'].str.contains(unit), 'um_name'] = 'L'

    return data

#data_WFP = data_normalise(data_WFP)

valutas = data_WFP['cur_name'].unique()
valuta = [e for e in valutas if e not in ('USD', 'AFA')]
valuta.sort()

data_exchange = pd.read_excel('../data/exchangerate_simple.xlsx')

currency = data_WFP['cur_name'] == 'USD'
year = data_WFP['mp_year'] == 2015
#print(data_WFP.loc[currency, 'adm0_name'])
dollars  = data_WFP[currency]['adm0_name'].unique()

for land in dollars:
    val = data_WFP[data_WFP['adm0_name'] == land]['cur_name'].unique()
    print(val)


#print(len(data_exchange["1992"]))
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
data_WFP = WFP_clean.data_aggregate(data_WFP)

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

    special_units = ['MT', 'Marmite']
    factor = [1000, 2.7]

    for i in range(len(special_units)):
        prices = data.loc[data['um_name'].str.contains(special_units[i]), 'mp_price']
        prices = prices / factor[i]
        data.loc[data['um_name'].str.contains(special_units[i]), 'mp_price'] = prices
        data.loc[data['um_name'].str.contains(special_units[i]), 'um_name'] = 'KG'
    return data

data_WFP = data_normalise(data_WFP)

data_exchange = pd.read_excel('../data/exchangerate_simple.xlsx')

def valuta_normalise(data_WFP, data_exchange):
    data_WFP['old currency'] = data_WFP['mp_price']
    years = [str(x) for x in range(1992, 2018)]
    countries = list(data_exchange['Country Name'])

    for country in countries:
        for year in years:
            country_exchange = data_exchange['Country Name'] == country
            rate = list(data_exchange[country_exchange][year])

            
            country_wfp = data_WFP['adm0_name'] == country
            year_wfp = data_WFP['mp_year'] == int(year)

            prices  = data_WFP.loc[(country_wfp) & (year_wfp), 'mp_price']
            prices = prices / rate[0]
            data_WFP.loc[(country_wfp) & (year_wfp), 'mp_price'] = prices

    return data_WFP

valuta_normalise(data_WFP, data_exchange)

data_WFP.to_csv('data_normalised.csv')

# writer = ExcelWriter('data_normalised.xlsx')
# data_WFP.to_excel(writer,'Sheet5')
# writer.save()
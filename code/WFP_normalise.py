# 12-06-2018
# Joshua de Roos
# This program normalises all units and currencies of the WFP database and
# writes the new dataframe to a new csv file

import matplotlib as plt
import pandas as pd
import numpy as np
from pandas import ExcelWriter
import re
import wfp_clean

# reads necessary files
filename = '../data/WFPVAM_FoodPrices_05-12-2017.csv'
df_wfp = pd.read_csv(filename, encoding='latin-1')
data_exchange = pd.read_excel('../data/exchangerate_simple.xlsx')


# converts different units to the same unit
def unit_conversion(data, conversion, unit, factor):
    for unit in conversion:
        amount = int(re.search(r'\d+', unit).group())
        prices = data.loc[data['um_name'].str.contains(unit), 'mp_price']
        prices = prices / (amount * factor)
        data.loc[data['um_name'].str.contains(unit), 'mp_price'] = prices
        data.loc[data['um_name'].str.contains(unit), 'um_name'] = unit

    return data


# converts a number of special units to standard unit
def special_conversion(data, units, factor, new_unit):
    for i in range(len(units)):
        prices = data.loc[data['um_name'].str.contains(units[i]), 'mp_price']
        prices = prices / factor[i]
        data.loc[data['um_name'].str.contains(units[i]), 'mp_price'] = prices
        data.loc[data['um_name'].str.contains(units[i]), 'um_name'] = new_unit

    return data


# converts units that differ per good to standard unit
def odd_conversions(data):
    old_unit = ['Unit', 'Unit', 'Month', 'KG', 'KG', '30 pcs', '10 pcs', 'KG',
                'Dozen', 'Unit', 'Unit', 'KG']
    special_products = ['Bread', 'Livestock', 'Wage', 'Fuel (diesel)', 'Oil',
                        'Eggs', 'Eggs', 'Eggs', 'Eggs', 'Milk', 'Cheese',
                        'Milk']
    factor = [0.7, 1, 30, 1.1299435028249, 1.086957, 30, 10, 20, 12, 7.5, 1,
              1.03]
    new_unit = ['KG', 'Head', 'Day', 'L', 'L', 'Unit', 'Unit', 'Unit', 'Unit',
                'L', 'KG', 'L']

    for i in range(len(special_products)):
        unit = data['um_name'] == old_unit[i]
        product = data['cm_name'] == special_products[i]
        prices = data.loc[unit & product, 'mp_price']
        prices = prices / factor[i]
        data.loc[unit & product, 'mp_price'] = prices
        data.loc[unit & product, 'um_name'] = new_unit[i]

    return data


# normalises the units in the WFP database
def data_normalise(data):
    units = data["um_name"].unique()
    gram_to_kg, kg_to_kg, liter_to_liter, ml_to_liter = ([] for i in range(4))

    # collects all regular units in list for conversion
    for value in units:
        if ' G' in value:
            gram_to_kg.append(value)
        elif ' KG' in value:
            kg_to_kg.append(value)
        elif ' L' in value:
            liter_to_liter.append(value)
        elif ' ML' in value:
            ml_to_liter.append(value)

    # converts regular units
    data = unit_conversion(data, gram_to_kg, 'KG', 0.001)
    data = unit_conversion(data, kg_to_kg, 'KG', 1)
    data = unit_conversion(data, ml_to_liter, 'L', 0.001)
    data = unit_conversion(data, liter_to_liter, 'L', 1)

    # converts number of special units
    special_units = ['MT', 'Marmite', 'Pound', 'Cuartilla', 'Loaf', 'Libra']
    factor = [1000, 2.7, 0.45359, 2.875575, 0.7, 0.45359]
    data = special_conversion(data, special_units, factor, 'KG')

    special_units = ['Gallon']
    factor = [3.78541178]
    data = special_conversion(data, special_units, factor, 'L')

    data = odd_conversions(data)

    return data


# converts all prices to prices in USD
def valuta_normalise(df_wfp, data_exchange):
    df_wfp['old currency'] = df_wfp['mp_price']
    years = [str(x) for x in range(1992, 2018)]
    countries = list(data_exchange['Country Name'])

    # converts all currencies per country using year to year exchange rates
    for country in countries:
        for year in years:
            country_exchange = data_exchange['Country Name'] == country
            rate = list(data_exchange[country_exchange][year])

            country_wfp = df_wfp['adm0_name'] == country
            year_wfp = df_wfp['mp_year'] == int(year)

            prices = df_wfp.loc[(country_wfp) & (year_wfp), 'mp_price']
            prices = prices / rate[0]
            df_wfp.loc[(country_wfp) & (year_wfp), 'mp_price'] = prices

    return df_wfp


# function calls
df_wfp = wfp_clean.data_clean(df_wfp)
df_wfp = wfp_clean.data_aggregate(df_wfp)
df_wfp = data_normalise(df_wfp)
valuta_normalise(df_wfp, data_exchange)

# writes processed data to new csv file
df_wfp.to_csv('WFP_data_normalised.csv')

# writer = ExcelWriter('data_normalised.xlsx')
# df_wfp.to_excel(writer,'Sheet5')
# writer.save()

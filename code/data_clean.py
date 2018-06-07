# Joshua de Roos en Ellen Bogaards
# 5 juni 2018
# Dit programma maakt van het csv-bestand van de WFP een overzichtelijke tabel

import matplotlib as plt
import pandas as pd
import numpy as np

# lees bestand in
data = pd.read_csv('../data/WFPVAM_FoodPrices_05-12-2017.csv', encoding='latin-1')
failed_columns = []


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


# controleert op missende data of dummy invoer
for column in data:
    unique_values = data[column].unique()
    
    try:
        unique_values.sort()
    except:
        failed_columns.append(column)

    if all(isinstance(item, str) for item in unique_values):
        print(column)
        for value in unique_values:
            print(value)

        print('\n')

        text = input()




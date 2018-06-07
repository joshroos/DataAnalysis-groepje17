# Joshua de Roos en Ellen Bogaards
# 5 juni 2018
# Dit programma maakt van het csv-bestand van de WFP een overzichtelijke tabel

import matplotlib as plt
import pandas as pd
import numpy as np

# lees bestand in
data = pd.read_csv('../data/WFPVAM_FoodPrices_05-12-2017.csv', encoding='latin-1')
failed_columns = []

# controleert op missende data of dummy invoer
for column in data:
    unique_values = data[column].unique()
    print(column)
    
    try:
        unique_values.sort()
    except:
        failed_columns.append(column)

    for value in unique_values:
       # print(value)
       continue

    print('\n')

# vult de 'NaN' waarden met verschillende invoeren
data[data["mkt_name"] == 'National Average'] = data[data["mkt_name"] == 'National Average'].fillna('National Average')
data[data["mkt_name"] == 'Jammu'] = data[data["mkt_name"] == 'Jammu'].fillna('Jammu Kasjmir')
data[data["mkt_name"] == 'Srinagar'] = data[data["mkt_name"] == 'Srinagar'].fillna('Jammu Kasjmir')

# verwijdert source van metingen 
data = data.drop(columns=['mp_commoditysource'])


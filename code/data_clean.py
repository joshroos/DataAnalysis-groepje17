# Joshua de Roos en Ellen Bogaards
# 5 juni 2018
# Dit programma maakt van het csv-bestand van de WFP een overzichtelijke tabel

import matplotlib as plt
import pandas as pd

data = pd.read_csv('../data/WFPVAM_FoodPrices_05-12-2017.csv', encoding='latin-1')

# hier lees ik alle landen in en schrijf deze naar een ander bestand
countries = data['adm0_name'].unique()
all_countries = open('../data/BNP data/countries.csv', 'w')
for country in countries:
    all_countries.write("%s," % country)


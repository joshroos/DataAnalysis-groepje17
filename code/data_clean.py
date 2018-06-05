# Joshua de Roos en Ellen Bogaards
# 5 juni 2018
# Dit programma maakt van het csv-bestand van de WFP een overzichtelijke tabel

import matplotlib as plt
import pandas as pd



data = pd.read_csv('/Users/joshua/Documents/GitHub/DataAnalysis-groepje17/data/WFPVAM_FoodPrices_05-12-2017.csv')

print(data)
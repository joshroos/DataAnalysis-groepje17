# Joshua de Roos en Ellen Bogaards
# 5 juni 2018
# Dit programma maakt van het csv-bestand van de WFP een overzichtelijke tabel

import matplotlib as plt
import pandas as pd

# Transformeert het csv bestand naar panda dataframe
data = pd.read_csv('../data/WFPVAM_FoodPrices_05-12-2017.csv', encoding='latin-1')

for line in data["mp_year"]:
    if line < 1992 or type(line) is not int or line > 2017:
        print(line)

    if type(line) is None:
        print(line)

for line in data["mp_price"]:
    if type(line) is not int and type(line) is not float:
        print(line)

    if type(line) is None:
        print(line)

for column in data:
    for line in data[column]:
        if type(line) is None or line == '' or line == 'NaN':
            print('Hier')

        if type(line) is not str:    
            if line < 0:
                print('Hier')

landen = data["adm0_name"].unique()
valuta = data["cur_name"].unique()
goederen = data["cm_name"].unique()
afzetmarkt = data["pt_name"].unique()
eenheid = data["um_name"].unique()
print(eenheid)

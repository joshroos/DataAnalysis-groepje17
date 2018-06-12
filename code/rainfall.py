import matplotlib as plt
import pandas as pd
import io
from pandas import ExcelWriter

rainfall = pd.read_csv('../data/EXCEL_RAINFALL_COUNTRIES.csv',header=0, sep=',', error_bad_lines=False, encoding = 'latin-1')
#print(rainfall_1991_2015)
counter = 0
rainfall['per_year'] = 0
for i in range(21301):
    if counter < 12:
        rainfall['per_year'][i] += rainfall['pr'][i]
        counter += 1
        print(rainfall['per_year'])
    else:
        print("hoi")

#elke 12 waardes moeten samengevoegd worden maar lukt niet

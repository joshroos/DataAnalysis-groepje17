import matplotlib as plt
import pandas as pd
import io
from pandas import ExcelWriter
import WFP_clean

rainfall = pd.read_csv('../data/EXCEL_RAINFALL_COUNTRIES.csv',header=0, sep=',', error_bad_lines=False, encoding = 'latin-1')
data_WFP = pd.read_csv('../data/WFPVAM_FoodPrices_05-12-2017.csv', encoding='latin-1')
countrycodes = pd.read_csv('../data/countrycodes.csv', header = 0, sep = ',', error_bad_lines=False, encoding = 'latin-1')
data_WFP = WFP_clean.data_clean(data_WFP)

download = "rainfall_better.csv" 
csv = open(download, "w") 
columnTitleRow = "country, year, pr_total\n"
csv.write(columnTitleRow)

countries = rainfall['Country_Code'].unique()

for country in countries:
    for year in range(1991, 2015):
        pr_new = rainfall.loc[(rainfall['Year'] == year) &  (rainfall['Country_Code'] == country), 'pr']
        pr_total = pr_new.sum()
        country_name = list(countrycodes.loc[countrycodes['alpha-3'] == country, 'name'])
        row = str(country_name[0]) + "," + str(year) + "," + str(pr_total) + "\n"
        csv.write(row)


# 12-06-2018
# Joshua de Roos
# Exploratory Data Analysis van Joshua

from bokeh.plotting import figure
from bokeh.io import output_file, show
import matplotlib as plt
import pandas as pd
import io
from pandas import ExcelWriter

rainfall = pd.read_csv('../data/rainfall_better.csv',header=0, sep=',', error_bad_lines=False, encoding = 'latin-1')
exchangerate = pd.read_excel('../data/exchangerate_simple.xlsx',header=0, sep=',', error_bad_lines=False, encoding = 'latin-1')
data_WFP = pd.read_csv('../data/WFP_data_normalised.csv', encoding='latin-1')

goed1 = data_WFP.loc[data_WFP['cm_name'].str.contains('Bread'), 'adm0_name'].unique()
goed2 = data_WFP.loc[data_WFP['cm_name'].str.contains('Wheat'), 'adm0_name'].unique()

goed = list(set(goed1) & set(goed2))
goed.sort()

units = data_WFP.loc[data_WFP['cm_name'] == 'Flour', 'um_name'].unique()
units.sort()

for unit in units:
    print(unit)
# for goederen in goed:
#     print(goederen)

# print(len(goed))

# print(data_WFP.loc[(data_WFP['cm_name'] == 'Flour') & (data_WFP['mp_price'] > 5) & (data_WFP['mp_year'] == 2008), 'adm0_name'])

years = [x for x in range(1992, 2018)]
brood_prijzen = []
meel_prijzen = []
for year in years:

    brood = data_WFP.loc[(data_WFP['cm_name'] == 'Bread') & (data_WFP['mp_year'] == year), 'mp_price']
    meel = data_WFP.loc[(data_WFP['cm_name'] == 'Flour') & (data_WFP['mp_year'] == year) & (data_WFP['adm0_name'] != 'Somalia'), 'mp_price']
    meel_prijzen.append(meel.mean())
    brood_prijzen.append(brood.mean())

output_file("test.html")

g = figure()

g.line(years,brood_prijzen, line_width=3, color = "blue")
g.line(years, meel_prijzen, line_width=3, color = "red")

show(g)

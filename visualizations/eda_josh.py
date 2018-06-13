# 12-06-2018
# Joshua de Roos
# Exploratory Data Analysis van Joshua

from bokeh.plotting import figure
from bokeh.io import output_file, show
import matplotlib as plt
import pandas as pd
import io
from pandas import ExcelWriter
import numpy as np

rainfall = pd.read_csv('../data/rainfall_better.csv',header=0, sep=',', error_bad_lines=False, encoding = 'latin-1')
exchangerate = pd.read_excel('../data/exchangerate_simple.xlsx',header=0, sep=',', error_bad_lines=False, encoding = 'latin-1')
data_WFP = pd.read_csv('../data/WFP_data_normalised.csv', encoding='latin-1')

goed1 = data_WFP.loc[data_WFP['cm_name'].str.contains('Milk'), 'adm0_name'].unique()
goed2 = data_WFP.loc[data_WFP['cm_name'].str.contains('Cheese'), 'adm0_name'].unique()

goed = list(set(goed1) & set(goed2))
goed.sort()

def correlations(data_WFP):
    years = [x for x in range(1992, 2018)]
    countries = data_WFP['adm0_name'].unique()

    for land in countries:
        country = data_WFP['adm0_name'] == land
        goods = data_WFP.loc[country, 'cm_name'].unique()
        done = []
        for i in goods:
            for j in goods:
                if i != j:
                    if (i,j) not in done and (j,i) not in done:
                        done.append((i,j))
                        good1 = data_WFP['cm_name'] == i
                        good2 = data_WFP['cm_name'] == j

                        prices1 = []
                        prices2 = []

                        for year in years:
                            time = data_WFP['mp_year'] == year
                            for month in range(1, 13):
                                data_month = data_WFP['mp_month'] == month
                                list_good1 = data_WFP.loc[country & good1 & time & data_month, 'mp_price']
                                list_good2 = data_WFP.loc[country & good2 & time & data_month, 'mp_price']

                                if list_good2.empty is False and list_good1.empty is False:
                                    prices1.append(list_good1.mean())
                                    prices2.append(list_good2.mean())

                        if prices1 and prices2 and len(prices1) > 10:
                            coeff = np.corrcoef(prices1, prices2)
                            if coeff[0][1] > 0.90 or coeff[0][1] < -0.90:
                                print("{}:  {} and  {}  =   {}      {}".format(land, i, j, round(coeff[0][1], 4), len(prices1)))
correlations(data_WFP)

# units = data_WFP.loc[data_WFP['cm_name'] == 'Flour', 'um_name'].unique()
# units.sort()

# for unit in units:
#     print(unit)
# for goederen in goed:
#     print(goederen)

# print(len(goed))

# # print(data_WFP.loc[(data_WFP['cm_name'] == 'Flour') & (data_WFP['mp_price'] > 5) & (data_WFP['mp_year'] == 2008), 'adm0_name'])

# years = [x for x in range(1992, 2018)]
# brood_prijzen = []
# meel_prijzen = []
# for year in years:

#     brood = data_WFP.loc[(data_WFP['cm_name'] == 'Bread') & (data_WFP['mp_year'] == year), 'mp_price']
#     meel = data_WFP.loc[(data_WFP['cm_name'] == 'Flour') & (data_WFP['mp_year'] == year), 'mp_price']
#     meel_prijzen.append(meel.mean())
#     brood_prijzen.append(brood.mean())

# output_file("test.html")

# g = figure()

# g.line(years,brood_prijzen, line_width=3, color = "blue")
# g.line(years, meel_prijzen, line_width=3, color = "red")

# show(g)

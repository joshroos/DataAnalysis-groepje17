from bokeh.plotting import figure
from bokeh.io import output_file, show
from bokeh.models import LinearAxis, Range1d
import matplotlib as plt
import math
import pandas as pd
import io
from pandas import ExcelWriter
import numpy as np

rainfall = pd.read_csv('../data/rainfall_better.csv',header=0, sep=',', error_bad_lines=False, encoding = 'latin-1')
#exchangerate = pd.read_excel('../data/exchangerate_simple.xlsx',header=0, sep=',', error_bad_lines=False, encoding = 'latin-1')
data_WFP = pd.read_csv('../data/WFP_data_normalised.csv', encoding='latin-1')


def rainfall_correlation(rainfall, data_WFP):
    #products = data_WFP['cm_name'].unique()
    years = [x for x in range(1992, 2016)]
    products = ["Wheat", "Millet", "Milk"]
    #countries = ['Afghanistan', 'Ethiopia', 'Guinea-Bissau', 'India']
    correlations = []
    prices = []
    rainfall_country = []
    Amount_of_n = []
    all_products = []

    for k in products:

        val = data_WFP.loc[(data_WFP['cm_name'] == k), 'adm0_name']
        countries = val.unique()

        for j in countries:
            n = 0
            for i in years:
                
                year = data_WFP['mp_year'] == i
                country = data_WFP['adm0_name'] == j
                cm_name = data_WFP['cm_name'] == k
                val1 = data_WFP.loc[(year) & (country) & (cm_name), 'mp_price']
                #print(k, j, i, val1.mean())
                year_info = rainfall['year'] == i
                country = rainfall['country'] == j
                val2 = rainfall.loc[(year_info) & (country), 'pr_total']
                #print(k, j, i, val2.mean())

                if math.isnan(val1.mean()) or math.isnan(val2.mean()):
                    pass
                else:
                    prices.append(val1.mean())
                    rainfall_country.append(val2.mean())
                    all_products.append(k)
                    n += 1
            
            correlation = np.corrcoef(prices, rainfall_country)
            print(j, k, correlation)
            correlations.append(correlation[0,1])
            Amount_of_n.append(n)
     

    print(countries, Amount_of_n, correlations)

    download = "rainfall_wheat_correlations.csv" 
    csv = open(download, "w") 
    columnTitleRow = "product, country, n, correlation\n"
    csv.write(columnTitleRow)

    for i in range(len(countries)):
        row = str(all_products[i])  + "," + str(countries[i]) + "," + str(Amount_of_n[i]) + "," + str(correlations[i]) + "\n"
        csv.write(row)

    return

rainfall_correlation(rainfall, data_WFP)
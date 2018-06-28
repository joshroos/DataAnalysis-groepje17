from bokeh.plotting import figure
from bokeh.io import output_file, show
from bokeh.models import LinearAxis, Range1d
import matplotlib as plt
import math
import pandas as pd
import io
from pandas import ExcelWriter
import numpy as np

data_all = pd.read_csv('../week3_analysis/all_data.csv', encoding='latin-1')

# prints for every product for every country the amount of data points and correlation between population and productprice
def correlation_population(data_all):
    products = data_all['cm_name'].unique()
    years = [x for x in range(1992, 2016)]
    correlations = []
    prices = []
    population_country = []
    Amount_of_n = []
    all_products = []

    for k in products:

        val = data_all.loc[(data_all['cm_name'] == k), 'adm0_name']
        countries = val.unique()
        country_withcorrelation = []

        for j in countries:
            n = 0
            for i in years:
                
                year = data_all['mp_year'] == i
                country = data_all['adm0_name'] == j
                cm_name = data_all['cm_name'] == k
                val1 = data_all.loc[(year) & (country) & (cm_name), 'mp_price']
                year_info = data_all['mp_year'] == i
                country = data_all['adm0_name'] == j
                val2 = data_all.loc[(year_info) & (country), 'population']

                if math.isnan(val1.mean()) or math.isnan(val2.mean()):
                    pass
                else:
                    prices.append(val1.mean())
                    population_country.append(val2.mean())
                    n += 1
            
            correlation = np.corrcoef(prices, population_country)
            all_products.append(k)
            country_withcorrelation.append(j)
            correlations.append(correlation[0,1])
            Amount_of_n.append(n)
            print(j, ",", k, ",", n, ",", correlation[0,1])
    
    # makes the csv
    download = "population_and_correlations.csv" 
    csv = open(download, "w") 
    columnTitleRow = "product, country, n, correlation\n"
    csv.write(columnTitleRow)

    for i in range(len(country_withcorrelation)):
        row = str(all_products[i])  + "," + str(country_withcorrelation[i]) + "," + str(Amount_of_n[i]) + "," + str(correlations[i]) + "\n"
        csv.write(row)

    return



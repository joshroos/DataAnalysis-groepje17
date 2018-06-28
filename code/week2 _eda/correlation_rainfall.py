from bokeh.plotting import figure
from bokeh.io import output_file, show
from bokeh.models import LinearAxis, Range1d
import matplotlib as plt
import math
import pandas as pd
import io
from pandas import ExcelWriter
import numpy as np

rainfall = pd.read_csv('../../data/rainfall_better.csv',header=0, sep=',', error_bad_lines=False, encoding = 'latin-1')
data_WFP = pd.read_csv('../../data/WFP_data_normalised.csv', encoding='latin-1')
correlation_rainfall = pd.read_csv('../../data/rainfall_correlations.csv', encoding='latin-1')

# prints all correlations between rainfall and all products in all countries for all years
def rainfall_correlation(rainfall, data_WFP):
    products = data_WFP['cm_name'].unique()
    years = [x for x in range(1992, 2016)]
    correlations = []
    prices = []
    rainfall_country = []
    Amount_of_n = []
    all_products = []

    for k in products:

        val = data_WFP.loc[(data_WFP['cm_name'] == k), 'adm0_name']
        countries = val.unique()
        country_withcorrelation = []

        for j in countries:
            n = 0
            for i in years:
                
                year = data_WFP['mp_year'] == i
                country = data_WFP['adm0_name'] == j
                cm_name = data_WFP['cm_name'] == k
                val1 = data_WFP.loc[(year) & (country) & (cm_name), 'mp_price']

                year_info = rainfall['year'] == i
                country = rainfall['country'] == j
                val2 = rainfall.loc[(year_info) & (country), 'pr_total']

                if math.isnan(val1.mean()) or math.isnan(val2.mean()):
                    pass
                else:
                    prices.append(val1.mean())
                    rainfall_country.append(val2.mean())
                    n += 1
            
            correlation = np.corrcoef(prices, rainfall_country)
            
            if n != 0:
                all_products.append(k)
                country_withcorrelation.append(j)
                correlations.append(correlation[0,1])
                Amount_of_n.append(n)
                print(j, ",", k, ",", n, ",", correlation[0,1])
     

    print(country_withcorrelation, Amount_of_n, all_products, correlations)

    # makes the csv
    download = "rainfall_and_correlations.csv" 
    csv = open(download, "w") 
    columnTitleRow = "product, country, n, correlation\n"
    csv.write(columnTitleRow)

    for i in range(len(country_withcorrelation)):
        row = str(all_products[i])  + "," + str(country_withcorrelation[i]) + "," + str(Amount_of_n[i]) + "," + str(correlations[i]) + "\n"
        csv.write(row)

    return


# writes the csv to an excel sheet where all second lines are deleted (makes it readable)
def rainfall_better(correlation_rainfall):
    rainfall_correlations = correlation_rainfall.iloc[::2]
    print(rainfall_correlations)

    writer = ExcelWriter('rainfall_correlations1.xlsx')
    rainfall_correlations.to_excel(writer, 'Sheet1')
    writer.save()  
    return

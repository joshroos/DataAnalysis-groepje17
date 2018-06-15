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

    years = [x for x in range(1992, 2016)]
    val = data_WFP.loc[(data_WFP['cm_name'] == 'Wheat'), 'adm0_name']
    countries = val.unique()
    print(countries)
    #countries = ['Afghanistan', 'Ethiopia', 'Guinea-Bissau', 'India']
    correlations = []
    prices = []
    rainfall_country = []
    Amount_of_n = []

    for j in countries:
        n = 0
        for i in years:
            
            year = data_WFP['mp_year'] == i
            country = data_WFP['adm0_name'] == j
            cm_name = data_WFP['cm_name'] == 'Wheat'
            val1 = data_WFP.loc[(year) & (country) & (cm_name), 'mp_price']
            print(j, i, val1.mean())
            year_info = rainfall['year'] == i
            country = rainfall['country'] == j
            val2 = rainfall.loc[(year_info) & (country), 'pr_total']
            print(j, i, val2.mean())

            if math.isnan(val1.mean()) or math.isnan(val2.mean()):
                pass
            else:
                prices.append(val1.mean())
                rainfall_country.append(val2.mean())
                n += 1

        correlation = np.corrcoef(prices, rainfall_country)
        correlations.append(correlation[0,1])
        Amount_of_n.append(n)

    print(countries, Amount_of_n, correlations)

    download = "rainfall_wheat_correlations.csv" 
    csv = open(download, "w") 
    columnTitleRow = "country, n, correlation\n"
    csv.write(columnTitleRow)

    for i in range(len(countries)):
        row = str(countries[i]) + "," + Amount_of_n[i] + "," + correlations[i] + "\n"
        csv.write(row)


    return


def rainfall_correlations_per_country(data_WFP):
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
                                list_good1 = data_WFP.loc[country & good1 &
                                 time & data_month, 'mp_price']
                                list_good2 = data_WFP.loc[country & good2 & 
                                time & data_month, 'mp_price']

                                if list_good2.empty is False and list_good1.empty is False:
                                    prices1.append(list_good1.mean())
                                    prices2.append(list_good2.mean())

                        if prices1 and prices2 and len(prices1) > 40:
                            coeff = np.corrcoef(prices1, prices2)
                            if coeff[0][1] > 0.75 or coeff[0][1] < -0.75:
                                print("{}:  {} and  {}  =   {}      {}".format
                                (land, i, j, round(coeff[0][1], 4), len(prices1)))

#rainfall_correlations_per_country(data_WFP)

rainfall_correlation(rainfall, data_WFP)
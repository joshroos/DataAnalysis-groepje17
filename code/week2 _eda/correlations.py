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

rainfall = pd.read_csv('../../data/rainfall_better.csv',header=0, sep=',', error_bad_lines=False, encoding = 'latin-1')
exchangerate = pd.read_excel('../../data/exchangerate_simple.xlsx',header=0, sep=',', error_bad_lines=False, encoding = 'latin-1')
data_WFP = pd.read_csv('../../data/WFP_data_normalised.csv', encoding='latin-1')

goed1 = data_WFP.loc[data_WFP['cm_name'].str.contains('Milk'), 'adm0_name'].unique()
goed2 = data_WFP.loc[data_WFP['cm_name'].str.contains('Cheese'), 'adm0_name'].unique()

goed = list(set(goed1) & set(goed2))
goed.sort()

# def compare_amount(data_combinations):


#     country = data_combinations.loc[data_combinations['combinations'] == 'Rice & Maize', 'country']
#     country = country.tolist()
#     countrynew = []
#     print(country)
#     for x in range(len(country)):
#         countrynew.append(country[x].split(' & '))

#     amount_total = len(countrynew[0])
#     print(amount_total)

#     correlations = find_things(data_combinations,13)
#     for x in range(len(correlations)):
#         print(len(correlations[x]))

#     return

def correlations_per_country(data_WFP):
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
#correlations_per_country(data_WFP)

def correlations_per_good(data_WFP):
    done = []
    goods = data_WFP['cm_name'].unique()
    years = [x for x in range(1992, 2018)]
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
                            list_good1 = data_WFP.loc[good1 &
                                time & data_month, 'mp_price']
                            list_good2 = data_WFP.loc[good2 & 
                            time & data_month, 'mp_price']

                            if list_good2.empty is False and list_good1.empty is False:
                                prices1.append(list_good1.mean())
                                prices2.append(list_good2.mean())

                    if prices1 and prices2 and len(prices1) > 40:
                        coeff = np.corrcoef(prices1, prices2)
                        if coeff[0][1] > 0.75 or coeff[0][1] < -0.75:
                            print("{} and  {}  =   {}      {}".format
                            (i, j, round(coeff[0][1], 4), len(prices1)))

correlations_per_good(data_WFP)
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

# reads necessary data
file_rain = '../../data/rainfall_better.csv'
file_exchange = '../../data/exchangerate_simple.xlsx'
file_wfp = '../../data/WFP_data_normalised.csv'

rainfall = pd.read_csv(file_rain, header=0, sep=',', error_bad_lines=False,
                       encoding='latin-1')
exchangerate = pd.read_excel(file_exchange, header=0, sep=',',
                             error_bad_lines=False, encoding='latin-1')
data_WFP = pd.read_csv(file_wfp, encoding='latin-1')


# calculates all correlations of any two goods per country
def correlations_per_country(data_WFP):
    years = [x for x in range(1992, 2018)]
    countries = data_WFP['adm0_name'].unique()

    for land in countries:
        country = data_WFP['adm0_name'] == land
        goods = data_WFP.loc[country, 'cm_name'].unique()
        done = []

        # makes all combinations of two goods
        for i in goods:
            for j in goods:
                if i != j:
                    if (i, j) not in done and (j, i) not in done:
                        done.append((i, j))
                        good1 = data_WFP['cm_name'] == i
                        good2 = data_WFP['cm_name'] == j
                        prices1 = []
                        prices2 = []

                        # collects mean of all prices measured in same month
                        for year in years:
                            time = data_WFP['mp_year'] == year
                            for month in range(1, 13):
                                data_month = data_WFP['mp_month'] == month
                                l_good1 = data_WFP.loc[country & good1 &
                                                time & data_month, 'mp_price']
                                l_good2 = data_WFP.loc[country & good2 &
                                                time & data_month, 'mp_price']
                                if l_good2.empty is False:
                                    if l_good1.empty is False:
                                        prices1.append(l_good1.mean())
                                        prices2.append(l_good2.mean())

                        # calculates coefficient
                        if prices1 and prices2 and len(prices1) > 40:
                            coeff = np.corrcoef(prices1, prices2)
                            if coeff[0][1] > 0.75 or coeff[0][1] < -0.75:
                                print("{}:  {} and  {}  =   {}      {}".format
                                (land, i, j, round(coeff[0][1], 4), len(prices1)))


correlations_per_country(data_WFP)


# calculates all correlations of any two goods worldwide
def correlations_per_good(data_WFP):
    done = []
    goods = data_WFP['cm_name'].unique()
    years = [x for x in range(1992, 2018)]
    
    # makes all combinations of two goods
    for i in goods:
        for j in goods:
            if i != j:
                if (i,j) not in done and (j,i) not in done:
                    done.append((i,j))
                    good1 = data_WFP['cm_name'] == i
                    good2 = data_WFP['cm_name'] == j

                    prices1 = []
                    prices2 = []

                    # collects mean of all prices measured in same month
                    for year in years:
                        time = data_WFP['mp_year'] == year
                        for month in range(1, 13):
                            data_month = data_WFP['mp_month'] == month
                            l_good1 = data_WFP.loc[good1 &
                                time & data_month, 'mp_price']
                            l_good2 = data_WFP.loc[good2 & 
                            time & data_month, 'mp_price']
                            if l_good2.empty is False:
                                if l_good1.empty is False:
                                    prices1.append(l_good1.mean())
                                    prices2.append(l_good2.mean())

                    # calculates coefficient
                    if prices1 and prices2 and len(prices1) > 40:
                        coeff = np.corrcoef(prices1, prices2)
                        if coeff[0][1] > 0.75 or coeff[0][1] < -0.75:
                            print("{} and  {}  =   {}      {}".format
                            (i, j, round(coeff[0][1], 4), len(prices1)))


correlations_per_good(data_WFP)

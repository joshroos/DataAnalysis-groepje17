# Darius Barsony 
# 28 juni 2018
#
# this file contains two functions, one is called correlations
# the other one is called plot. Correlations is used 
# to compute the correlations between all countries and 
# the GDP of those countries. Plot is used to generate a plot 
# for a certain country and and the GDP of that country. 

from bokeh.plotting import figure, ColumnDataSource
from bokeh.models import HoverTool, CustomJS, Slider
from bokeh.io import output_file, show
from bokeh.layouts import row, widgetbox, gridplot
import math
import pandas as pd
import io
from pandas import ExcelWriter
import numpy as np
import csv

data_BNP = pd.read_excel('../../../data/BBP_countries.xlsx',header=0, sep=',', error_bad_lines=False, encoding = 'latin-1')
data_WFP = pd.read_csv('../../../data/WFP_data_normalised.csv', encoding='latin-1')
data_population = pd.read_csv('../../../data/population_1960_2017_GOEDE.csv')

'''
This function computes the correlation coefficient
between all of the countries and all of their commodities
throughout the years. If either the GDP or the price of a commodity
in some year is missing, the datapoint will be skipped.
In adittion the correlation coeficcient is only computed if there is 
data available from more than three years.
Lastly the correlations are written to a csv file to make it easier to further
analyze the data. 
'''
def correlations():
    countries = data_WFP["adm0_name"].unique()
    years = [x for x in range(1992, 2018)]

    with open("../../../data/BNP/corrcoeffBNP.csv", 'w') as csvfile:
        wr = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)

        for country in countries:
            # filter data by country
            BNP_country = data_BNP[data_BNP["Country Name"] == country]
            commodities = data_WFP.loc[data_WFP['adm0_name'] == country, 'cm_name'].unique()
            data_country = data_WFP[data_WFP["adm0_name"] == country]

            for commodity in commodities:
                average_commodity_prices = []
                BNP_country_years = []

                # filter by commodity
                data_country_commodity = data_country[data_country["cm_name"] == commodity]
                
                for year in years:
                    data_country_year = data_country_commodity[data_country_commodity["mp_year"] == year]

                    #get data points
                    commodity_price = list(data_country_year["mp_price"])
                    BNP = list(BNP_country["{}".format(year)])

                    # check availability of data
                    if commodity_price and BNP[0] != 'Unknown':
                        average = sum(commodity_price)/len(commodity_price)
                        average_commodity_prices.append(average)
                        BNP_country_years.append(BNP[0] / 1000000000)

                # check by amount of datapoints
                if len(average_commodity_prices) > 3:
                    correlatie_coefficient = np.corrcoef(average_commodity_prices, BNP_country_years)
                    correlatie = correlatie_coefficient[0][1]
                    csvRow = [country, commodity, correlatie, len(average_commodity_prices)]
                    wr.writerow(csvRow)
                    
'''
This function takes a country as an argument and generates
a line of both the BNP and price of a commodity of that country.
It returns a regression line through a scatter of datapoints. 

'''
def plot(country, commodity):
    years = [x for x in range(1992, 2018)]
    g = figure(title="{} price for {} from 1992 to 2017".format(commodity, country))
    g.xaxis.axis_label = "BNP"
    g.yaxis.axis_label = "{} price".format(commodity)

    BNP_country = data_BNP[data_BNP["Country Name"] == country]
    WFP_country = data_WFP.loc[data_WFP['adm0_name'] == country]
    commodity_prices = WFP_country.loc[WFP_country['cm_name'] == commodity]

    average_commodity_prices = []
    BNP_country_years = []

    for year in years:
        # filter by year
        commodity_price_year = commodity_prices[commodity_prices["mp_year"] == year]
        commodity_price = list(commodity_price_year["mp_price"])
        BNP = list(BNP_country["{}".format(year)])
        # check if data is available
        if commodity_price and BNP[0] != 'Unknown':
            average = sum(commodity_price)/len(commodity_price)
            average_commodity_prices.append(average)
            BNP_country_years.append(BNP[0] / 1000000000)
    # compute regression
    if BNP_country_years and average_commodity_prices:
        regression = np.polyfit(BNP_country_years, average_commodity_prices, 1)
        r_x, r_y = zip(*((i, i*regression[0] + regression[1]) for i in range(len(BNP_country_years))))

        g.scatter(BNP_country_years, average_commodity_prices)
        g.line(r_x, r_y, line_width=2, color='#FF0000')
    return g

# compute gridplot
countries = ['Mali', 'Algeria', "Cote d'Ivoire", 'Burkina Faso',
 'Niger', 'Guinea', 'Guinea-Bissau', 'Ghana', 'Cameroon', 'Gambia', 'Mauritania', 'Nigeria']

commodity = 'Rice'

ma = plot('Mali', commodity)
al = plot('Algeria', commodity)
co = plot("Cote d'Ivoire", commodity)
bu = plot('Burkina Faso', commodity)
ni = plot('Niger', commodity)
gu = plot('Guinea', commodity)
gub = plot('Guinea-Bissau', commodity)
gh = plot('Ghana', commodity)
ca = plot('Cameroon', commodity)
ga = plot('Gambia', commodity)
mau = plot('Mauritania', commodity)
nig = plot('Nigeria', commodity)

p = gridplot([[ma, al, co], [bu, ni, gu], [gub, gh, ca], [ga, mau, nig]])
show(p)

# correlations()
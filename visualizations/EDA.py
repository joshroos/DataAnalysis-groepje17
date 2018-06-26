from bokeh.plotting import figure
from bokeh.io import output_file, show
from bokeh.models import LinearAxis, Range1d
import matplotlib as plt
import pandas as pd
import io
from pandas import ExcelWriter
import numpy as np

rainfall = pd.read_csv('../data/rainfall_better.csv',header=0, sep=',', error_bad_lines=False, encoding = 'latin-1')
exchangerate = pd.read_excel('../data/exchangerate_simple.xlsx',header=0, sep=',', error_bad_lines=False, encoding = 'latin-1')
data_WFP = pd.read_csv('../data/WFP_data_normalised.csv', encoding='latin-1')


def wheat_rainfall_Afghanistan(rainfall, data_WFP):

    years = [x for x in range(2004, 2015)]
    prices = []
    rainfall_afghanistan = []

    for i in years:
        year = data_WFP['mp_year'] == i
        country = data_WFP['adm0_name'] == 'Afghanistan'
        cm_name = data_WFP['cm_name'] == 'Wheat'
        val1 = data_WFP.loc[(year) & (country) & (cm_name), 'mp_price']
        prices.append(val1.mean())

        year_info = rainfall['year'] == i
        country = rainfall['country'] == 'Afghanistan'
        val2 = rainfall.loc[(year_info) & (country), 'pr_total']
        rainfall_afghanistan.append(val2.mean())

    s1 = figure(x_range=(2004, 2015), y_range=(0, 1.1))
    s1.extra_y_ranges = {"foo": Range1d(start=0, end=500)}
    s1.add_layout(LinearAxis(y_range_name="foo"), 'right')   
    s1.line(years, prices, color="red")
    s1.line(years, rainfall_afghanistan, color="blue", y_range_name="foo")
    output_file("wheat_rainfall_afghanistan.html")
    show(s1)
    
    correlation = np.corrcoef(prices, rainfall_afghanistan)
    print(correlation)
    return

def wheat_rainfall_Ethiopia(rainfall, data_WFP):

    years = [x for x in range(2005, 2015)]
    prices = []
    rainfall_Ethiopia = []

    for i in years:

        year = data_WFP['mp_year'] == i
        country = data_WFP['adm0_name'] == 'Ethiopia'
        cm_name = data_WFP['cm_name'] == 'Wheat'
        val1 = data_WFP.loc[(year) & (country) & (cm_name), 'mp_price']
        prices.append(val1.mean())

        year_info = rainfall['year'] == i
        country = rainfall['country'] == 'Ethiopia'
        val2 = rainfall.loc[(year_info) & (country), 'pr_total']
        rainfall_Ethiopia.append(val2.mean())

    s1 = figure(x_range=(1992, 2015), y_range=(0, 1.1))
    s1.extra_y_ranges = {"foo": Range1d(start=0, end=2000)}
    s1.add_layout(LinearAxis(y_range_name="foo"), 'right')   
    s1.line(years, prices, color="red")
    s1.line(years, rainfall_Ethiopia, color="blue", y_range_name="foo")
    output_file("wheat_rainfall_ethiopia.html")
    show(s1)
    
    correlation = np.corrcoef(prices, rainfall_Ethiopia)
    print(correlation)
    return

def wheat_rainfall_India(rainfall, data_WFP):

    years = [x for x in range(2004, 2015)]
    prices = []
    rainfall_India = []

    for i in years:

        year = data_WFP['mp_year'] == i
        country = data_WFP['adm0_name'] == 'India'
        cm_name = data_WFP['cm_name'] == 'Wheat'
        val1 = data_WFP.loc[(year) & (country) & (cm_name), 'mp_price']
        prices.append(val1.mean())

        year_info = rainfall['year'] == i
        country = rainfall['country'] == 'India'
        val2 = rainfall.loc[(year_info) & (country), 'pr_total']
        rainfall_India.append(val2.mean())

    s1 = figure(x_range=(1992, 2015), y_range=(0, 1.1))
    s1.extra_y_ranges = {"foo": Range1d(start=0, end=2000)}
    s1.add_layout(LinearAxis(y_range_name="foo"), 'right')   
    s1.line(years, prices, color="red")
    s1.line(years, rainfall_India, color="blue", y_range_name="foo")
    output_file("wheat_rainfall_India.html")
    show(s1)
    
    correlation = np.corrcoef(prices, rainfall_India)
    print(correlation)

    return

def wheat_rainfall(rainfall, data_WFP, country):
    years = [x for x in range(1992, 2016)]
    prices = []
    rainfall_country = []

    for i in years:

        year1 = data_WFP['mp_year'] == i
        country1 = data_WFP['adm0_name'] == country
        cm_name = data_WFP['cm_name'] == 'Wheat'
        val1 = data_WFP.loc[(year1) & (country1) & (cm_name), 'mp_price']
        prices.append(val1.mean())

        year2 = rainfall['year'] == i
        country2 = rainfall['country'] == country
        val2 = rainfall.loc[(year2) & (country2), 'pr_total']
        rainfall_country.append(val2)

    s1 = figure(x_range=(1992, 2015), y_range=(0, 1.1))
    s1.extra_y_ranges = {"foo": Range1d(start=0, end=2000)}
    s1.add_layout(LinearAxis(y_range_name="foo"), 'right')   
    s1.line(years, prices, color="red")
    s1.line(years, rainfall_country, color="blue", y_range_name="foo")
    show(s1)

    

    return

#val = data_WFP.loc[(data_WFP['cm_name'] == 'Wheat'), 'adm0_name']
#countries = val.unique()

#for country in countries:    
#    wheat_rainfall(rainfall, data_WFP, country)

wheat_rainfall_Afghanistan(rainfall, data_WFP)
wheat_rainfall_Ethiopia(rainfall, data_WFP)
wheat_rainfall_India(rainfall, data_WFP)
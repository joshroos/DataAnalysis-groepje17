# Darius Barsony
# 28 juni 2018
# 
# The GDP of a country is looked up in the database
# and plotted. 
#

from bokeh.plotting import figure, ColumnDataSource
from bokeh.models import HoverTool, CustomJS, Slider
from bokeh.io import output_file, show
from bokeh.layouts import row, widgetbox
import math
import pandas as pd
import io
from pandas import ExcelWriter
import numpy as np
import csv

'''
This function generates a line plot of the BNP of a country. 
It takes some country as an argument as a string.
'''
def BNP_country(country):
    data_BNP = pd.read_excel('../../../data/BBP_countries.xlsx',header=0, sep=',', error_bad_lines=False, encoding = 'latin-1')
    BNP_country = data_BNP[data_BNP["Country Name"] == country]
    years = [x for x in range(1992, 2018)]

    p = figure(title="GDP of {} from 1992 to 2017".format(country))
    p.xaxis.axis_label = "Years"
    p.yaxis.axis_label = "GDP (billions) {}".format(country)

    bnp_country = []

    for year in years:
        BNP = list(BNP_country["{}".format(year)])
        bnp_country.append(BNP[0]/1000000000)

    p.line(years, bnp_country)
    return p

show(BNP_country("Yemen"))


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

data_BNP = pd.read_excel('../../../data/BBP_countries.xlsx',header=0, sep=',', error_bad_lines=False, encoding = 'latin-1')

BNP_country = data_BNP.loc[data_BNP["Country Name"] == 'Yemen']
years = [x for x in range(1992, 2018)]

bnp_country = []

for year in years:
    BNP = BNP_country["{}".format(year)]
    print(BNP)
    bnp_country.append(BNP/1000000000)


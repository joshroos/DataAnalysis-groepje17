# Exploratory data analysis van Darius 
# BNP vergelijken met prijzen van bv rijst.

from bokeh.plotting import figure
from bokeh.models import FactorRange, LinearAxis, Range1d
from bokeh.io import output_file, show
import matplotlib as plt
import math
import pandas as pd
import io
from pandas import ExcelWriter
import numpy as np

# Read in data
data_BNP = pd.read_excel('../../data/BBP_countries.xlsx',header=0, sep=',', error_bad_lines=False, encoding = 'latin-1')
data_WFP = pd.read_csv('../../data/WFP_data_normalised.csv', encoding='latin-1')

years = [x for x in range(1992, 2017)]

rice_countries = data_WFP.loc[data_WFP["cm_name"].str.contains("Rice")]
India = rice_countries.loc[rice_countries["adm0_name"].str.contains("India")]
average_per_year = []
BNP_india = data_BNP[data_BNP["Country Name"] == "India"]

BNP_india_years = []


for year in years:
    BNP = BNP_india["{}".format(year)]
    BNP_india_years.append(BNP / 1000000000)
    price = list(India.loc[India["mp_year"] == year, "mp_price"])
    if len(price) != 0:
        average = sum(price)/len(price)
        average_per_year.append(average)
    else:
        average_per_year.append('nan')

# plot of GDP per year in India and 
# average prices of rice per year  
output_file("average_rice_price_india.html")
g = figure(y_range=(0, 0.5))
g.xaxis.axis_label = "Years"
g.yaxis.axis_label = "Average rice price U.S. dollars"
g.line(years, average_per_year)
g.extra_y_ranges = {"foo": Range1d(start=1, end=3000)}
g.line(years, BNP_india_years,  y_range_name="foo", color="red")
g.add_layout(LinearAxis(y_range_name="foo"), 'right')
show(g)


# plot of GDP in 2017 per country
countries = data_BNP["Country Name"]
BNP_2017 = data_BNP["2017"]
BNP_normalized = []

for BNP in BNP_2017:
    BNP = BNP / 1000000000
    BNP_normalized.append(BNP)

output_file("GDP.html")

p = figure(x_range=list(countries), plot_height=500,plot_width=1000,  title="BNP_2017")
p.vbar(x=list(countries), top=BNP_normalized, width=0.9)

p.xaxis.major_label_orientation = math.pi/2
p.xgrid.grid_line_color = None
p.y_range.start = 0

show(p)
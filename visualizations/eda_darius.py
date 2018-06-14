# Exploratory data analysis van Darius 
# BNP vergelijken met prijzen van bv rijst.

from bokeh.plotting import figure
from bokeh.models import FactorRange
from bokeh.io import output_file, show
import matplotlib as plt
import math
import pandas as pd
import io
from pandas import ExcelWriter
import numpy as np

data_BNP = pd.read_excel('../code/BBP_countries.xlsx',header=0, sep=',', error_bad_lines=False, encoding = 'latin-1')
data_WFP = pd.read_csv('../data/WFP_data_normalised.csv', encoding='latin-1')

countries = data_BNP["Country Name"]
BNP_2017 = data_BNP["2017"]
BNP_normalized = []

rice_countries = data_WFP.loc[data_WFP["cm_name"].str.contains("Rice")]
India = rice_countries.loc[rice_countries["adm0_name"].str.contains("India")]
years_rice_india = India["mp_year"].unique()
average_per_year = []

for year in years_rice_india:
    price = list(India.loc[India["mp_year"] == year, "mp_price"])
    average = sum(price)/len(price)
    average_per_year.append(average)

print(average_per_year)

output_file("average_rice_price_india.html")
g = figure()
g.line(years_rice_india, average_per_year)

show(g)



for BNP in BNP_2017:
    BNP = BNP / 1000000000
    BNP_normalized.append(BNP)

output_file("GDP.html")

p = figure(x_range=list(countries), plot_height=500,plot_width=1000,  title="BNP_2017")
p.vbar(x=list(countries), top=BNP_normalized, width=0.9)

p.xaxis.major_label_orientation = math.pi/2
p.xgrid.grid_line_color = None
p.y_range.start = 0

# show(p)
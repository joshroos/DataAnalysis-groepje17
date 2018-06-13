from bokeh.plotting import figure
from bokeh.io import output_file, show
import matplotlib as plt
import pandas as pd
import io
from pandas import ExcelWriter

rainfall = pd.read_csv('../data/rainfall_better.csv',header=0, sep=',', error_bad_lines=False, encoding = 'latin-1')
exchangerate = pd.read_excel('../data/exchangerate_simple.xlsx',header=0, sep=',', error_bad_lines=False, encoding = 'latin-1')
data_WFP = pd.read_csv('../data/WFP_data_normalised.csv', encoding='latin-1')

years = [x for x in range(1992, 2015)]
print(data_WFP.loc[data_WFP["cm_name"] == "Wheat"])



# Prepare some data
print(data_WFP.loc[(data_WFP["cm_name"] == "Wheat") & (data_WFP["adm0_name"] == "Afghanistan"), 'mp_price'].mean())

wheat = data_WFP.loc[(data_WFP["cm_name"] == "Wheat") & (data_WFP["adm0_name"] == "Afghanistan"), 'mp_price']
years_w = data_WFP.loc[(data_WFP["cm_name"] == "Wheat"), 'mp_year']

# Prepare the output file
output_file("wheat.html")

# Create a figure object
g = figure()

# Create line plot
g.line(years_w, wheat)

show(g)

rainfall = rainfall.loc[rainfall['pr_total']]
years_r = rainfall.loc[rainfall['years']]

# Prepare the output file
output_file("rainfall.html")

# Create a figure object
h = figure()

# Create line plot
h.line(years_r, rainfall)

show(h)


'''
prices = []

for year in years:

    month = data_WFP['mp_month'] == 6
    year = data_WFP['mp_year'] == year
    country = data_WFP['adm0_name'] == 'Afghanistan'
    cm_name = data_WFP['cm_name'] == 'Rice'

    val = data_WFP.loc[(month) & (year) & (country) & (cm_name), 'mp_price']
    prices.append(val.mean())

output_file("Line_from_csv.html")
f = figure()
f.line(years,prices)
show(f)

'''
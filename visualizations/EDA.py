from bokeh.plotting import figure
from bokeh.io import output_file, show
import matplotlib as plt
import pandas as pd
import io
from pandas import ExcelWriter

rainfall = pd.read_csv('../data/rainfall_better.csv',header=0, sep=',', error_bad_lines=False, encoding = 'latin-1')
exchangerate = pd.read_excel('../data/exchangerate_simple.xlsx',header=0, sep=',', error_bad_lines=False, encoding = 'latin-1')
data_WFP = pd.read_csv('../data/WFP_data_normalised.csv', encoding='latin-1')


# Prepare some data
x = rainfall["year"]
y = rainfall["pr_total"]

# Prepare the output file
output_file("rainfall.html")

# Create a figure object
g = figure()

# Create line plot
g.line(x,y)

show(g)

years = [x for x in range(2003, 2015)]
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


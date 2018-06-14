from bokeh.plotting import figure
from bokeh.io import output_file, show
from bokeh.models import LinearAxis, Range1d
import matplotlib as plt
import pandas as pd
import io
from pandas import ExcelWriter

rainfall = pd.read_csv('../data/rainfall_better.csv',header=0, sep=',', error_bad_lines=False, encoding = 'latin-1')
exchangerate = pd.read_excel('../data/exchangerate_simple.xlsx',header=0, sep=',', error_bad_lines=False, encoding = 'latin-1')
data_WFP = pd.read_csv('../data/WFP_data_normalised.csv', encoding='latin-1')

years = [x for x in range(1992, 2014)]

#########################
prices = []

for year in years:

    month = data_WFP['mp_month'] == 6
    year = data_WFP['mp_year'] == year
    country = data_WFP['adm0_name'] == 'Afghanistan'
    cm_name = data_WFP['cm_name'] == 'Wheat'

    val = data_WFP.loc[(month) & (year) & (country) & (cm_name), 'mp_price']
    prices.append(val.mean())

#output_file("wheat_new.html")
#f = figure()
#f.line(years,prices)
#show(f)

#########################
years = [x for x in range(1992, 2014)]


rainfall_afghanistan = []

for year in years:
    year_info = rainfall['year'] == year

    country = rainfall['country'] == 'Afghanistan'
    
    val = rainfall.loc[(year_info) & (country), 'pr_total']
    rainfall_afghanistan.append(val)


#output_file("rainfall.html")
#h = figure()
#h.line(years, rainfall_afghanistan)
#show(h)

#########################

# Seting the params for the first figure.
s1 = figure(x_axis_type="datetime", plot_width=1000, plot_height=600)

# Setting the second y axis range name and range
s1.extra_y_ranges = {"foo": Range1d(start=0, end=500)}

# Adding the second axis to the plot.  
s1.add_layout(LinearAxis(y_range_name="foo"), 'right')

# Setting the rect glyph params for the first graph. 
# Using the default y range and y axis here.           
s1.line(years, prices)

# Setting the rect glyph params for the second graph. 
# Using the aditional y range named "foo" and "right" y axis here. 
s1.line(years, rainfall_afghanistan, y_range_name="foo")

# Show the combined graphs with twin y axes.
show(s1)

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
from bokeh.plotting import figure
from bokeh.io import output_file, show
import matplotlib as plt
import pandas as pd
import io
from pandas import ExcelWriter

rainfall = pd.read_csv('../code/rainfall_better.csv',header=0, sep=',', error_bad_lines=False, encoding = 'latin-1')
exchangerate = pd.read_excel('../code/exchangerate_simple.xlsx',header=0, sep=',', error_bad_lines=False, encoding = 'latin-1')

# Prepare some data
x = rainfall["year"]
y = rainfall["pr_total"]

# Prepare the output file
output_file("rainfall.html")

# Create a figure object
f = figure()

# Create line plot
f.line(x,y)

show(f)
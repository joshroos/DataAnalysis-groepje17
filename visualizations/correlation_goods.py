from bokeh.plotting import figure
from bokeh.io import output_file, show
import matplotlib as plt
import pandas as pd
import io
from pandas import ExcelWriter
import numpy as np

#rainfall = pd.read_csv('../data/rainfall_better.csv',header=0, sep=',', error_bad_lines=False, encoding = 'latin-1')
#exchangerate = pd.read_excel('../data/exchangerate_simple.xlsx',header=0, sep=',', error_bad_lines=False, encoding = 'latin-1')
data_WFP = pd.read_csv('../data/WFP_data_normalised.csv', encoding='latin-1')
data_correlation = pd.read_csv('../visualizations/corrcoef.csv', encoding='latin-1')

def best_correlation(data_correlation):
    correlations = data_correlation.loc[(data_correlation['correlation'] >= 0.9), ['product1', 'product2', 'Country']]
    print(correlations)

    products = data_WFP['cm_name'].unique()

    for product1 in products:
        for product2 in products:

            countries = correlations.loc[(correlation['product1'] == product1 or product2) and (correlation['product2'] == product1 or product2), 'Country']
    
    
    return

best_correlation(data_correlation)


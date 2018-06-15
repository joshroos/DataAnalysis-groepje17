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
data_BNP = pd.read_excel('../code/BBP_countries.xlsx',header=0, sep=',', error_bad_lines=False, encoding = 'latin-1')
data_WFP = pd.read_csv('../data/WFP_data_normalised.csv', encoding='latin-1')

countries = data_WFP["adm0_name"].unique()
years = [x for x in range(1992, 2017)]
average_commodity_prices = []

for country in countries:
    commodities = data_WFP.loc[data_WFP['adm0_name'] == country, 'cm_name'].unique()
    for comodity in commodities:
        for year in years:
            average_commodity_price = data_WFP

    print(commodities)
    # for commodity in unique_commodities_per_country:
    #     commodity = commodity


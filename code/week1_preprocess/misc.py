import matplotlib as plt
import pandas as pd
import numpy as np
from pandas import ExcelWriter
import re
import wfp_clean

filename = '../../data/WFP_data_normalised.csv'
df_wfp = pd.read_csv(filename, encoding='latin-1')

goods = df_wfp['cm_name'].unique()
years = [x for x in range(1992, 2018)]
countries = df_wfp['adm0_name'].unique()


for country in countries:
    for year in years:
        time = df_wfp['mp_year'] == year
        place = df_wfp['adm0_name'] == country
        units = df_wfp.loc[time & place, 'cm_name']
        units = units.unique()
    if 'Rice' in units and 'Oil' in units:
        print(country)

        

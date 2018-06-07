
#data_population = pd.read_csv('../data/population_countries_1960-2016.csv', encoding='latin-1')
#print(data_population)

import matplotlib as plt
import pandas as pd
import io
from pandas import ExcelWriter


filename_pop = '../data/population_1960_2016.csv'
data = pd.read_csv(filename_pop ,header=2, sep=',', error_bad_lines=False, encoding = 'latin-1')
print(data)

import matplotlib as plt
import pandas as pd
import io
from pandas import ExcelWriter

rainfall_1991_2015 = pd.read_csv('../data/EXCEL_RAINFALL_COUNTRIES.csv',header=0, sep=',', error_bad_lines=False, encoding = 'latin-1')
print(rainfall_1991_2015)

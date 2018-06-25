# Joshua de Roos
# 5 juni 2018
# This program converts a csv file to an excel file

import matplotlib as plt
import pandas as pd
from pandas import ExcelWriter

file = "../../data/refugees_per_year.csv"


# converts csv file to excel file
def csv_to_excel(file):
    # reads file
    data = pd.read_csv(file, encoding='latin-1', error_bad_lines=False)

    # writes file
    writer = ExcelWriter('data_overview.xlsx')
    data.to_excel(writer, 'Sheet1')
    writer.save()


csv_to_excel(file)

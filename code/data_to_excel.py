# Joshua de Roos
# 5 juni 2018
# Dit programma maakt van het csv-bestand van de WFP een overzichtelijke excel file

import matplotlib as plt
import pandas as pd
from pandas import ExcelWriter

# leest bestand in
data = pd.read_csv('../data/refugees_per_year.csv', encoding='latin-1', error_bad_lines=False)

# schrijft bestand naar Excel file
writer = ExcelWriter('data_overview.xlsx')
data.to_excel(writer,'Sheet5')
writer.save()

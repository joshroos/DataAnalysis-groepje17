import pandas as pd
import  numpy as np 

dataframe = pd.read_csv("/home/darius/Documents/DataAnalysis-groepje17/data/BNP data/API_NY.GDP.MKTP.CD_DS2_en_csv_v2_9944656.csv", header = 2)

# drop columns that are unnecessary for analysis
processed_data = dataframe.drop(columns = list(dataframe)[4:36])

print(processed_data)
import pandas as pd
import  numpy as np 

dataframe = pd.read_csv("../data/BNP data/API_NY.GDP.MKTP.CD_DS2_en_csv_v2_9944656.csv", header = 2)
countries_file = pd.read_csv("../data/BNP data/countries.csv")

countries = []
for country in countries_file:
    # if country != 'Unnamed: 74':
    countries.append(country)

# drop columns that are unnecessary for analysis
processed_data = dataframe.drop(columns = list(dataframe)[4:36])

countries_BNP = processed_data["Country Name"]
common_countries = set(countries_BNP).intersection(countries)

# main_list = np.setdiff1d(common_countries, set(countries))

print(len(countries), countries_BNP)
import pandas as pd
import  numpy as np 
from pandas import ExcelWriter

df = pd.read_csv("../data/BNP data/API_NY.GDP.MKTP.CD_DS2_en_csv_v2_9944656.csv", header = 2)
countries_file = pd.read_csv("../data/BNP data/countries.csv")

countries = []
for country in countries_file:
    countries.append(country)

# drop columns and rows that are unnecessary for analysis (years 1960 - 1991)
df = df.drop(columns = list(df)[3:36])
# drop 2017 - ...
df = df.drop(columns = list(df)[29:])

# drop rows that are not part of countries in WFP 
df = df[df['Country Name'].isin(countries)]

# find countries that overlap
countries_BNP = df["Country Name"]
common_countries = set(countries_BNP).intersection(countries)

for year in range(1992, 2018):
    df["{}".format(year)] = df["{}".format(year)].fillna("Unknown")


GDP_all = pd.read_excel("../data/BNP data/WEO_Data_GDP_population_purchasingPower_2015-2020.xls.xlsx")
GDP = GDP_all[GDP_all["Subject Descriptor"] == "Gross domestic product, current prices"]
GDP = GDP_all[GDP_all["Units"] == "U.S. dollars"]

landen1 = set(df["Country Name"])
landen2 = set(GDP["Country"])

exceptions = ["Syrian Arab Republic", "State of Palestine", 
                "Pakistan", "Egypt", "Indonesia", "India"]

# puts GDP in 2017 of countries in correct rows
for country in landen2:
    if country not in exceptions:
        df.loc[df["Country Name"] == country, "2017"] = list(GDP[(GDP["Country"] == country)][2017])[0] * 1000000

# some minor changes
df.loc[df["Country Name"] == "State of Palestine", "2017"] = 14000000000
df.loc[df["Country Name"] == "Djibouti", "2016"] = 1890000000
df.loc[df["Country Name"] == "South Sudan", "2016"] = 3100000000
df.loc[df["Country Name"] == "Syrian Arab Republic", "2017"] = 0
df.loc[df["Country Name"] == "Pakistan", "2017"] = 304000000000
df.loc[df["Country Name"] == "Egypt", "2017"] = 237000000000
df.loc[df["Country Name"] == "Indonesia", "2017"] = 1011000000000
df.loc[df["Country Name"] == "India", "2017"] = 2439000000000

# write data to excel
writer = ExcelWriter('BBP_countries.xlsx')
df.to_excel(writer,'Sheet5')
writer.save()
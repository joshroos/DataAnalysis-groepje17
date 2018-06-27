# Joshua de Roos
# 17 juni 2018
# This program preprocesses the data containing the numver of refugees
# during the last 25 years and writes the processed data to a new csv file

import pandas as pd
import numpy as np

# read necessary files
df = pd.read_csv('../../data/Refugees 1962 - 2017.csv', encoding='latin-1',
                 error_bad_lines=False)
codes = pd.read_csv('../../data/countrycodes.csv', encoding='latin-1',
                    error_bad_lines=False)
wfp_df = pd.read_csv('../../data/WFP_data_normalised.csv', encoding='latin-1',
                     error_bad_lines=False)


# changes country codes to country names
def change_country_code(df):
    # all countries
    countries = df['Country Code'].unique()

    # changes all codes to names
    for code in countries:
        country = list(codes.loc[codes['alpha-3'] == code, 'name'])

        if code == 'ISR':
            country = ['State of Palestine']

        if len(country) > 0:
            df.loc[df['Country Code'] == code, 'Country Name'] = country[0]
    return df


df = change_country_code(df)


# removes irrelevant data from dataframe
def drop_data(df):
    # removes irrelevant columns
    df = df.drop([str(x) for x in range(1960, 1990)], axis=1)
    df = df.drop(['Indicator Name', 'Indicator Code'], axis=1)
    df = df.drop(['2017', 'Unnamed: 62'], axis=1)

    countries_wfp = wfp_df['adm0_name'].unique()
    countries_refugee = df['Country Name'].unique()
    df = df.set_index('Country Name')

    # removes countries not in WFP data
    for country in countries_refugee:
        if country not in countries_wfp:
            df = df.drop(country)

    df = df.reset_index()
    return df


df = drop_data(df)

# writes dataframe to new csv file
df.to_csv('refugees_per_year.csv')

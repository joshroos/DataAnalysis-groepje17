import pandas as pd 
import numpy as np 

df = pd.read_csv('../data/Refugees 1962 - 2017.csv', encoding='latin-1', error_bad_lines=False)
countrycodes = pd.read_csv('../data/countrycodes.csv', encoding='latin-1', error_bad_lines=False)
wfp_df = pd.read_csv('../data/WFP_data_normalised.csv', encoding='latin-1', error_bad_lines=False)


def change_country_code(df):
    countries = df['Country Code'].unique()
    
    for code in countries:
        country = list(countrycodes.loc[countrycodes['alpha-3'] == code, 'name'])

        if code == 'ISR':
            country = ['State of Palestine']

        if len(country) > 0:
            df.loc[df['Country Code'] == code, 'Country Name'] = country[0]
    return df 

df = change_country_code(df)

def drop_data(df):
    df = df.drop([str(x) for x in range(1960, 1990)], axis=1)
    df = df.drop(['Indicator Name', 'Indicator Code'], axis=1)
    df = df.drop(['2017', 'Unnamed: 62'], axis=1)

    countries_wfp = wfp_df['adm0_name'].unique()
    countries_refugee = df['Country Name'].unique()
    df = df.set_index('Country Name')
    
    for country in countries_refugee:
        if country not in countries_wfp:
            df = df.drop(country)

    df = df.reset_index()
    return df


df = drop_data(df)
df.to_csv('refugees_per_year.csv')
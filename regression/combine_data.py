# 19 juni 2018
# Joshua de Roos

import pandas as pd

df = pd.read_csv('../data/WFP_data_normalised.csv', encoding='latin-1')
df_rain = pd.read_csv('../data/rainfall_per_month.csv', encoding='latin-1')
df_refugee = pd.read_csv('../data/refugees_per_year.csv', encoding='latin-1')
df_bbp = pd.read_excel('../code/BBP_countries.xlsx')
df_population = pd.read_csv('../data/population_1960_2017_GOEDE.csv')
print(df_bbp)
def clean_wfp(df):
    columns = columns = list(df.columns)
    columns = [x for x in columns if x not in ['mp_year', 'mp_price', 'mp_month', 'adm0_name', 'cm_name']]
    df = df.drop(columns, axis=1)
    return df
df = clean_wfp(df)

def combine_data(df, df_rain, df_population):
    countries = df['adm0_name'].unique()
    for country in countries:
        place_wfp = df['adm0_name'] == country
        place_rain = df_rain['Country_Code'] == country
        place_pop = df_population['Country_Name'] == country
        place_bbp = df_bbp['Country Name'] == country
        for year in range(1992, 2018):
            year_wfp = df['mp_year'] == year
            year_rain = df_rain['Year'] == year
            for month in range(1, 13):
                month_wfp = df['mp_month'] == month
                month_rain = df_rain['Month'] == month
                rain = list(df_rain.loc[place_rain & year_rain & month_rain, 'pr'])
                population = list(df_population.loc[place_pop, str(year)])
                bbp = list(df_bbp.loc[place_bbp, str(year)])
                if len(rain) > 0:
                    df.loc[place_wfp & year_wfp & month_wfp, 'rainfall'] = rain[0]
                if len(population) > 0:
                    df.loc[place_wfp & year_wfp & month_wfp, 'population'] = population[0]
                if len(bbp) > 0 and bbp[0] != 'Unknown':
                    df.loc[place_wfp & year_wfp & month_wfp, 'bbp'] = bbp[0]
    #print(df)
    return df
                    


df = combine_data(df, df_rain, df_population)

df.to_csv('all_data.csv')
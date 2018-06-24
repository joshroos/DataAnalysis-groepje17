# 19 juni 2018
# Joshua de Roos

import pandas as pd

df = pd.read_csv('../data/WFP_data_normalised.csv', encoding='latin-1')
df_rain = pd.read_csv('../data/rainfall_per_month.csv', encoding='latin-1')
df_bbp = pd.read_excel('../code/BBP_countries.xlsx')
df_pop = pd.read_csv('../data/population_1960_2017_GOEDE.csv')


# cleans world food price data
def clean_wfp(df):
    columns = list(df.columns)
    not_needed = ['mp_year', 'mp_price', 'mp_month', 'adm0_name', 'cm_name']
    columns = [x for x in columns if x not in not_needed]
    df = df.drop(columns, axis=1)
    return df


# combines all the data into one dataframe
def combine_data(df, df_rain, df_pop):
    countries = df['adm0_name'].unique()

    # adds rain, bbp and population per data point
    for country in countries:
        loc_wfp = df['adm0_name'] == country
        loc_rain = df_rain['Country_Code'] == country
        loc_pop = df_pop['Country_Name'] == country
        loc_bbp = df_bbp['Country Name'] == country
        for yr in range(1992, 2018):
            yr_wfp = df['mp_year'] == yr
            yr_rain = df_rain['Year'] == yr
            for mnth in range(1, 13):
                mnth_wfp = df['mp_month'] == mnth
                mnth_rain = df_rain['Month'] == mnth
                rain = list(df_rain.loc[loc_rain & yr_rain & mnth_rain, 'pr'])
                pop = list(df_pop.loc[loc_pop, str(yr)])
                bbp = list(df_bbp.loc[loc_bbp, str(yr)])
                if len(rain) > 0:
                    df.loc[loc_wfp & yr_wfp & mnth_wfp, 'rainfall'] = rain[0]
                if len(pop) > 0:
                    df.loc[loc_wfp & yr_wfp & mnth_wfp, 'population'] = pop[0]
                if len(bbp) > 0 and bbp[0] != 'Unknown':
                    df.loc[loc_wfp & yr_wfp & mnth_wfp, 'bbp'] = bbp[0]
    return df


# writes new dataframe to csv
df = clean_wfp(df)
df = combine_data(df, df_rain, df_pop)
df.to_csv('all_data.csv')

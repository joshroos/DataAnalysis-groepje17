from bokeh.plotting import figure, show, output_file
import pandas as pd
import numpy as np

# reads necessary files
file_refugee = '../../data/Refugees 1962 - 2017.csv'
file_wfp = '../../data/WFP_data_normalised.csv'
df = pd.read_csv(file_refugee, encoding='latin-1', error_bad_lines=False)
wfp_df = pd.read_csv(file_wfp, encoding='latin-1', error_bad_lines=False)

# variables for retrieving specific correlations of specific country
country = 'Jordan'

wfp_df.loc[wfp_df['cm_name'].str.contains('Millet'), 'cm_name'] = 'Grain'
wfp_df.loc[wfp_df['cm_name'].str.contains('Sorghum'), 'cm_name'] = 'Grain'
wfp_df.loc[wfp_df['cm_name'].str.contains('Maize'), 'cm_name'] = 'Grain'
wfp_df.loc[wfp_df['cm_name'] == 'Wheat', 'cm_name'] = 'Grain'
wfp_df.loc[wfp_df['cm_name'].str.contains('Rice'), 'cm_name'] = 'Grain'

good = 'Grain'


# calculates the correlation of prices of a good with number of refugees
def scatter_refugees(df, wfp_df, country, good):
    country1 = wfp_df['adm0_name'] == country
    good1 = wfp_df['cm_name'] == good
    country2 = df['Country Name'] == country

    years = [x for x in range(1990, 2017)]
    prices = []
    refugees = []

    # collects years with data of prices and refugees
    for year in years:
        time = wfp_df['mp_year'] == year
        val = wfp_df.loc[country1 & good1 & time, 'mp_price']

        val2 = df.loc[country2, str(year)]

        if len(val2) > 0 and len(val) > 0:
            refugees.append(val2.mean())
            prices.append(val.mean())

    # calculates correlation coefficient
    if prices is not None and refugees is not None:
        coeff = np.corrcoef(refugees, prices)
        coeff = round(coeff[0][1], 3)
        print('{} : {} of length {}'.format(country, coeff, len(prices)))
        X = np.vstack(refugees)
        X = np.column_stack((X, np.ones(X.shape[0])))
        Y = prices

        a, b = np.linalg.lstsq(X, Y)[0]

    # possible code for a specific plot of the correlation
    p = figure(title="Refugees Jordan", toolbar_location=None, tools='hover')

    p.scatter(refugees, prices, marker="circle", size=10,
                line_color="navy", fill_color="orange", alpha=0.5)
    p.text(text_align='left', text=['Correlation: {}'.format(coeff)], 
           text_font_size='15pt', x=2400000, y=1.7)
    p.line(pd.Series(refugees), a * pd.Series(refugees) + b, color='red')
    p.background_fill_color = "#eeeeee"
    output_file("refugees.html")
    show(p)
    return coeff, len(prices)

coeff, n = scatter_refugees(df, wfp_df, country, good)

# # calculates coefficients for all countries
# countries = wfp_df.loc[wfp_df['cm_name'] == good, 'adm0_name']
# countries = countries.unique()
# list_coeff = []
# download = "../../data/refugees_correlations.csv"
# csv = open(download, "w")
# columnTitleRow = "country, correlation, n \n"
# csv.write(columnTitleRow)
# for country in countries:
#     coeff, n = scatter_refugees(df, wfp_df, country, good)
#     row = country + "," + str(coeff) + "," + str(n) + "\n"
#     csv.write(row)

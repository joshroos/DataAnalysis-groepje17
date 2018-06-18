from bokeh.plotting import figure, show, output_file
import pandas as pd
import numpy as np

df  = df = pd.read_csv('../data/Refugees 1962 - 2017.csv', encoding='latin-1', error_bad_lines=False)
wfp_df = pd.read_csv('../data/WFP_data_normalised.csv', encoding='latin-1', error_bad_lines=False)
#country = 'Jordan'
good = 'Rice'

def scatter_refugees(df, wfp_df, country, good):
    country1 = wfp_df['adm0_name'] == country
    good1 = wfp_df['cm_name'] == good
    country2 = df['Country Name'] == country

    years = [x for x in range(1990, 2017)]
    prices = []
    refugees = []
    for year in years:
        time = wfp_df['mp_year'] == year
        val = wfp_df.loc[country1 & good1 & time, 'mp_price']

        val2 = df.loc[country2, str(year)]
        
        if len(val2) > 0 and len(val) > 0:
            refugees.append(val2.mean())
            prices.append(val.mean())

    if prices and refugees:
        coeff = np.corrcoef(refugees, prices)
        print('{} : {} of length {}'.format(country, round(coeff[0][1], 3), len(prices)))
    # p = figure(title="Refugees Jordan", toolbar_location=None, tools='hover')

    # p.scatter(refugees, prices, marker="circle", size=10,
    #             line_color="navy", fill_color="orange", alpha=0.5)
    # p.text(text_align='left', text=[round(coeff[0][1], 3)], text_font_size='15pt', x=2400000, y=1.7)

    # p.background_fill_color = "#eeeeee"
    # output_file("markers.html")
    # show(p)

countries = wfp_df.loc[wfp_df['cm_name'] == 'Rice', 'adm0_name']
countries = countries.unique()
for country in countries:
    scatter_refugees(df, wfp_df, country, good)
from bokeh.plotting import figure, ColumnDataSource
from bokeh.models import FactorRange, LinearAxis, Range1d, HoverTool, CustomJS, Slider
from bokeh.io import output_file, show
from bokeh.palettes import brewer
from bokeh.layouts import row, widgetbox
import matplotlib.pyplot as plt
import math
import pandas as pd
import io
from pandas import ExcelWriter
import numpy as np
import csv

# Read in data
data_BNP = pd.read_excel('../code/BBP_countries.xlsx',header=0, sep=',', error_bad_lines=False, encoding = 'latin-1')
data_WFP = pd.read_csv('../data/WFP_data_normalised.csv', encoding='latin-1')
data_population = pd.read_csv('../data/population_1960_2017_GOEDE.csv')

def correlations():
    countries = data_WFP["adm0_name"].unique()
    years = [x for x in range(1992, 2018)]


    with open('TEST.csv', 'w') as csvfile:
        wr = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)

        for country in countries:
            # BNP of country
            BNP_country = data_BNP[data_BNP["Country Name"] == country]

            # get all commodities in list
            commodities = data_WFP.loc[data_WFP['adm0_name'] == country, 'cm_name'].unique()

            # filter by country
            data_country = data_WFP[data_WFP["adm0_name"] == country]

            for commodity in commodities:
                average_commodity_prices = []

                # filter by commodity
                data_country_commodity = data_country[data_country["cm_name"] == commodity]
                BNP_country_years = []
                
                for year in years:
                    # filter by year
                    data_country_year = data_country_commodity[data_country_commodity["mp_year"] == year]
                    commodity_price = list(data_country_year["mp_price"])

                    BNP = list(BNP_country["{}".format(year)])
                    if commodity_price and BNP[0] != 'Unknown':
                        average = sum(commodity_price)/len(commodity_price)
                        average_commodity_prices.append(average)
                        BNP_country_years.append(BNP[0] / 1000000000)

                if len(average_commodity_prices) > 3:
                    correlatie_coefficient = np.corrcoef(average_commodity_prices, BNP_country_years)
                    correlatie = correlatie_coefficient[0][1]

                    csvRow = [country, commodity, correlatie, len(average_commodity_prices)]
                    wr.writerow(csvRow)

def plot(country):
    years = [x for x in range(1992, 2018)]

    multi_line_BNP = []
    multi_line_CM_price = []

    # plot
    output_file("commodities.html")
    g = figure()
    g.xaxis.axis_label = "BNP"
    g.yaxis.axis_label = "commodity prices"

    # BNP of country
    BNP_country = data_BNP[data_BNP["Country Name"] == country]

    # get all commodities in list
    commodities = data_WFP.loc[data_WFP['adm0_name'] == country, 'cm_name'].unique()

    # filter by country
    data_country = data_WFP[data_WFP["adm0_name"] == country]
    print(commodities)
    for commodity in commodities[0:2]:
        average_commodity_prices = []

        # filter by commodity
        data_country_commodity = data_country[data_country["cm_name"] == commodity]
        BNP_country_years = []

        for year in years:
            # filter by year
            data_country_year = data_country_commodity[data_country_commodity["mp_year"] == year]
            commodity_price = list(data_country_year["mp_price"])

            BNP = list(BNP_country["{}".format(year)])
            if commodity_price and BNP[0] != 'Unknown':
                average = sum(commodity_price)/len(commodity_price)
                average_commodity_prices.append(average)
                BNP_country_years.append(BNP[0] / 1000000000)

        regression = np.polyfit(BNP_country_years, average_commodity_prices, 1)
        r_x, r_y = zip(*((i, i*regression[0] + regression[1]) for i in range(len(BNP_country_years))))
        multi_line_BNP.append(r_x)
        multi_line_CM_price.append(r_y)
        g.scatter(BNP_country_years, average_commodity_prices)

    g.multi_line(multi_line_BNP, multi_line_CM_price, color=["red", "blue"])
    show(g)


def bubble_chart():
    years = [x for x in range(1992, 2018)]
    countries = data_WFP["adm0_name"].unique()

    # all countries through the years
    y_rice_prices = []
    y_BNP_countries = []
    y_population_country = []
    y_known_countries = []

    for year in years[9:11]:
        rice_prices = []
        BNP_countries = []
        population_country = []
        known_countries = []

        for country in countries:
            # filter data
            BNP_country = data_BNP[data_BNP["Country Name"] == country]
            FP_country = data_WFP[data_WFP["adm0_name"] == country]
            POP_country = data_population[data_population["Country_Name"] == country]

            # get rice prices of country
            data_country_commodity = FP_country[FP_country["cm_name"] == "Rice"]
        
            # filter by year
            data_country_year = data_country_commodity[data_country_commodity["mp_year"] == year]

            commodity_price = list(data_country_year["mp_price"])
            BNP = list(BNP_country["{}".format(year)])
            population = list(POP_country["{}".format(year)])

            # check if data is available
            if commodity_price and BNP[0] != 'Unknown' and population:
                average = sum(commodity_price)/len(commodity_price)
                rice_prices.append(average)
                BNP_countries.append(BNP[0]/1000000000)
                population_country.append(population[0])
                known_countries.append(country)
        if rice_prices and BNP_countries and population_country and known_countries:
            y_rice_prices.append(rice_prices)
            y_BNP_countries.append(BNP_countries)
            y_population_country.append(population_country)
            y_known_countries.append(known_countries)
    source = ColumnDataSource(data=dict(
        x=y_population_country[0],
        y=y_rice_prices[0],
        sizes=y_BNP_countries[0],
        desc=y_known_countries[0]
    ))

    hover = HoverTool(tooltips=[
        ("(x,y)", "($x, $y)"),
        ("desc", "@desc"),
        ("BNP x 10^9", "@sizes")
    ])

    p = figure(tools=[hover, "pan,wheel_zoom,box_zoom,reset"], plot_width=1000, plot_height=700, title="{}".format(year))
    p.xaxis.axis_label = "Population"
    p.yaxis.axis_label = "Average wheat price"
    p.scatter(x='x', y='y' , size='sizes', alpha=0.5, source=source)
    
    callback = CustomJS(args=dict(source=source), code="""
        var data = source.data;
        var A = cb_obj.value;
        var x = data['x'];
        var y = data['y'];
        var sizes = data['sizes'];
        var desc = data['desc'];

        x.splice(0, x.length, pop_country[A]);
        y.splice(0, y.length, rice_prices[A]);
        sizes.splice(0, sizes.length, BNP[A]);
        desc.splice(0, desc.length, known_countries[A]);

        x = x[0]
        y = y[0]
        sizes = sizes[0]
        desc = desc[0]

        console.log(x, y, sizes, desc, A)

        source.change.emit()
    """)

    year_slider = Slider(start=0, end=4, value=0, step=1,
                    title="Years", callback=callback)
    # year_slider.js_on_change('value', callback)
    # callback.args["year"] = year_slider
    callback.args["pop_country"] = y_population_country
    callback.args["rice_prices"] = y_rice_prices
    callback.args["BNP"] = y_BNP_countries
    callback.args["known_countries"]= y_known_countries

    layout = row(p, widgetbox(year_slider))
    show(layout)  

# plot("Burkina Faso")
# correlations()
bubble_chart()
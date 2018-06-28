# 14-06-2018
# Joshua de Roos
# This program makes a scatter matrix of the correlation of four goods
# in one country.

from __future__ import print_function
import pandas as pd
import numpy as np
import math
from bokeh.plotting import figure
from bokeh.io import output_file, show
from bokeh.layouts import gridplot
from bokeh.models.glyphs import Circle
from bokeh.models import (BasicTicker, ColumnDataSource, Grid, LinearAxis,
                          DataRange1d, Plot, Label)
from sklearn.metrics import mean_squared_error

# reads necessary files
file_wfp = '../../data/WFP_data_normalised.csv'
file_amount = '../../data/amount_combinations.csv'
file_combi = '../../data/combination_correlations.csv'
data_wfp = pd.read_csv(file_wfp, encoding='latin-1')
data_amount = pd.read_csv(file_amount, encoding='latin-1')
df_combi = pd.read_csv(file_combi, encoding='latin-1')

# goods and country to be plotted
goods = ['Milk', 'Onions', 'Bread', 'Potatoes']
country = data_wfp['adm0_name'] == 'Ukraine'


# makes ColumnDataSource of necessary data
def make_source(goods, country, data_wfp):
    good1 = data_wfp['cm_name'] == goods[0]
    good2 = data_wfp['cm_name'] == goods[1]
    good3 = data_wfp['cm_name'] == goods[2]
    good4 = data_wfp['cm_name'] == goods[3]
    prices1, prices2, prices3, prices4 = ([] for i in range(4))

    # collects all prices of goods in same months, year and country
    for year in range(1992, 2018):
        time = data_wfp['mp_year'] == year
        for month in range(1, 13):
            data_month = data_wfp['mp_month'] == month
            list_good1 = data_wfp.loc[country & good1 & time & data_month,
                                      'mp_price']
            list_good2 = data_wfp.loc[country & good2 & time & data_month,
                                      'mp_price']
            list_good3 = data_wfp.loc[country & good3 & time & data_month,
                                      'mp_price']
            list_good4 = data_wfp.loc[country & good4 & time & data_month,
                                      'mp_price']
            if len(list_good1) > 0 and len(list_good2) > 0:
                if len(list_good3) > 0 and len(list_good4) > 0:
                    prices1.append(list_good1.mean())
                    prices2.append(list_good2.mean())
                    prices3.append(list_good3.mean())
                    prices4.append(list_good4.mean())

    # turns lists into panda series
    prices1 = pd.Series(prices1)
    prices2 = pd.Series(prices2)
    prices3 = pd.Series(prices3)
    prices4 = pd.Series(prices4)

    # makes dict, manual changes of names necessary
    data = dict(
            Milk=prices1,
            Onions=prices2,
            Bread=prices3,
            Potatoes=prices4,)

    source = ColumnDataSource(data)
    return source, data


# makes scatter plot for scatter matrix
def make_scatter(source, data, xname, yname, xax=False, yax=False):
    # sets range and borders for plot
    xdr = DataRange1d(bounds=None)
    ydr = DataRange1d(bounds=None)
    mbl = 40 if yax else 0
    mbb = 40 if xax else 0
    plot = figure(
        x_range=xdr, y_range=ydr, background_fill_color="#efe8e2",
        border_fill_color='white', plot_width=200 + mbl, plot_height=200 + mbb,
        min_border_left=2+mbl, min_border_right=2, min_border_top=2,
        min_border_bottom=2+mbb)

    # plots points
    circle = Circle(x=xname, y=yname, fill_color="blue", fill_alpha=0.2,
                    size=4, line_color="blue")
    plot.add_glyph(source, circle)

    # calculates and plots regression line
    a, b, mse = make_regression_line(data, xname, yname)
    mse_mean = mse.mean()
    print(xname, yname, mse_mean)
    x = data[xname]
    plot.line(x, a * x + b, color='red')
    plot.axis.visible = False

    # makes axis according to place in matrix
    xticker = BasicTicker()
    if xax:
        xaxis = LinearAxis()
        xaxis.axis_label = xname
        plot.add_layout(xaxis, 'below')
        xticker = xaxis.ticker
    plot.add_layout(Grid(dimension=0, ticker=xticker))

    yticker = BasicTicker()
    if yax:
        yaxis = LinearAxis()
        yaxis.axis_label = yname
        yaxis.major_label_orientation = 'vertical'
        plot.add_layout(yaxis, 'left')
        yticker = yaxis.ticker

    plot.add_layout(Grid(dimension=1, ticker=yticker))

    return plot


# makes scatter plot
def make_scatter_plot(source, data, country, xname, yname,
                      xax=False, yax=False):
    # sets range and borders for plot
    xdr = DataRange1d(bounds=None)
    ydr = DataRange1d(bounds=None)
    mbl = 40 if yax else 0
    mbb = 40 if xax else 0
    plot = figure(
        x_range=xdr, y_range=ydr, background_fill_color="#efe8e2",
        border_fill_color='white', plot_width=200 + mbl, plot_height=200 + mbb,
        min_border_left=2+mbl, min_border_right=2, min_border_top=2,
        min_border_bottom=2+mbb, title=country)

    # plots points
    circle = Circle(x=xname, y=yname, fill_color="blue", fill_alpha=0.2,
                    size=4, line_color="blue")
    plot.add_glyph(source, circle)

    # calculates and plots regression line
    a, b, mse = make_regression_line(data, xname, yname)
    mse_mean = mse.mean()
    print(xname, yname, mse_mean)
    x = data[xname]
    plot.line(x, a * x + b, color='red')
    plot.axis.visible = False

    # makes axis according to place in matrix
    xticker = BasicTicker()
    if xax:
        xaxis = LinearAxis()
        xaxis.axis_label = xname
        plot.add_layout(xaxis, 'below')
        xticker = xaxis.ticker
    plot.add_layout(Grid(dimension=0, ticker=xticker))

    yticker = BasicTicker()
    if yax:
        yaxis = LinearAxis()
        yaxis.axis_label = yname
        yaxis.major_label_orientation = 'vertical'
        plot.add_layout(yaxis, 'left')
        yticker = yaxis.ticker

    plot.add_layout(Grid(dimension=1, ticker=yticker))

    return plot


# makes plot of distribution of data points of good
def make_dist(data, xname, xax=False, yax=False):
    # sets ranges and borders for plot
    xdr = DataRange1d(bounds=None)
    ydr = DataRange1d(bounds=None)
    mbl = 40 if yax else 0
    mbb = 40 if xax else 0
    TOOLS = "hover, save, reset"
    plot = figure(x_range=xdr, y_range=ydr, tools=TOOLS, x_axis_label="",
                  y_axis_label="", background_fill_color="#E8DDCB",
                  plot_width=200+mbl, plot_height=200+mbb,
                  min_border_left=2+mbl, min_border_right=2, min_border_top=2,
                  min_border_bottom=2+mbb)

    # makes histogram
    measured = data[xname]
    hist, edges = np.histogram(measured, density=True, bins=50)

    # plots histogram
    plot.quad(top=hist, bottom=0, left=edges[:-1], right=edges[1:],
              fill_color="#036564", line_color="#033649")

    # makes axis according to place in matrix
    plot.axis.visible = False
    xticker = BasicTicker()
    if xax:
        xaxis = LinearAxis()
        xaxis.axis_label = xname
        plot.add_layout(xaxis, 'below')
        xticker = xaxis.ticker

    yticker = BasicTicker()
    if yax:
        yaxis = LinearAxis()
        yaxis.axis_label = xname
        yaxis.major_label_orientation = 'vertical'
        plot.add_layout(yaxis, 'left')
        yticker = yaxis.ticker
    plot.legend.location = "center_right"
    plot.legend.background_fill_color = "darkgrey"

    return plot


# calculates and plots correlation coefficient in matrix
def show_coeff(data, xname, yname, xax=False, yax=False):
    # sets ranges and borders of plot
    xdr = DataRange1d(bounds=None)
    ydr = DataRange1d(bounds=None)
    mbl = 40 if yax else 0
    mbb = 40 if xax else 0
    plot = figure(
        x_range=xdr, y_range=ydr, background_fill_color="#efe8e2",
        border_fill_color='white', plot_width=200 + mbl, plot_height=200 + mbb,
        min_border_left=2+mbl, min_border_right=2, min_border_top=2,
        min_border_bottom=2+mbb)

    # calculates and plots correlation coefficient
    measured1 = data[xname]
    measured2 = data[yname]
    coeff = np.corrcoef(measured1, measured2)
    coeff = round(coeff[0][1], 3)
    plot.text(text_align='center', text_baseline='middle', text=[coeff],
              text_font_size='35pt', x=0, y=-5)

    # adjust axes according to place in matrix
    plot.axis.visible = False
    xticker = BasicTicker()
    if xax:
        xaxis = LinearAxis()
        xaxis.axis_label = xname
        plot.add_layout(xaxis, 'below')
        xticker = xaxis.ticker

    yticker = BasicTicker()
    if yax:
        yaxis = LinearAxis()
        yaxis.axis_label = yname
        yaxis.major_label_orientation = 'vertical'
        plot.add_layout(yaxis, 'left')
        yticker = yaxis.ticker

    plot.add_layout(Grid(dimension=0, ticker=xticker))
    plot.add_layout(Grid(dimension=1, ticker=yticker))
    return plot


# calculates properties of regression line
def make_regression_line(data, xname, yname):
    # creating X and Y
    X = np.vstack(data[xname])
    X = np.column_stack((X, np.ones(X.shape[0])))
    Y = data[yname]

    # get out a and b values for best fit line
    a, b = np.linalg.lstsq(X, Y)[0]

    r = np.array(data[yname])
    x = np.array(data[xname])
    y = a * x + b

    mse = mean_squared_error(r, y)

    return a, b, mse


# plots scatter matrix to html file
def make_gridplot(goods, country, data_wfp):
    source, data = make_source(goods, country, data_wfp)
    goods = [x.replace(" ", "_") for x in goods]
    yattrs = list(reversed(goods))
    plots = []
    done = []

    # makes plots, distribution and coefficients
    for y in yattrs:
        row = []
        for x in goods:
            xax = (y == yattrs[-1])
            yax = (x == goods[0])
            if (x, y) in done or (y, x) in done:
                plot = show_coeff(data, x, y, xax, yax)
                row.append(plot)
            elif x != y:
                plot = make_scatter(source, data, x, y, xax, yax)
                row.append(plot)
                done.append((x, y))
            elif x == y:
                plot = make_dist(data, x, xax, yax)
                row.append(plot)
                done.append((x, y))

        plots.append(row)
    grid = gridplot(plots)
    filename = "plots/scatter_matrix_kyrgyzstan.html"
    output_file(filename, title="Scatter Matrix")
    show(grid)


# makes scatterplots about countries in the Middle East for Oil and Rice
def gridplot_middleeast(goods, data_wfp):

    country = data_wfp['adm0_name'] == 'Syrian Arab Republic'
    source, data = make_source(goods, country, data_wfp)
    p1 = make_scatter_plot(source, data, 'Syria', 'Oil', 'Rice', 4, 4)

    country = data_wfp['adm0_name'] == 'Turkey'
    source, data = make_source(goods, country, data_wfp)
    p2 = make_scatter_plot(source, data, 'Turkey', 'Oil', 'Rice', 4, 4)

    country = data_wfp['adm0_name'] == 'Iran  (Islamic Republic of)'
    source, data = make_source(goods, country, data_wfp)
    p3 = make_scatter_plot(source, data, 'Iran  (Islamic Republic of)', 'Oil',
                           'Rice', 4, 4)

    country = data_wfp['adm0_name'] == 'Yemen'
    source, data = make_source(goods, country, data_wfp)
    p4 = make_scatter_plot(source, data, 'Yemen', 'Oil', 'Rice', 4, 4)

    country = data_wfp['adm0_name'] == 'Armenia'
    source, data = make_source(goods, country, data_wfp)
    p5 = make_scatter_plot(source, data, 'Armenia', 'Oil', 'Rice', 4, 4)

    country = data_wfp['adm0_name'] == 'Jordan'
    source, data = make_source(goods, country, data_wfp)
    p6 = make_scatter_plot(source, data, 'Jordan', 'Oil', 'Rice', 4, 4)

    country = data_wfp['adm0_name'] == 'Iraq'
    source, data = make_source(goods, country, data_wfp)
    p7 = make_scatter_plot(source, data, 'Iraq', 'Oil', 'Rice', 4, 4)

    filename = "plots/riceandoil_middleeast.html"
    output_file(filename, title="Rice and Oil Middle East")
    p = gridplot([[p1, p2, p3, p4], [p5, p6, p7, None]])
    show(p)

    return


# makes scatterplots about countries in West Africa for Oil and Rice
def gridplot_westafrica(goods, data_wfp):

    country = data_wfp['adm0_name'] == 'Algeria'
    source, data = make_source(goods, country, data_wfp)
    p1 = make_scatter_plot(source, data, 'Algeria', 'Oil', 'Rice', 4, 4)

    country = data_wfp['adm0_name'] == "Cote d'Ivoire"
    source, data = make_source(goods, country, data_wfp)
    p2 = make_scatter_plot(source, data, "Cote d'Ivoire", 'Oil', 'Rice', 4, 4)

    country = data_wfp['adm0_name'] == 'Guinea-Bissau'
    source, data = make_source(goods, country, data_wfp)
    p3 = make_scatter_plot(source, data, 'Guinea-Bissau', 'Oil', 'Rice', 4, 4)

    country = data_wfp['adm0_name'] == 'Guinea'
    source, data = make_source(goods, country, data_wfp)
    p4 = make_scatter_plot(source, data, 'Guinea', 'Oil', 'Rice', 4, 4)

    # writes the plot to an html file
    filename = "plots/riceandoil_WestAfrica.html"
    output_file(filename, title="Rice and Oil West Africa")
    p = gridplot([[p1, p2], [p3, p4]])
    show(p)

    return


# makes scatterplots about countries in East Africa for Oil and Rice
def gridplot_eastafrica(goods, data_wfp):

    country = data_wfp['adm0_name'] == 'Madagascar'
    source, data = make_source(goods, country, data_wfp)
    p1 = make_scatter_plot(source, data, 'Madagascar', 'Oil', 'Rice', 4, 4)

    country = data_wfp['adm0_name'] == 'Mozambique'
    source, data = make_source(goods, country, data_wfp)
    p2 = make_scatter_plot(source, data, 'Mozambique', 'Oil', 'Rice', 4, 4)

    # writes the plot to an html file
    filename = "plots/riceandoil_EastAfrica.html"
    output_file(filename, title="Rice and Oil East Africa")
    p = gridplot([[p1, p2], [None, None]])
    show(p)

    return
    


# makes scatterplots about countries in South Asia for Oil and Rice
def gridplot_SouthAsia(goods, data_wfp):

    country = data_wfp['adm0_name'] == 'Bangladesh'
    source, data = make_source(goods, country, data_wfp)
    p1 = make_scatter_plot(source, data, 'Bangladesh', 'Oil', 'Rice', 4, 4)

    country = data_wfp['adm0_name'] == 'India'
    source, data = make_source(goods, country, data_wfp)
    p2 = make_scatter_plot(source, data, 'India', 'Oil', 'Rice', 4, 4)

    country = data_wfp['adm0_name'] == 'Pakistan'
    source, data = make_source(goods, country, data_wfp)
    p3 = make_scatter_plot(source, data, 'Pakistan', 'Oil', 'Rice', 4, 4)

    country = data_wfp['adm0_name'] == 'Tajikistan'
    source, data = make_source(goods, country, data_wfp)
    p4 = make_scatter_plot(source, data, 'Tajikistan', 'Oil', 'Rice', 4, 4)

    # writes the plot to an html file
    filename = "plots/riceandoil_SouthAsia.html"
    output_file(filename, title="Rice and Oil South Asia")
    p = gridplot([[p1, p2], [p3, p4]])
    show(p)

    return


# all countries per region found with rice and oil
oil_rice_range_middle_east = ['Armenia', 'Iran  (Islamic Republic of)', 'Iraq',
                              'Jordan', 'Syrian Arab Republic', 'Turkey',
                              'Yemen']
oil_rice_range_west_africa = ['Algeria', "Cote d'Ivoire", 'Guinea-Bissau',
                              'Guinea']
oil_rice_range_east_africa = ['Madagascar', 'Mozambique']
oil_rice_range_south_asia = ['Bangladesh', 'India', 'Pakistan', 'Tajikistan']

# countries East Africa
h_range = ['Mozambique', 'Zambia', 'United Republic of Tanzania', 'Madagascar',
           'Malawi', 'Burundi', 'Ethiopia', 'Djibouti', 'Kenya', 'Rwanda',
           'Somalia', 'Uganda', 'Sudan', 'South Sudan']

# countries Middle East
i_range = ['Armenia', 'Iraq', 'Iran  (Islamic Republic of)', 'Turkey',
           'Syrian Arab Republic', 'Jordan', 'Yemen', 'Afghanistan']

# countries West Afrika
j_range = ['Mali', 'Algeria', "Cote d'Ivoire", 'Burkina Faso', 'Niger',
           'Guinea', 'Guinea-Bissau', 'Ghana', 'Cameroon', 'Gambia',
           'Mauritania', 'Nigeria']

# countries South Asia
k_range = ['India', 'Pakistan', 'Bhutan', 'Bangladesh', 'Nepal', 'Sri Lanka',
           'Tajikistan']


# finds the countries within the regions that has data about two given goods
def find_countries_with_goods(data_wfp, good1, good2, i_range, j_range,
                              h_range, k_range):
    good1 = data_wfp.loc[(data_wfp['cm_name'] == good1), 'adm0_name'].unique()
    good2 = data_wfp.loc[(data_wfp['cm_name'] == good2), 'adm0_name'].unique()

    countries = []
    for x in good1:
        if x in good2:
            countries.append(x)
    print(countries)

    middleeast = []
    for i in countries:
        if i in i_range:
            middleeast.append(i)

    westafrica = []
    for i in countries:
        if i in j_range:
            westafrica.append(i)

    eastafrica = []
    for i in countries:
        if i in h_range:
            eastafrica.append(i)

    southasia = []
    for i in countries:
        if i in k_range:
            southasia.append(i)

    print(middleeast)
    print(westafrica)
    print(eastafrica)
    print(southasia)
    return


# prints the correlation of two given products in a given country
def correlations(country, product1, product2, data_wfp):
    years = [x for x in range(1992, 2018)]
    months = [x for x in range(1, 13)]
    price_product1 = []
    price_product2 = []
    n = 0

    for i in years:
        for j in months:
            year = data_wfp['mp_year'] == i
            month = data_wfp['mp_month'] == j
            place = data_wfp['adm0_name'] == country
            good1 = data_wfp['cm_name'] == product1
            good2 = data_wfp['cm_name'] == product2
            price1 = data_wfp.loc[good1 & place & year & month, 'mp_price']
            price2 = data_wfp.loc[good2 & place & year & month, 'mp_price']

            if math.isnan(price1.mean()) or math.isnan(price2.mean()):
                pass
            else:
                price_product1.append(price1.mean())
                price_product2.append(price2.mean())
                print(price1.mean(), price2.mean())
                n += 1

    correlation = np.corrcoef(price_product1, price_product2)
    print(country, product1, product2, n, correlation)

    return


# prints the average price of two products in a given country
def average(country, product1, product2, data_wfp):
    years = [x for x in range(1992, 2018)]
    months = [x for x in range(1, 13)]
    price_product1 = []
    price_product2 = []
    n = 0

    for i in years:
        for j in months:
            year = data_wfp['mp_year'] == i
            month = data_wfp['mp_month'] == j
            place = data_wfp['adm0_name'] == country
            good1 = data_wfp['cm_name'] == product1
            good2 = data_wfp['cm_name'] == product2
            price1 = data_wfp.loc[good1 & place & year & month, 'mp_price']
            price2 = data_wfp.loc[good2 & place & year & month, 'mp_price']

            if math.isnan(price1.mean()) or math.isnan(price2.mean()):
                pass
            else:
                price_product1.append(price1.mean())
                price_product2.append(price2.mean())
                print(price1.mean(), price2.mean())
                n += 1

    average_price1 = sum(price_product1) / float(len(price_product1))
    average_price2 = sum(price_product2) / float(len(price_product2))

    print(country, average_price1, average_price2)

    return


# prints all countries with data about two products
def Countries_with_products(data_wfp, df_combi, product1, product2):
    good1 = data_wfp['cm_name'] == product1
    good2 = data_wfp['cm_name'] == product2
    Countries_with_product1 = data_wfp.loc[good1, 'adm0_name'].unique()
    Countries_with_product2 = data_wfp.loc[good2, 'adm0_name'].unique()
    both = []

    for x in Countries_with_product1:
        if x in Countries_with_product2:
            both.append(x)

    if len(both) >= 5:
        combi = product1 + ' & ' + product2
        amount = df_combi.loc[df_combi['combinations'] == combi, 'n'].sum()
        rel = amount*100/len(both)

        print(product1, ",", product2, ",", len(both), ",", amount, ",", rel)
    return


# prints amount of all countries and amount with high correlation of all possible food combination
def compare_countries_with_products(data_wfp, data_combination):
    all_products = data_wfp['cm_name'].unique()

    for product1 in all_products:
        for product2 in all_products:
            Countries_with_products(data_wfp, df_combi, product1, product2)

    return


# finds product combinations with high amount countries with high correlation
def find_combination(data_amount):
    needed = ['product1', 'product2', 'total_countries',
              'countries_correlation', 'percentage']
    relevant = data_amount.loc[data_amount['percentage'] > 34, needed]

    for x in relevant.values.tolist():
        print(x)

    print(len(relevant.values.tolist()))
    return

# 14-06-2018
# Joshua de Roos
# This program makes a scatter matrix of the correlation of four goods
# in one country.

from __future__ import print_function
import pandas as pd
import numpy as np
from bokeh.plotting import figure
from bokeh.io import output_file, show
from bokeh.layouts import gridplot
from bokeh.models.glyphs import Circle
from bokeh.models import (BasicTicker, ColumnDataSource, Grid, LinearAxis,
                          DataRange1d, Plot, Label)
from sklearn.metrics import mean_squared_error

# reads necessary files
data_wfp = pd.read_csv('../data/WFP_data_normalised.csv', encoding='latin-1')

# goods and country to be plotted
goods = ['Milk', 'Sour cream', 'Butter', 'Curd']
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
            Sour_cream=prices2,
            Curd=prices3,
            Butter=prices4,)

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
    plot = figure(x_range=xdr, y_range=ydr, tools="save", x_axis_label="",
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
    filename = "../visualizations/plots/scatter_matrix.html"
    output_file(filename, title="Scatter Matrix")
    show(grid)


make_gridplot(goods, country, data_wfp)

# 14-06-2018
# Joshua de Roos
# 

from __future__ import print_function
from bokeh.plotting import figure
from bokeh.io import output_file, show
import matplotlib as plt
import pandas as pd
import io
from pandas import ExcelWriter
import numpy as np
from bokeh.document import Document
from bokeh.embed import file_html
from bokeh.layouts import gridplot
from bokeh.models.glyphs import Circle
from bokeh.models import (BasicTicker, ColumnDataSource, Grid, LinearAxis,
                         DataRange1d, PanTool, Plot, WheelZoomTool, Label)
from bokeh.resources import INLINE
from bokeh.sampledata.iris import flowers
from bokeh.util.browser import view
import scipy.special


data_WFP = pd.read_csv('../data/WFP_data_normalised.csv', encoding='latin-1')

country = data_WFP['adm0_name'] == 'Turkey'
good1 = data_WFP['cm_name'] == 'Oil'
good2 = data_WFP['cm_name'] == 'Salt'

prices1 = []
prices2 = []

for year in range(1992, 2018):
    time = data_WFP['mp_year'] == year
    for month in range(1, 13):
        data_month = data_WFP['mp_month'] == month
        list_good1 = data_WFP.loc[country & good1 &
            time & data_month, 'mp_price']
        list_good2 = data_WFP.loc[country & good2 & 
        time & data_month, 'mp_price']

        if list_good2.empty is False and list_good1.empty is False:
            prices1.append(list_good1.mean())
            prices2.append(list_good2.mean())

prices3 = []
prices4 = []

good1 = data_WFP['cm_name'] == 'Fish'
good2 = data_WFP['cm_name'] == 'Milk'

for year in range(1992, 2018):
    time = data_WFP['mp_year'] == year
    for month in range(1, 13):
        data_month = data_WFP['mp_month'] == month
        list_good1 = data_WFP.loc[country & good1 &
            time & data_month, 'mp_price']
        list_good2 = data_WFP.loc[country & good2 & 
        time & data_month, 'mp_price']

        if list_good2.empty is False and list_good1.empty is False:
            prices3.append(list_good1.mean())
            prices4.append(list_good2.mean())

prices1 = pd.Series(prices1)
prices2 = pd.Series(prices2)
prices3 = pd.Series(prices3)
prices4 = pd.Series(prices4)
data = dict(
        Milk=prices1,
        Sour_cream=prices2,
        Curd=prices3,
        Butter=prices4,

    )
source = ColumnDataSource(data)

def make_corr(xname, yname, xax=False, yax=False):
    xdr = DataRange1d(bounds=None)
    ydr = DataRange1d(bounds=None)
    mbl = 40 if yax else 0
    mbb = 40 if xax else 0
    plot = Plot(
        x_range=xdr, y_range=ydr, background_fill_color="#efe8e2",
        border_fill_color='white', plot_width=200 + mbl, plot_height=200 + mbb,
        min_border_left=2+mbl, min_border_right=2, min_border_top=2, min_border_bottom=2+mbb)

    circle = Circle(x=xname, y=yname, fill_color="blue", fill_alpha=0.2, size=4, line_color="blue")
    r = plot.add_glyph(source, circle)

    xdr.renderers.append(r)
    ydr.renderers.append(r)

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
    plot.add_tools(PanTool(), WheelZoomTool())        
    
    return plot

def make_dist(xname, xax=False, yax=False):
    xdr = DataRange1d(bounds=None)
    ydr = DataRange1d(bounds=None)
    mbl = 40 if yax else 0
    mbb = 40 if xax else 0
    plot = figure(tools="save", x_axis_label="", y_axis_label="",
            background_fill_color="#E8DDCB", plot_width=200+mbl, plot_height=200+mbb, 
            min_border_left=2+mbl, min_border_right=2, min_border_top=2, min_border_bottom=2+mbb)

    measured = data[xname]
    hist, edges = np.histogram(measured, density=True, bins=50)
    

    # x = np.linspace(-2, 2, 1000)
    # pdf = 1/(sigma * np.sqrt(2*np.pi)) * np.exp(-(x-mu)**2 / (2*sigma**2))
    # cdf = (1+scipy.special.erf((x-mu)/np.sqrt(2*sigma**2)))/2

    plot.quad(top=hist, bottom=0, left=edges[:-1], right=edges[1:],
            fill_color="#036564", line_color="#033649")
    # plot.line(x, pdf, line_color="#D95B43", line_width=8, alpha=0.7, legend="PDF")
    # plot.line(x, cdf, line_color="white", line_width=2, alpha=0.7, legend="CDF")
    
    xticker = BasicTicker()
    plot.axis.visible = False
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


def show_coeff(xname, yname, xax=False, yax=False):
    xdr = DataRange1d(bounds=None)
    ydr = DataRange1d(bounds=None)
    mbl = 40 if yax else 0
    mbb = 40 if xax else 0

    measured1 = data[xname]
    measured2 = data[yname]

    coeff = np.corrcoef(measured1, measured2)

    plot = figure(
        x_range=xdr, y_range=ydr, background_fill_color="#efe8e2",
        border_fill_color='white', plot_width=200 + mbl, plot_height=200 + mbb,
        min_border_left=2+mbl, min_border_right=2, min_border_top=2, min_border_bottom=2+mbb)
    
    plot.text(text_align='center', text=[round(coeff[0][1], 3)], text_font_size='35pt', x = 0, y=-5)

    xticker = BasicTicker()
    plot.axis.visible = False
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
    plot.add_tools(PanTool(), WheelZoomTool()) 

    return plot

xattrs = ['Milk', 'Sour_cream', 'Butter', 'Curd' ]
yattrs = list(reversed(xattrs))
plots = []

done = []
for y in yattrs:
    row = []
    for x in xattrs:
        if (x, y) in done or (y, x) in done:
            xax = (y == yattrs[-1])
            yax = (x == xattrs[0])
            plot = show_coeff(x, y, xax, yax)
            row.append(plot)

        elif x != y:
            xax = (y == yattrs[-1])
            yax = (x == xattrs[0])
            plot = make_corr(x, y, xax, yax)
            row.append(plot)
            done.append((x, y))
        elif x == y:
            xax = (y == yattrs[-1])
            yax = (x == xattrs[0])
            plot = make_dist(x, xax, yax)
            row.append(plot)
            done.append((x, y))

    plots.append(row)

grid = gridplot(plots)

doc = Document()
doc.add_root(grid)

if __name__ == "__main__":
    doc.validate()
    filename = "iris_splom.html"
    with open(filename, "w") as f:
        f.write(file_html(doc, INLINE, "Iris Data SPLOM"))
    print("Wrote %s" % filename)
    view(filename)
from bokeh.plotting import figure, show, output_file
from bokeh.io import output_file, show
import matplotlib as plt
import pandas as pd
import io
import bokeh.models
from pandas import ExcelWriter
import numpy as np
from bokeh.io import show, output_file
from bokeh.models import ColumnDataSource, FactorRange
from bokeh.plotting import figure

dir(bokeh.models.tools)
from bokeh.models import PanTool, ResetTool, WheelZoomTool, HoverTool, LassoSelectTool, BoxSelectTool


from sklearn import datasets
from sklearn.cluster import KMeans
import sklearn.metrics as sm

#rainfall = pd.read_csv('../data/rainfall_better.csv',header=0, sep=',', error_bad_lines=False, encoding = 'latin-1')
#exchangerate = pd.read_excel('../data/exchangerate_simple.xlsx',header=0, sep=',', error_bad_lines=False, encoding = 'latin-1')
data_WFP = pd.read_csv('../data/WFP_data_normalised.csv', encoding='latin-1')
data_correlation = pd.read_csv('../visualizations/corrcoef.csv', encoding='latin-1')



def rijst_olie_chart(data_WFP):
    output_file("scatter_rice_and_oil.html")

    countries_names = ['Djibouti', 'Haiti', 'India', 'Iran(Islamic Republic of)', 'Jordan', 'Mozambique', 'Pakistan', 'Somalia', 'Swaziland' , 'Syrian Arab Republic', 'Tajikistan', 'Congo', 'Myanmar' ]
    countries = [1,2,3,45,6,7,8,9,10,11,12,13]

    #rijst_prijzen = []

    for x in countries_names:
        rijst_prijzen = (data_WFP.loc[(data_WFP['adm0_name'] == x) & (data_WFP['cm_name'] == 'Rice'), 'mp_price'])
        #rijst_prijzen.append(gemiddelde_rijst_prijs)

    #olie_prijzen = []

    for x in countries_names:
        olie_prijzen = (data_WFP.loc[(data_WFP['adm0_name'] == x) & (data_WFP['cm_name'] == 'Oil'), 'mp_price'])
        #olie_prijzen.append(gemiddelde_olie_prijs)
    
    
    olie_cds = ColumnDataSource(olie_prijzen)
    rijst_cds = ColumnDataSource(rijst_prijzen)
 

    s1 = figure(title = "Oil and Rice prices", x_axis_label = "Oil price", y_axis_label = "Rice price")

    s1.toolbar.tools = [PanTool(), ResetTool(), WheelZoomTool(), HoverTool(), LassoSelectTool(), BoxSelectTool()]

    # And let us just move it to the top instead of the side.
    s1.toolbar_location='above'
    #TOOLS = "hover,pan,wheel_zoom,box_zoom,reset,save" 
    hover = s1.select(dict(type=HoverTool))
    
    s1.hover.tooltips = [
    ("Country", "$index"),
    ("Oil price:", "$x"),
    ("Rice price", "$y"), 
    ]
    s1.add_tools(BoxSelectTool(dimensions="width"))   
    s1.scatter(x=olie_prijzen, y=rijst_prijzen, color="blue")
    show(s1)
    return

rijst_olie_chart(data_WFP)

def example():
    from bokeh.plotting import figure, output_file, show, ColumnDataSource

    output_file("toolbar.html")

    source = ColumnDataSource(data=dict(
        x=[1, 2, 3, 4, 5],
        y=[2, 5, 8, 2, 7],
        desc=['A', 'b', 'C', 'd', 'E'],
    ))

    TOOLTIPS = [
        ("index", "$index"),
        ("(x,y)", "($x, $y)"),
        ("desc", "@desc"),
    ]

    p = figure(plot_width=400, plot_height=400, tools=TOOLTIPS,
            title="Mouse over the dots")

    p.circle('x', 'y', size=20, source=source)

    show(p)
    return

#example()

def rijst_mais_perjaar(data_WFP):
    output_file("scatter_rice_and_oil.html")

    countries_names = ['Djibouti', 'Haiti', 'India', 'Iran(Islamic Republic of)', 'Jordan', 'Mozambique', 'Pakistan', 'Somalia', 'Swaziland' , 'Syrian Arab Republic', 'Tajikistan', 'Congo', 'Myanmar' ]
    countries = [1,2,3,45,6,7,8,9,10,11,12,13]

    rijst_prijzen = []

    for x in countries_names:
        gemiddelde_rijst_prijs = (data_WFP.loc[(data_WFP['adm0_name'] == x) & (data_WFP['cm_name'] == 'Rice'), 'mp_price']).mean()
        rijst_prijzen.append(gemiddelde_rijst_prijs)

    olie_prijzen = []

    for x in countries_names:
        gemiddelde_olie_prijs = (data_WFP.loc[(data_WFP['adm0_name'] == x) & (data_WFP['cm_name'] == 'Oil'), 'mp_price']).mean()
        olie_prijzen.append(gemiddelde_olie_prijs)
    
    s1 = figure(title = "Oil and Rice prices", x_axis_label = "Oil price", y_axis_label = "Rice price")
    s1.scatter(olie_prijzen, rijst_prijzen, color="blue")
    show(s1)


    return





# Joshua de Roos
# 21-06-2018
# This program plots a choropleth map of the world with 
# all countries having a shade according to the price of a product.

from bokeh.io import show, output_notebook, output_file
from bokeh.layouts import row, widgetbox
from bokeh.models import (
    Legend,
    GeoJSONDataSource,
    Slider,
    HoverTool,
    CustomJS
)
from bokeh.plotting import figure
from bokeh.transform import linear_cmap
import json
import pandas as pd
import math
import random

# import necessary files
df_wfp = pd.read_csv('../../data/WFP_data_normalised.csv', encoding='latin-1')
countrycodes = pd.read_csv('../../data/countrycodes.csv', header=0, sep=',',
                           error_bad_lines=False, encoding='latin-1')

with open(r'../../data/countries.geo.json', 'r') as f:
    geo_data = json.load(f)


# makes new json file with geo and price data
def make_data_source(geo_data, df_wfp, countrycodes):
    countries = df_wfp['adm0_name'].unique()

    # combines prices of different grains in foodprice data
    df_wfp.loc[df_wfp['cm_name'].str.contains('Millet'), 'cm_name'] = 'Grain'
    df_wfp.loc[df_wfp['cm_name'].str.contains('Sorghum'), 'cm_name'] = 'Grain'
    df_wfp.loc[df_wfp['cm_name'].str.contains('Maize'), 'cm_name'] = 'Grain'
    df_wfp.loc[df_wfp['cm_name'] == 'Wheat', 'cm_name'] = 'Grain'
    df_wfp.loc[df_wfp['cm_name'].str.contains('Rice'), 'cm_name'] = 'Grain'

    # specifies year and product for world map
    good = df_wfp['cm_name'] == 'Grain'
    year = df_wfp['mp_year'] == 2017

    # list of colors and border values for map
    colors = ['#084594', '#2171b5', '#4292c6', '#6baed6', '#9ecae1', '#c6dbef',
              '#deebf7', '#f7fbff']
    colors.reverse()
    quants = [df_wfp.loc[good, 'mp_price'].quantile(x/8) for x in range(1, 9)]

    # assigns to every country a color based on price of product
    for country in geo_data['features']:
        code = country["id"]
        entry = list(countrycodes.loc[countrycodes['alpha-3'] == code, 'name'])
        if entry in countries:
            entry = df_wfp['adm0_name'] == entry[0]
            price = df_wfp.loc[good & year & entry, 'mp_price']
            price = price.mean()
            if math.isnan(price):
                country["properties"]["fill"] = "white"
                country["properties"]["price"] = "Unknown"
            else:
                for i in range(8):
                    if price < quants[i]:
                        country["properties"]["fill"] = colors[i]
                        country["properties"]["price"] = price
                        break
        else:
            country["properties"]["fill"] = "white"
            country["properties"]["price"] = "Unknown"

    # exports data to new json source
    return json.dumps(geo_data, ensure_ascii=True)

# def make_regions(geo_data, df_wfp, countrycodes):
#     # countries East Africa
#     east_africa = ['Mozambique', 'Zambia','United Republic of Tanzania', 'Madagascar', 'Malawi', 'Burundi', 'Afghanistan']
#     # countries Middle East
#     middle_east = ['Armenia', 'Iraq', 'Iran  (Islamic Republic of)','Turkey','Syrian Arab Republic', 'Jordan', 'Yemen','Afghanistan']
#     # countries West Afrika
#     west_africa = ['Mali', 'Algeria', "Cote d'Ivoire", 'Burkina Faso', 'Niger', 'Guinea', 'Guinea-Bissau', 'Ghana', 'Afghanistan']
#     # countries South Asia
#     asia = ['India', 'Pakistan', 'Bhutan', 'Bangladesh','Nepal', 'Sri Lanka', 'Afghanistan']
#     countries = east_africa + west_africa + middle_east + asia
#     regions = []
#     print(len(geo_data['features']))
#     for i in range(len(geo_data['features'])):
#         print(i)
#         country = geo_data['features'][i]
#         code = country["id"]
#         entry = list(countrycodes.loc[countrycodes['alpha-3'] == code, 'name'])

#         if entry and entry[0] in countries:
#             continue
#         else:
#             geo_data['features'].pop(i)

#     return json.dumps(geo_data, ensure_ascii=True)


# regions = make_regions(geo_data, df_wfp, countrycodes)


# plots choropleth map of world
def make_choropleth(data_source):
    # converts data to right format
    geo_source = GeoJSONDataSource(geojson=data_source)

    # plots countries with colors
    TOOLS = "pan,wheel_zoom,reset,hover,save"
    p = figure(title="Grain prices 2017", tools=TOOLS, x_axis_location=None,
               y_axis_location=None, width=1200, height=700)
    p.grid.grid_line_color = None
    p.patches(xs='xs', ys='ys', fill_color="fill",
              line_color='black', line_width=0.5, source=geo_source,
              legend="price")
    # p.patches(xs='xs', ys='ys', fill_color=None,
    #           line_color='black', line_width=1.0, source=geo_regions)        

    # sets properties of hovertool
    hover = p.select_one(HoverTool)
    hover.point_policy = "follow_mouse"
    hover.tooltips = [("Country:", "@name"), ("Grain price:", "@price")]

    output_file("choropleth_grain.html", title="World map Bokeh")
    show(p)


data_source = make_data_source(geo_data, df_wfp, countrycodes)
make_choropleth(data_source)

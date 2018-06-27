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
    CustomJS,
    BasicTickFormatter
)
from bokeh.plotting import figure
from bokeh.transform import linear_cmap
from bokeh.models import LinearColorMapper, FixedTicker, ColorBar, ContinuousColorMapper
import json
import pandas as pd
import math
import random
from bokeh.palettes import Blues8

# import necessary files
df_wfp = pd.read_csv('../../data/WFP_data_normalised.csv', encoding='latin-1')
countrycodes = pd.read_csv('../../data/countrycodes.csv', header=0, sep=',',
                           error_bad_lines=False, encoding='latin-1')
df_bbp = pd.read_excel('../../data/BBP_countries.xlsx')
df_pop = pd.read_csv('../../data/population_1960_2017_GOEDE.csv')

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
    time = 2015
    year = df_wfp['mp_year'] == time

    # list of colors and border values for map
    colors = ['#084594', '#2171b5', '#4292c6', '#6baed6', '#9ecae1', '#c6dbef',
              '#deebf7', '#f7fbff']
    colors.reverse()
    quants = [x/6 for x in range(1, 9)]

    # assigns to every country a color based on price of product
    for country in geo_data['features']:
        code = country["id"]
        entry = list(countrycodes.loc[countrycodes['alpha-3'] == code, 'name'])
        bbp = get_bbp(entry, time)
        pop = get_pop(entry, time)
        if entry in countries and entry[0] not in ['Somalia', 'Mauritania']:
            entry = df_wfp['adm0_name'] == entry[0]
            price = df_wfp.loc[good & year & entry, 'mp_price']
            price = price.mean()
            
            if math.isnan(price):
                country["properties"]["fill"] = "white"
                country["properties"]["price"] = "Unknown"
                country["properties"]["bbp"] = bbp
                country["properties"]["pop"] = pop
            else:
                for i in range(8):
                    if price < quants[i]:
                        country["properties"]["fill"] = colors[i]
                        country["properties"]["price"] = price
                        country["properties"]["bbp"] = bbp
                        country["properties"]["pop"] = pop
                        break
                    if price > quants[7]:
                        country["properties"]["fill"] = colors[7]
                        country["properties"]["price"] = price
                        country["properties"]["bbp"] = bbp
                        country["properties"]["pop"] = pop
                        break
        else:
            country["properties"]["fill"] = "white"
            country["properties"]["price"] = "Unknown"
            country["properties"]["bbp"] = bbp
            country["properties"]["pop"] = pop

    # exports data to new json source
    return json.dumps(geo_data, ensure_ascii=True)


def get_bbp(entry, time):
    if len(entry) > 0:    
        country = df_bbp['Country Name'] == entry[0]
        bbp = list(df_bbp.loc[country, str(time)])
        if len(bbp) > 0:
            return bbp[0]
        else:
            return "Unknown"


def get_pop(entry, time):
    if len(entry) > 0:    
        country = df_pop['Country_Name'] == entry[0]
        pop = list(df_pop.loc[country, str(time)])
        if len(pop) > 0:
            return pop[0]
        else:
            return "Unknown"

# plots choropleth map of world
def make_choropleth(data_source):
    # converts data to right format
    geo_source = GeoJSONDataSource(geojson=data_source)
    # plots countries with colors
    TOOLS = "pan,wheel_zoom,reset,hover,save"
    p = figure(title="Grain prices 2015 in USD", tools=TOOLS, x_axis_location=None,
               y_axis_location=None, width=1200, height=700)
    p.grid.grid_line_color = None
    p.title.align = "center"
    p.title.text_color = "#084594"
    p.title.text_font_size = "25px"
    p.background_fill_color = '#f7fbff'
    p.background_fill_alpha = 0.5

    p.patches(xs='xs', ys='ys', fill_color="fill",
              line_color='black', line_width=0.5, source=geo_source)
    # p.patches(xs='xs', ys='ys', fill_color=None,
    #           line_color='black', line_width=1.0, source=geo_regions) 
    # 
    palette = Blues8
    palette.reverse()
    mapper = LinearColorMapper( palette=palette, low=0, high=8/6)
    ticker = FixedTicker()
    ticker.ticks = [x/6 for x in range(1, 8)]
    color_bar = ColorBar(color_mapper=mapper, ticker=ticker,
                 label_standoff=12, border_line_color=None, location=(0,0),
                 orientation="horizontal")
    
    p.add_layout(color_bar, 'below')


    # sets properties of hovertool
    hover = p.select_one(HoverTool)
    hover.point_policy = "follow_mouse"
    hover.tooltips = [("Country:", "@name"), ("Grain price:", "@price"), ("Population:", "@pop"), ("GDP (USD):", "@bbp")]

    output_file("plots/choropleth_grain2015.html", title="World map Bokeh")
    show(p)


data_source = make_data_source(geo_data, df_wfp, countrycodes)
make_choropleth(data_source)

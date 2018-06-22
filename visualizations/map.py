from bokeh.io import show, output_notebook, output_file
from bokeh.layouts import row, widgetbox
from bokeh.models import (
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

df_wfp = pd.read_csv('../data/WFP_data_normalised.csv', encoding='latin-1')
countrycodes = pd.read_csv('../data/countrycodes.csv', header = 0, sep = ',', error_bad_lines=False, encoding = 'latin-1')

with open(r'countries.geo.json', 'r') as f:
    data = json.load(f)

countries = df_wfp['adm0_name'].unique()
df_wfp.loc[df_wfp['cm_name'].str.contains('Millet'), 'cm_name'] = 'Grain'
df_wfp.loc[df_wfp['cm_name'].str.contains('Sorghum'), 'cm_name'] = 'Grain'
df_wfp.loc[df_wfp['cm_name'].str.contains('Maize'), 'cm_name'] = 'Grain'
df_wfp.loc[df_wfp['cm_name'] == 'Wheat', 'cm_name'] = 'Grain'
df_wfp.loc[df_wfp['cm_name'].str.contains('Rice'), 'cm_name'] = 'Grain'

good = df_wfp['cm_name'] == 'Grain'
year = df_wfp['mp_year'] == 2017

max_price = df_wfp.loc[df_wfp['cm_name'] == 'Grain', 'mp_price'].quantile(0.98)

colors = ['#084594', '#2171b5', '#4292c6', '#6baed6', '#9ecae1', '#c6dbef', '#deebf7', '#f7fbff']
colors.reverse()
borders = [df_wfp.loc[df_wfp['cm_name'] == 'Grain', 'mp_price'].quantile(x/8) for x in range(1, 9)]
counter = 0
for country in data['features']:
    #country["properties"]["fill"] = "green"
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
                if price < borders[i]:
                    country["properties"]["fill"] = colors[i]
                    country["properties"]["price"] = price

                    break
    else:
        country["properties"]["fill"] = "white"
        country["properties"]["price"] = "Unknown"

   
test = json.dumps(data, ensure_ascii=True)
geo_source = GeoJSONDataSource(geojson=test)

TOOLS = "pan,wheel_zoom,box_zoom,reset,hover,save"

p = figure(title="Grain prices 2017", tools=TOOLS, x_axis_location=None, y_axis_location=None, width=1100, height=700)
p.grid.grid_line_color = None
p.patches(xs='xs', ys='ys', fill_color="fill",
          line_color='black', line_width=0.5, source=geo_source, legend="fill")

callback = CustomJS(args=dict(source=geo_source), code="""
    var data = source.data;
    var A = amp.value;
    var k = freq.value;
    var phi = phase.value;
    var B = offset.value;
    var x = data['x']
    var y = data['y']
    for (var i = 0; i < x.length; i++) {
        y[i] = B + A*Math.sin(k*x[i]+phi);
    }
    source.change.emit();
""")

amp_slider = Slider(start=1992, end=2018, value=1, step=1,
                    title="Amplitude", callback=callback)
#callback.args["amp"] = amp_slider

hover = p.select_one(HoverTool)
hover.point_policy = "follow_mouse"
hover.tooltips = [("Country:", "@name"), ("Grain price:", "@price")]

layout = row(
    p,
    widgetbox(amp_slider),
)

output_file("PBIar.html", title="World map Bokeh")

show(p)
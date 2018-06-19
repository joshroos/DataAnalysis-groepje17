# Joshua de Roos
# 18-06-2018
# Maakt kaart met rijst prijzen over de wereld

import geopandas as gpd
from bokeh.plotting import figure, show, output_file
from shapely.geometry import Polygon
from shapely.geometry import  MultiLineString, mapping, shape
from bokeh.models import Range1d

input_file = r"../data/countries_shp/countries.shp"
coordinates = gpd.read_file(input_file)
countries = coordinates['NAME'].unique()
long = []
lat = []
for country in countries:
    lines = coordinates.loc[coordinates['NAME'] == country, 'geometry']
    border_long = []
    border_lat = []
    for line in lines:
        line = mapping(line)
        coords = line['coordinates'][0]

        if country == 'United States':
            lines = mapping(lines)
            coords = lines['features'][0]['geometry']['coordinates']

        if type(coords[0]) is not float:
            for i in range(len(coords)):
                if type(coords[i][0]) is not float:
                    for j in range(len(coords[i])):
                        if type(coords[i][j][0]) is not float:
                            for k in range(len(coords[i][j])):
                                border_long.append(coords[i][j][k][0])
                                border_lat.append(coords[i][j][k][1])
                        else:
                            border_long.append(coords[i][j][0])
                            border_lat.append(coords[i][j][1])
                else:
                    border_long.append(coords[i][0])
                    border_lat.append(coords[i][1])
        else:
            border_long.append(coords[0])
            border_lat.append(coords[1])

    long.append(border_long)
    lat.append(border_lat)


p = figure(title="US Unemployment 2009", toolbar_location="left", tools=['hover', 'box_zoom', 'reset'],
           plot_width=1100, plot_height=700)

p.patches(long, lat, fill_alpha=1.0,fill_color="#D4B9DA",
          line_color="#884444", line_width=2, line_alpha=0.3)
p.y_range = Range1d(-90, 90)
p.x_range = Range1d(-180, 180)
output_file("choropleth.html", title="choropleth.py example")

show(p)
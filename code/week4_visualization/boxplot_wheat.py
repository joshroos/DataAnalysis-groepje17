import numpy as np
import pandas as pd
from bokeh.plotting import figure, show, output_file

# data all countries that contain the product wheat
df = pd.read_csv('../../data/WFP_data_normalised.csv' ,header=0, sep=',',
 error_bad_lines=False, encoding = 'latin-1')
yy = df.loc[df["cm_name"].str.contains("Wheat"), "mp_price"]
g = df.loc[df["cm_name"].str.contains("Wheat"), 'adm0_name']
countries = ['Afghanistan']

# dataframe
df = pd.DataFrame(dict(score=yy, group=g))

# find the quartiles and IQR for each category
groups = df.groupby('group')
q1 = groups.quantile(q=0.25)
q2 = groups.quantile(q=0.5)
q3 = groups.quantile(q=0.75)
iqr = q3 - q1
upper = q3 + 1.5*iqr
lower = q1 - 1.5*iqr

# show outliers
def outliers(group):
    countries = group.name
    return group[(group.score > upper.loc[countries]['score']) |
     (group.score < lower.loc[countries]['score'])]['score']
out = groups.apply(outliers).dropna()

# plot figure
p = figure(tools="save", background_fill_color="#E8F8F5", title="",
 x_range=countries)

# if no outliers, shrink lengths of stems to be no longer than
# the minimums or maximums
qmin = groups.quantile(q=0.00)
qmax = groups.quantile(q=1.00)
upper.score = [min([x,y]) for (x,y) in zip(list(qmax.loc[:,'score']),
upper.score)]
lower.score = [max([x,y]) for (x,y) in zip(list(qmin.loc[:,'score']),
lower.score)]

# stems
p.segment(countries, upper.score, countries, q3.score, line_color="black")
p.segment(countries, lower.score, countries, q1.score, line_color="black")

# boxes
p.vbar(countries, 0.7, q2.score, q3.score, fill_color="#9B59B6",
 line_color="black")
p.vbar(countries, 0.7, q1.score, q2.score, fill_color="#C0392B",
 line_color="black")

# whiskers
p.rect(countries, lower.score, 0.2, 0.01, line_color="black")
p.rect(countries, upper.score, 0.2, 0.01, line_color="black")

p.xgrid.grid_line_color = None
p.ygrid.grid_line_color = "white"
p.grid.grid_line_width = 2
p.xaxis.major_label_text_font_size="12pt"

output_file("plots/boxplot_wheat.html",
 title="boxplotwheat.py")

show(p)

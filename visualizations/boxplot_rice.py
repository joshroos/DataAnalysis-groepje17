import pandas as pd
import math
from bokeh.plotting import figure, show, output_file

# data all countries that contain the product rice
df = pd.read_csv('../data/WFP_data_normalised.csv' ,header=0, sep=',', error_bad_lines=False, encoding = 'latin-1')
yy = df.loc[df["cm_name"].str.contains("Rice"), "mp_price"]
g = df.loc[df["cm_name"].str.contains("Rice"), 'adm0_name']
countries = g.unique()
countries.sort()

df = pd.DataFrame(dict(score=yy, group=g))

# find IQR and quartiles for each group
groups = df.groupby('group')
q1 = groups.quantile(q=0.25)
q2 = groups.quantile(q=0.5)
q3 = groups.quantile(q=0.75)
iqr = q3 - q1
upper = q3 + 1.5*iqr
lower = q1 - 1.5*iqr

# countries Middle East
i_range = ['Armenia', 'Iraq', 'Iran  (Islamic Republic of)','Turkey','Syrian Arab Republic', 'Jordan', 'Yemen','Afghanistan']
# countries West Afrika
j_range = ['Mali', 'Algeria', "Cote d'Ivoire", 'Burkina Faso', 'Niger', 'Guinea', 'Guinea-Bissau', 'Ghana', 'Afghanistan']

# plot figure
p = figure(tools=["save", "hover", "box_zoom"], background_fill_color="#E8F8F5", title="Price of Rice West Africa", x_range=i_range)

# shrink lengths of stems to be no longer than the minimums or maximums
qmin = groups.quantile(q=0.00)
qmax = groups.quantile(q=1.00)
upper.score = [min([x,y]) for (x,y) in zip(list(qmax.loc[:,'score']),upper.score)]
lower.score = [max([x,y]) for (x,y) in zip(list(qmin.loc[:,'score']),lower.score)]
print(lower.score)
# stems
p.segment(countries, upper.score, countries, q3.score, line_color="black")
p.segment(countries, lower.score, countries, q1.score, line_color="black")

# boxes
p.vbar(countries, 0.7, q2.score, q3.score, fill_color="#9B59B6", line_color="black")
p.vbar(countries, 0.7, q1.score, q2.score, fill_color="#C0392B", line_color="black")

<<<<<<< HEAD
# whiskers
p.rect(countries, lower.score, 0.2, 0.01, line_color="black")
=======
# whiskers (almost-0 height rects simpler than segments)
>>>>>>> 0d46b3fb714d5d0151b0443bf6e186edf0695c31
p.rect(countries, upper.score, 0.2, 0.01, line_color="black")
p.rect(countries, lower.score, 0.2, 0.01, line_color="black")

# design boxplot
p.xgrid.grid_line_color = None
p.ygrid.grid_line_color = "white"
p.grid.grid_line_width = 2
p.xaxis.major_label_text_font_size="12pt"
p.axis.major_label_orientation = math.pi/4
p.yaxis.axis_label = "Dollar per KG"



output_file("boxplot.html", title="boxplot_rice_West_Africa.py Rice Price West Africa")

show(p)

# calculate average median Middle East
def calculate_median_i():
    i_range2 = ['Armenia', 'Iraq', 'Iran  (Islamic Republic of)','Turkey','Syrian Arab Republic', 'Jordan', 'Yemen']
    median_i_range = 0
    # add all median scores
    for i in i_range2:
        median_i_range += q2.score[i]
    # average median
    median_i_range = (median_i_range/len(i_range2))
    return median_i_range

# calculate average median West Africa
def calculate_median_j():
    median_j_range = 0
    j_range2 = ['Mali', 'Algeria', "Cote d'Ivoire", 'Burkina Faso', 'Niger', 'Guinea', 'Guinea-Bissau', 'Ghana']
    # add all median scores
    for j in j_range2:
        median_j_range += q2.score[j]
    # average median
    median_j_range = (median_j_range/len(j_range2))
    return median_j_range

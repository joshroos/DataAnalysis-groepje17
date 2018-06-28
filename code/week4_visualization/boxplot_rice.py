import pandas as pd
import math
from bokeh.plotting import figure, show, output_file

# data all countries that contain the product rice
df = pd.read_csv('../../data/WFP_data_normalised.csv' ,header=0, sep=',',
 error_bad_lines=False, encoding = 'latin-1')
yy = df.loc[df["cm_name"].str.contains("Rice"), "mp_price"]
g = df.loc[df["cm_name"].str.contains("Rice"), 'adm0_name']
countries = g.unique()
countries.sort()

# data frame
df = pd.DataFrame(dict(score=yy, group=g))

# find IQR and quartiles for each group
groups = df.groupby('group')
q1 = groups.quantile(q=0.25)
q2 = groups.quantile(q=0.5)
q3 = groups.quantile(q=0.75)
iqr = q3 - q1
upper = q3 + 1.5*iqr
lower = q1 - 1.5*iqr

# countries East Africa
EA_range = ['Mozambique', 'Zambia','United Republic of Tanzania', 'Madagascar',
 'Malawi', 'Burundi', 'Afghanistan']
# countries Middle East
ME_range = ['Armenia', 'Iraq', 'Iran  (Islamic Republic of)','Turkey',
'Syrian Arab Republic', 'Jordan', 'Yemen','Afghanistan']
# countries West Afrika
WA_range = ['Mali', 'Algeria', "Cote d'Ivoire", 'Burkina Faso', 'Niger',
 'Guinea', 'Guinea-Bissau', 'Ghana', 'Afghanistan']
# countries South Asia
SA_range = ['India', 'Pakistan', 'Bhutan', 'Bangladesh','Nepal', 'Sri Lanka',
 'Afghanistan']

# plot figure
p = figure(tools=["save", "hover", "box_zoom"], background_fill_color="#E8F8F5"
 , title="Price of Rice Middle East", x_range=ME_range)

# shrink lengths of stems to be no longer than the minimums or maximums
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

# whiskers (almost-0 height rects simpler than segments)
p.rect(countries, upper.score, 0.2, 0.01, line_color="black")
p.rect(countries, lower.score, 0.2, 0.01, line_color="black")

# design boxplot
p.xgrid.grid_line_color = None
p.ygrid.grid_line_color = "white"
p.grid.grid_line_width = 2
p.xaxis.major_label_text_font_size="12pt"
p.axis.major_label_orientation = math.pi/4
p.yaxis.axis_label = "Dollar per KG"

output_file("boxplot_rice.html", title="boxplot_rice.py")

show(p)

# calculate average median Middle East
def calculate_median_ME():
    ME_range2 = ['Armenia', 'Iraq', 'Iran  (Islamic Republic of)',
    'Turkey','Syrian Arab Republic', 'Jordan', 'Yemen']
    median_ME_range = 0
    # add all median scores
    for i in ME_range2:
        median_ME_range += q2.score[i]
    # average median
    median_ME_range = (median_ME_range/len(ME_range2))
    return median_ME_range

# calculate average median West Africa
def calculate_median_WA():
    median_WA_range = 0
    WA_range2 = ['Mali', 'Algeria', "Cote d'Ivoire", 'Burkina Faso',
     'Niger', 'Guinea', 'Guinea-Bissau', 'Ghana']
    # add all median scores
    for i in WA_range2:
        median_WA_range += q2.score[i]
    # average median
    median_WA_range = (median_WA_range/len(WA_range2))
    return median_WA_range

# calculate average median East Africa
def calculate_median_EA():
    median_EA_range = 0
    EA_range2 = ['Mozambique', 'Zambia','United Republic of Tanzania',
     'Madagascar', 'Malawi', 'Burundi']
    # add all median scores
    for i in EA_range2:
        median_EA_range += q2.score[i]
    # average median
    median_EA_range = (median_EA_range/len(EA_range2))
    return median_EA_range

# calculate average median South Asia
def calculate_median_SA():
    median_SA_range = 0
    SA_range2 = ['India', 'Pakistan', 'Bhutan', 'Bangladesh','Nepal',
     'Sri Lanka']
    # add all median scores
    for i in SA_range2:
        median_SA_range += q2.score[i]
    # average median
    median_SA_range = (median_SA_range/len(SA_range2))
    return median_SA_range

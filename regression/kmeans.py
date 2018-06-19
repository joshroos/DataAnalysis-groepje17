import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn.cluster import KMeans
import sklearn.metrics as sm
 
import pandas as pd
import numpy as np

from bokeh.layouts import gridplot, row, column

from bokeh.io import push_notebook, show, output_notebook
from bokeh.plotting import figure


x = pd.read_csv('all_data.csv')
x = x.drop(['Unnamed: 0', 'adm0_name', 'cm_name', 'mp_month', 'mp_year'], axis=1)
inertias = []
x = x.dropna()
for i in range(1, 100):
    model = KMeans(n_clusters=i)
    model.fit(x)
    inertias.append(model.inertia_)
print(inertias)

f = figure(plot_width=400, plot_height=250)

# Create the line
f.line(range(1, 15), inertias)

## Add some axis information
f.xaxis.axis_label = 'Number of Clusters'
f.yaxis.axis_label = 'Inertia'

show(f)
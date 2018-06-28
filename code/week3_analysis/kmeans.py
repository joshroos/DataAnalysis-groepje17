# Joshua de Roos
# 21-06-2018
# This program calculates the optimal number of clusters for the combined data

import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn.cluster import KMeans
import sklearn.metrics as sm
import pandas as pd
import numpy as np
from bokeh.layouts import gridplot, row, column
from bokeh.io import push_notebook, show, output_notebook
from bokeh.plotting import figure


# makes elbow graph of KMeans clustering
def make_elbow():
    # read necessary data
    x = pd.read_csv('../../data/all_data.csv')

    # drop not needed columns
    not_needed = ['Unnamed: 0', 'adm0_name', 'cm_name', 'mp_month', 'mp_year']
    x = x.drop(not_needed, axis=1)
    x = x.dropna()
    inertias = []

    # calculates inertia for i number of clusters
    for i in range(1, 100):
        model = KMeans(n_clusters=i)
        model.fit(x)
        inertias.append(model.inertia_)

    # makes elbow graph
    f = figure(plot_width=400, plot_height=250)

    # create the line
    f.line(range(1, 15), inertias)

    # add axis information
    f.xaxis.axis_label = 'Number of Clusters'
    f.yaxis.axis_label = 'Inertia'
    show(f)


make_elbow()

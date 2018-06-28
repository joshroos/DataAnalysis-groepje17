# Joshua de Roos
# 28 juni 2018
# This program does KMeans clustering for a dataframe and plots this clustered
# dataframe using tsne

import pandas as pd
import pylab
from sklearn.manifold import TSNE
from sklearn.cluster import KMeans

# make usable dataframe
df = pd.read_csv('all_data.csv')
df = df[df['adm0_name'] == 'Afghanistan']
not_needed = ['Unnamed: 0', 'adm0_name', 'cm_name', 'mp_month', 'mp_year']
df = df.drop(not_needed, axis=1)
df = df.dropna()


# clusters dataframe and plots with tsne
def tsne(df):
    model = KMeans(n_clusters=2)
    model.fit(df)

    X_tsne = TSNE(learning_rate=100).fit_transform(df)

    pylab.figure(figsize=(10, 5))
    pylab.scatter(X_tsne[:, 0], X_tsne[:, 1], c=df['mp_price'])
    pylab.show()


tsne(df)

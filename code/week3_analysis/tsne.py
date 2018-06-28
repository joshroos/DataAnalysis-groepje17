# Joshua de Roos
# 28 juni 2018

import pandas as pd
import pylab
from sklearn.manifold import TSNE
from sklearn.cluster import KMeans


df = pd.read_csv('all_data.csv')
df = df[df['adm0_name'] == 'Afghanistan']
df = df.drop(['Unnamed: 0', 'adm0_name', 'cm_name', 'mp_month', 'mp_year'], axis=1)
df = df.dropna()

model = KMeans(n_clusters=2)
model.fit(df)

X_tsne = TSNE(learning_rate=100).fit_transform(df)

pylab.figure(figsize=(10, 5))
pylab.scatter(X_tsne[:, 0], X_tsne[:, 1], c=df['mp_price'])
pylab.show()
import pandas as pd
import numpy as np
import matplotlib as plt

rng = np.random.RandomState(42)
df = pd.DataFrame(rng.randint(0, 10, (10,5)),
                  columns=['A', 'B', 'C', 'D', 'E'])
#print(df)

data = pd.read_csv('../data/WFPVAM_FoodPrices_05-12-2017.csv',encoding='latin-1')
#print(data.head())
#print(data)
#print(data['adm0_name'])
#print(data[['adm0_id','adm0_name']])
#print(data['adm0_name'].unique())

data_population = pd.read_csv('../data/population_countries_1960-2016.csv', encoding='latin-1')
print(data[1:20])

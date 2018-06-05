<<<<<<< HEAD
import pandas as pd
import numpy as np

rng = np.random.RandomState(42)
df = pd.DataFrame(rng.randint(0, 10, (10,5)),
                  columns=['A', 'B', 'C', 'D', 'E'])
#print(df)

data = pd.read_csv('testWFP.csv')
print(data)
=======
# Joshua de Roos en Ellen Bogaards
# 5 juni 2018
# Dit programma maakt van het csv-bestand van de WFP een overzichtelijke tabel

import matplotlib as plt
import pandas as pd



data = pd.read_csv('../data/WFPVAM_FoodPrices_05-12-2017.csv', encoding='latin-1')

print(data)
>>>>>>> master

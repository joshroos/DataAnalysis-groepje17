import pandas as pd
import numpy as np

rng = np.random.RandomState(42)
df = pd.DataFrame(rng.randint(0, 10, (10,5)),
                  columns=['A', 'B', 'C', 'D', 'E'])
print(df)

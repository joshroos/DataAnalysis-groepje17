# Joshua de Roos
# 19-06-2018

import pandas as pd
from pandas import Series,DataFrame

import sklearn
from sklearn.linear_model import LinearRegression

df = pd.read_csv('all_data.csv')
df = df.dropna()
# Create a LinearRegression Object
lreg = LinearRegression()

# Data Columns
X_multi = df.drop(['adm0_name', 'mp_month', 'mp_year', 'cm_name', 'mp_price'],1)
# Targets
Y_target = df['mp_price']

# Implement Linear Regression
lreg.fit(X_multi,Y_target)
print(len(Y_target))
print(' The estimated intercept coefficient is {0:.2f}'.format(lreg.intercept_))

print(' The number of coefficients used was {0:d}'.format(len(lreg.coef_)))

# Set a DataFrame from the Features
coeff_df = DataFrame(df.drop(['Unnamed: 0', 'adm0_name', 'mp_month', 'mp_year', 'cm_name', 'mp_price'],1).columns)
coeff_df.columns = ['Features']

# Set a new column lining up the coefficients from the linear regression
coeff_df["Coefficient Estimate"] = pd.Series(lreg.coef_)

# Show
print(coeff_df.sort_values(by='Coefficient Estimate', ascending=False))
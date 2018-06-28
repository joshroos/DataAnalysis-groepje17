# Joshua de Roos
# 19-06-2018
# This program runs a linear regression algorithm on all combined data and
# prints the coefficient for all 3 used variables

import pandas as pd
from pandas import Series, DataFrame
import sklearn
from sklearn.linear_model import LinearRegression

df = pd.read_csv('all_data.csv')
df = df.dropna()
print(len(df))


def make_regression(df):
    # Create a LinearRegression Object
    lreg = LinearRegression()

    # Data Columns
    not_needed = ['adm0_name', 'mp_month', 'mp_year', 'cm_name', 'mp_price']
    X_multi = df.drop(not_needed, 1)
    # Targets
    Y_target = df['mp_price']

    # Implement Linear Regression
    lreg.fit(X_multi, Y_target)
    print(len(Y_target))
    print(' The intercept coefficient is {0:.2f}'.format(lreg.intercept_))
    print(' The number of coefficients used was {0:d}'.format(len(lreg.coef_)))

    # Set a DataFrame from the Features
    not_needed = ['Unnamed: 0', 'adm0_name', 'mp_month', 'mp_year', 'cm_name',
                  'mp_price']
    coeff_df = DataFrame(df.drop(not_needed, 1).columns)
    coeff_df.columns = ['Features']

    # Set a new column lining up the coefficients from the linear regression
    coeff_df["Coefficient Estimate"] = pd.Series(lreg.coef_)

    # Show
    print(coeff_df.sort_values(by='Coefficient Estimate', ascending=False))


make_regression(df)

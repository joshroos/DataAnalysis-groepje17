from bokeh.plotting import figure
from bokeh.io import output_file, show
import matplotlib as plt
import pandas as pd
import io
from pandas import ExcelWriter
import numpy as np

data_WFP = pd.read_csv('../../data/WFP_data_normalised.csv', encoding='latin-1')
data_correlation = pd.read_csv('../../data/corrcoef.csv', encoding='latin-1')
data_combinations = pd.read_csv('../../data/combination_correlations.csv', encoding='latin-1')
correlation_goods = pd.read_csv('../../data/correlation_between_goods.csv', encoding='latin-1')

# makes combination_correlations.csv which counts the countries with high correlation per goods combinations
def best_correlation(data_correlation):
    products = data_WFP['cm_name'].unique()
    countries = []
    all_amounts = []
    combinations = []
    correlations = []

    for product1 in products:
        for product2 in products:
            if product1 != product2:
                group_correlations = []
                group_countries = []
                group_combinations = []
                amount = 0
                correlation1 = data_correlation.loc[(data_correlation['product1'] == product1) & (data_correlation['product2'] == product2),'correlation']
                country1 = data_correlation.loc[(data_correlation['product1'] == product1) & (data_correlation['product2'] == product2),'Country']
                correlation2 = data_correlation.loc[(data_correlation['product1'] == product2) & (data_correlation['product2'] == product1),'correlation'] 
                country2 = data_correlation.loc[(data_correlation['product1'] == product2) & (data_correlation['product2'] == product1),'Country']
                found_correlations = correlation1.tolist() + correlation2.tolist()
                found_countries = country1.tolist() + country2.tolist()
                n = 0

                for correlation_found in found_correlations:
                    if correlation_found >= 0.75:
                        group_correlations.append(correlation_found)
                        group_countries.append(found_countries[n])
                        amount += 1
                        combi = []
                        combi.append(product1)
                        combi.append(product2)
                        group_combinations.append(combi)
                        n += 1
                
                if group_countries != []:
                    countries.append(group_countries)
                
                if group_correlations != []:
                    correlations.append(group_correlations)

                if group_combinations != []:
                    combinations.append(group_combinations[0])
                
                if n != 0:
                    all_amounts.append(amount)
                
    print(correlations, countries, all_amounts, combinations)
    print(len(correlations), len(countries), len(all_amounts), len(combinations))

    # creates csv, with all high correlations, corresponding countries, amount of those countries, and the food combination
    download = "combination_correlations2.csv" 
    csv = open(download, "w") 
    columnTitleRow = "correlation, country, n, combinations\n"
    csv.write(columnTitleRow)

    for i in range(len(correlations)):
        row = str(correlations[i])  + "," + str(countries[i]) + "," + str(all_amounts[i]) + "," + str(combinations[i]) + "\n"
        csv.write(row)

    return         


# gives product combination, countries and correlations for n amount of high correlations
def find_things(data_combinations, n):

    correlations_combinations = data_combinations.loc[data_combinations['n'] == n, 'combinations']
    correlations_countries = data_combinations.loc[data_combinations['n'] == n, 'country']
    correlations = data_combinations.loc[data_combinations['n'] == n, 'correlation']
    combinations = correlations_combinations.tolist()
    countries = correlations_countries.tolist()
    correlations = correlations.tolist()

    countriesnew = []
    combinationsnew = []
    correlationsnew = []

    for x in range(len(combinations)):
        countriesnew.append(countries[x].split(' & '))
        combinationsnew.append(combinations[x].split(' & '))
        correlationsnew.append(correlations[x].split(' & '))
    
    print(countriesnew)
    print(combinationsnew)
    print(correlationsnew)
    return countriesnew, combinationsnew, correlationsnew


# prints all negative correlations in correlation_between_goods.csv 
def negative_correlations(correlation_goods):
    negative_correlation = correlation_goods.loc[correlation_goods['correlation'] < 0, 'food_combination']
    return negative_correlation


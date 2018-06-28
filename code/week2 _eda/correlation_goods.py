from bokeh.plotting import figure
from bokeh.io import output_file, show
import matplotlib as plt
import pandas as pd
import io
from pandas import ExcelWriter
import numpy as np

#rainfall = pd.read_csv('../data/rainfall_better.csv',header=0, sep=',', error_bad_lines=False, encoding = 'latin-1')
#exchangerate = pd.read_excel('../data/exchangerate_simple.xlsx',header=0, sep=',', error_bad_lines=False, encoding = 'latin-1')
data_WFP = pd.read_csv('../../data/WFP_data_normalised.csv', encoding='latin-1')
data_correlation = pd.read_csv('../../data/corrcoef.csv', encoding='latin-1')


# counts how many times a product combination has a high correlation in which countries
def best_correlation(data_correlation):
    
    products = data_WFP['cm_name'].unique()
    #products = ["Wheat", "Millet", "Maize"]
    countries = []
    all_amounts = []
    combinations = []
    correlations = []

    #compares the correlations of product combinations, and gives all countries that have that combination
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
                    
                    # if the correlation is high add them to the new csv
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

    download = "combination_correlations.csv" 
    csv = open(download, "w") 
    columnTitleRow = "correlation, country, n, combinations\n"
    csv.write(columnTitleRow)

    # every row of the new csv has the correlations, the countries with a high correlation, the amount of countries, the combination of goods
    for i in range(len(correlations)):
        row = str(correlations[i])  + "," + str(countries[i]) + "," + str(all_amounts[i]) + "," + str(combinations[i]) + "\n"
        csv.write(row)

    return         

data_combinations = pd.read_csv('../../data/combination_correlations.csv', encoding='latin-1')

# this finds the combinations with n amount of countries with high correlation and the food combination.
def find_things(data_combinations, n):

    correlations_combinations = data_combinations.loc[data_combinations['n'] == n, 'combinations']
    correlations_countries = data_combinations.loc[data_combinations['n'] == n, 'country']
    correlations = data_combinations.loc[data_combinations['n'] == n, 'correlation']
    combinations = correlations_combinations.tolist()
    countries = correlations_countries.tolist()
    correlations = correlations.tolist()

    #print(countries)
    #print(combinations)
    #print(correlations)

    countriesnew = []
    combinationsnew = []
    correlationsnew = []

    for x in range(len(combinations)):
        countriesnew.append(countries[x].split(' & '))
        combinationsnew.append(combinations[x].split(' & '))
        correlationsnew.append(correlations[x].split(' & '))
    
    #print(countriesnew)
    #print(combinationsnew)
    #print(correlationsnew)
    return combinationsnew

print(find_things(data_combinations, 5))

# this counts the amount of countries that has these two products.
def compare_amount(data_correlation):
    country = data_correlation.loc[data_correlation['combinations'] == 'Bulgur & Salt', 'country']
    country = country.tolist()
    countrynew = []

    for x in range(len(country)):
        countrynew.append(country[x].split(' & '))

    print(len(countrynew[0]))

    return


def compare_amount2(data_combinations):


    country = data_combinations.loc[data_combinations['combinations'] == 'Rice & Maize', 'country']
    country = country.tolist()
    countrynew = []
    print(country)
    for x in range(len(country)):
        countrynew.append(country[x].split(' & '))

    amount_total = len(countrynew[0])
    print(amount_total)

    correlations = find_things(data_combinations,13)
    for x in range(len(correlations)):
        print(len(correlations[x]))

    return


#compare_amount(data_correlation)

#best_correlation(data_correlation)


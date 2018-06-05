#Hallo allemaal

print("Helloo")

import matplotlib as plt
import pandas as pd
import os 
os.getcwd()
# your current working directory will be displayed
print(os.path.exists('exchangerate.csv'))
# Must be True, otherwise it is unrelated to pandas
dir_path = os.path.dirname(os.path.realpath('exchangerate.csv'))
print(dir_path)

data = pd.read_csv('Users\Gebruiker\Documents\GitHub\DataAnalysis-groepje17\code\exchangerate.csv', encoding='latin-1')

print(data)

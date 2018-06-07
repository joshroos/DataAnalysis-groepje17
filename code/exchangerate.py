#Hallo allemaal

print("Helloo")

import matplotlib as plt
import pandas as pd
import io

filename = '..\data\exchangerate.csv'
data = pd.read_csv(filename ,header=2, sep=',')
countries = ['Afghanistan', 'Algeria', 'Armenia', 'Azerbaijan', 'Bangladesh', 'Benin',
 'Bhutan', 'Bolivia', 'Burkina Faso', 'Burundi', 'Cambodia', 'Cameroon',
 'Cape Verde', 'Central African Republic', 'Chad', 'Colombia', 'Congo',
 'Costa Rica', "Cote d' Ivoire", 'Democratic Republic of the Congo',
 'Djibouti', 'El Salvador', 'Ethiopia', 'Gambia', 'Georgia', 'Ghana',
 'Guatemala', 'Guinea-Bissau', 'Guinea', 'Haiti', 'Honduras', 'India',
 'Indonesia', 'Iran', 'Iraq', 'Jordan', 'Kenya',
 'Kyrgyzstan', "Lao People's Democratic Republic", 'Lebanon', 'Lesotho',
 'Liberia', 'Madagascar', 'Malawi', 'Mali', 'Mauritania', 'Mozambique',
 'Myanmar', 'Nepal', 'Niger', 'Nigeria', 'Pakistan', 'Panama', 'Peru',
 'Philippines', 'Rwanda', 'Senegal', 'Somalia', 'Sri Lanka', 'Swaziland',
 'Syrian Arab Republic', 'Tajikistan', 'Timor-Leste', 'Turkey', 'Uganda',
 'Ukraine', 'United Republic of Tanzania', 'Yemen', 'Zambia', 'Zimbabwe',
 'State of Palestine', 'Sudan', 'Egypt', 'South Sudan']

# Create a Pandas Excel writer using XlsxWriter as the engine.
writer = pd.ExcelWriter('exchangerate_simple.xlsx', engine='xlsxwriter')

# Convert the dataframe to an XlsxWriter Excel object.
data.to_excel(writer, sheet_name='Sheet1')

# Close the Pandas Excel writer and output the Excel file.
writer.save()

print(data)
        


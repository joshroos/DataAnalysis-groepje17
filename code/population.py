
#data_population = pd.read_csv('../data/population_countries_1960-2016.csv', encoding='latin-1')
#print(data_population)

import matplotlib as plt
import pandas as pd
import io
from pandas import ExcelWriter


filename_pop = '../data/population_1960_2016.csv'
data = pd.read_csv(filename_pop ,header=0, sep=',', error_bad_lines=False, encoding = 'latin-1')
#print(data)
countries_WFP = {'Afghanistan':1, 'Algeria':1,'Armenia':1,'Azerbaijan':1,'Bangladesh':1,'Benin':1,
 'Bhutan':1,'Bolivia':1,'Burkina Faso':1,'Burundi':1,'Cambodia':1,'Cameroon':1,
 'Cape Verde':1,'Central African Republic':1,'Chad':1,'Colombia':1,'Congo':1,
 'Costa Rica':1,"Cote d' Ivoire":1,'Democratic Republic of the Congo':1,
 'Djibouti':1,'El Salvador':1,'Ethiopia':1,'Gambia':1,'Georgia':1,'Ghana':1,
 'Guatemala':1,'Guinea-Bissau':1,'Guinea':1,'Haiti':1,'Honduras':1,'India':1,
 'Indonesia':1,'Iran':1,'Iraq':1,'Jordan':1,'Kenya':1,
 'Kyrgyzstan':1,"Lao People's Democratic Republic":1,'Lebanon':1,'Lesotho':1,
 'Liberia':1,'Madagascar':1,'Malawi':1,'Mali':1,'Mauritania':1,'Mozambique':1,
 'Myanmar':1,'Nepal':1,'Niger':1,'Nigeria':1,'Pakistan':1,'Panama':1,'Peru':1,
 'Philippines':1,'Rwanda':1,'Senegal':1,'Somalia':1,'Sri Lanka':1,'Swaziland':1,
 'Syrian Arab Republic':1,'Tajikistan':1,'Timor-Leste':1,'Turkey':1,'Uganda':1,
 'Ukraine':1,'United Republic of Tanzania':1,'Yemen':1,'Zambia':1,'Zimbabwe':1,
 'State of Palestine':1,'Sudan':1,'Egypt':1,'South Sudan':1}

# schrijft bestand naar Excel file
#writer = ExcelWriter('exchangerate_simple.xlsx')
#data.to_excel(writer,'Sheet1')
#writer.save()

def Find_corresponding(data, countries_WFP):
    countries_population = data['Country_Name']
    corresponding = []
    not_corresponding = []
    corresponding_countries = []
    missing = []

    for country in countries_population:
        if countries_WFP.get(country) == 1:
            corresponding.append(country)
        else:
            not_corresponding.append(country)

    for country in countries_WFP:
        if country not in corresponding:
            missing.append(country)

    print("Amount WFP countries:",len(countries_WFP))
    print("corresponding:",corresponding)
    print("Amount corresponding:", len(corresponding))
    print("not corresponding:", not_corresponding)
    print("Amount not corresponding:", len(not_corresponding))
    print("missing:", missing)
    print("Amount missing:", len(missing))

    return

#print(data.iloc[0:10])
#print(data[column].isna().sum())
for i in range(len(data["Country_Name"])):
    if data["Country_Name"][i] not in countries_WFP:
        data = data.drop(i)
years = [str(i) for i in range(1960, 1992)]
data = data.drop(years, axis = 1)

writer = ExcelWriter('population_1960_2016.xlsx')
data.to_excel(writer,'Population_excel')
writer.save()

population_with_2017 = pd.read_csv('../data/population_1960_2017_GOEDE.csv',header=0, sep=',', error_bad_lines=False, encoding = 'latin-1')
print(population_with_2017)
#list = ['Country_Name','Country_Code','Indicator_Name','Indicator_Code','1992','1993','1994','1995','1996','1997','1998','1999','2000','2001','2002','2003','2004','2005','2006','2007','2008','2009','2010','2011','2012','2013','2014','2015','2016','2017']
#print(len(list))
#print(population_with_2017['2017'].isna().sum())
#for i in population_with_2017.iloc:


"""
Example 1

"""


# coding: utf-8

# # Global numbers by year



# Import necessary packages
from pop_projection import Effectifs as eff
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt



# Define law of replacement
def law_replacement1(departures_, year_):
    
    '''
        assumes departures_ is a dic storing number of departures by group of the year year_
        returns a list of dics having keys : key, number and data
        
    '''
    def nouveaux(g_):
        structure_nouveaux = {'1':[25,25,0.8],'2':[25,25,0.8],'3':[25,25,0.6],'4':[29,29,0.6],'5':[28,28,0.5,],
        '6':[28,28,0.5],'7':[33,33,0.5],'8':[38,38,0.5],'9':[38,38,0.5],'10':[47,47,0.5],'11':[49,49,0.5]}

        if str(g_) in structure_nouveaux:
            return structure_nouveaux[str(g_)]
        else:
            return [30, 30, 1.0]

    def taux_rempl(y, g_ = '0'):
        if y <= 3 :
            if str(g_) in ['1','2','3','5','6','7']:
                return 0.64
            else:
                return 1
        else:
            return 1

    new_employees = []

    for g in departures_:
        # add a male
        if nouveaux(g)[2] > 0:
            temp = {'key':'male_groupe_' + str(g) + 'year_' + str(year_), 
            'number':nouveaux(g)[2]*departures_[g]*taux_rempl(year_, g),'data':['active', 'male', 'not married', nouveaux(g)[0], 1]}
            new_employees.append(temp)

        # add a female
        if nouveaux(g)[2] < 1:
            temp = {'key':'female_groupe_' + str(g) + 'year_' + str(year_), 
            'number':(1-nouveaux(g)[2])*departures_[g]*taux_rempl(year_, g),'data':['active', 'female', 'not married', nouveaux(g)[1], 1]}
            new_employees.append(temp)
    
    return new_employees

# Path for input data
path ="./pop_projection/data/"

# Loading data
employees = pd.read_csv(path + "employees - Copie.csv",sep=";", decimal = ",")
spouses = pd.read_csv(path + "spouses.csv",sep=";", decimal = ",")
children = pd.read_csv(path + "children.csv",sep=";", decimal = ",")

# Diplay some data
print('Employees :')
print(employees.head(10))
print('Spouses :')
print(spouses.head(10))
print('Children :')
print(children.head(10))

# Projection of population
# Number of years to project
MAX_ANNEES = 100

# Projection
numbers_ = eff.projectNumbers(employees, spouses, children, 'TV 88-90', MAX_ANNEES, law_replacement_ = law_replacement1)

# global numbers
global_numb = eff.globalNumbers(numbers_[0], numbers_[1], numbers_[2], MAX_ANNEES)

# printing results
print(global_numb)

print(eff.individual_employees_numbers(numbers_[0])[0])
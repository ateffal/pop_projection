
# coding: utf-8

# # Projecting slaries using projected individual numbers
# # #####################################################

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

    print(departures_)

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
            temp = {'key':'male_groupe_' + str(g) + '_year_' + str(year_), 
            'number':nouveaux(g)[2]*departures_[g]*taux_rempl(year_, g),'data':['active', 'male', 'not married', nouveaux(g)[0], year_,g,'01/01/'+str((2018+year_+1)),'31/12/'+str((2018+year_-nouveaux(g)[0]))]}
            new_employees.append(temp)

        # add a female
        if nouveaux(g)[2] < 1:
            temp = {'key':'female_groupe_' + str(g) + 'year_' + str(year_), 
            'number':(1-nouveaux(g)[2])*departures_[g]*taux_rempl(year_, g),'data':['active', 'female', 'not married', nouveaux(g)[1], year_,g,'01/01/'+str((2018+year_+1)),'31/12/'+str((2018+year_-nouveaux(g)[1]))]}
            new_employees.append(temp)
    
    return new_employees

# Path for input data
path ="./pop_projection/data/"

# Loading data
employees = pd.read_csv(path + "employees.csv",sep=";", decimal = ",")
spouses = pd.read_csv(path + "spouses.csv",sep=";", decimal = ",")
children = pd.read_csv(path + "children.csv",sep=";", decimal = ",")


# Projection of population
# Number of years to project
MAX_ANNEES = 3

# Projection
numbers_ = eff.simulerEffectif(employees, spouses, children, 'TV 88-90', MAX_ANNEES, law_replacement_ = law_replacement1)

# Getting individual numbers projection for employees
lives, deaths, resignation, type_ = eff.individual_employees_numbers(numbers_[0])

# printing new employees
df = eff.new_employees(numbers_[0], MAX_ANNEES)
print(df.tail(10))



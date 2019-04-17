# -*- coding: utf-8 -*-
"""
Created on Wed Dec 12 08:35:33 2018

@author: a.teffal
"""

from pop_projection import Effectifs as eff
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pop_projection import sample_laws as sl

# Path for input data
path = "./pop_projection/data/"

# Number of years to project
MAX_ANNEES = 100

# Loading data
employees = pd.read_csv(path + "employees.csv",sep=";", decimal = ",")
spouses = pd.read_csv(path + "spouses.csv",sep=";", decimal = ",")
children = pd.read_csv(path + "children.csv",sep=";", decimal = ",")


# Projection of population
numbers_ = eff.simulerEffectif(employees, spouses, children, 'TV 88-90', MAX_ANNEES, 
                               law_replacement_ = sl.law_replacement1, law_marriage_=sl.law_mar1)

ind_emp_numbers = eff.individual_employees_numbers(numbers_[0])

ind_emp_numbers[0].to_csv("Employees_lives.csv", sep=';')

employees_proj = ind_emp_numbers[0]

year = 'year_'

for i in range(1, MAX_ANNEES // 10):
    
    emp_grouped = employees_proj.groupby(['age','sex'], as_index=False)[year + str((i - 1) * 10)].sum()
    
    max_age = 100 # 101
    
    min_age = 19
    
    #update colum age to be age at year (i-1)*10
    emp_grouped['age'] = emp_grouped['age'] - MAX_ANNEES + (i - 1) * 10
    
    emp_grouped = emp_grouped.loc[(emp_grouped['age'] < max_age) & (emp_grouped['age'] > min_age)]
    
    table = pd.pivot_table(emp_grouped, values=year + str((i - 1) * 10), index=['age'],  columns=['sex'], aggfunc=np.sum)
    
    table = table.fillna(0)
    
    #calculate percentage
    if 'male' in list(table.columns):
        table['male'] = table['male'] / np.sum(table['male'])
    if 'female' in list(table.columns):
        table['female'] = table['female'] / np.sum(table['female'])
    
    if 'female' in list(table.columns):
        table['female'] = table['female'] * (-1)
    
    plt.subplot(4 , 4, i)
    plt.subplots_adjust(hspace = 0.5)
    plt.xlim(-0.05,0.05)
    plt.title('Year ' + str((i - 1) * 10))
    
    if 'male' in list(table.columns):
        values = [0] * (max_age - min_age - 1)
        for i in range(len(table['male'])):
            values[table.index[i] - min_age - 1] = table.iloc[i]['male']
        p_male = plt.barh(list(range(min_age + 1, max_age)), values, color = (149 / 255,125 / 255,98 / 255))
    
    if 'female' in list(table.columns):
        for i in range(len(table['female'])):
            values[table.index[i] - min_age - 1] = table.iloc[i]['female']
        p_female = plt.barh(list(range(min_age + 1, max_age)), values, color = (0 / 255,128 / 255,0 / 255))

    plt.figlegend((p_male[0], p_female[0]), ('Men', 'Women'), loc = 'lower center')
    plt.suptitle('Evolution of Ages Pyramid')

plt.show()

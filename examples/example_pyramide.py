# -*- coding: utf-8 -*-
"""
Created on Wed Dec 12 08:35:33 2018

@author: a.teffal
"""

# Spouses Ages Pyramid by mortality table at year 50

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
employees = pd.read_csv(path + "employees.csv", sep=";", decimal=",")
spouses = pd.read_csv(path + "spouses.csv", sep=";", decimal=",")
children = pd.read_csv(path + "children.csv", sep=";", decimal=",")

tables = ['TD 73-77', 'TD 90-92', 'TV 88-90', 'USA_2009']

year_ = 51

plot_num = 1

min_age_ = 19

max_age_ = 100

color_males = (149/255, 125/255, 98/255)
color_females = (0/255, 128/255, 0/255)

for t in tables:

    # Projection of population
    numbers_ = eff.projectNumbers(employees, spouses, children, t, MAX_ANNEES,
                                  law_replacement_=sl.law_replacement1, law_marriage_=sl.law_mar1)

    # Pyramid of spouses
    ind_spo_numbers = eff.individual_spouses_numbers(numbers_[1])
    spouses_proj = ind_spo_numbers[0]

    emp_grouped = spouses_proj.groupby(['age', 'sex'], as_index=False)[
        'year_'+str((year_-1))].sum()

    # update colum age to be age at year (year_-1)
    emp_grouped['age'] = emp_grouped['age'] - MAX_ANNEES + (year_-1)

    emp_grouped = emp_grouped.loc[(emp_grouped['age'] < max_age_) & (
        emp_grouped['age'] > min_age_)]

    table = pd.pivot_table(emp_grouped, values='year_'+str((year_-1)),
                           index=['age'],  columns=['sex'], aggfunc=np.sum)

    table = table.fillna(0)

    # calculate percentage
    if 'male' in list(table.columns):
        table['male'] = table['male']/np.sum(table['male'])
    if 'female' in list(table.columns):
        table['female'] = table['female']/np.sum(table['female'])

    if 'female' in list(table.columns):
        table['female'] = table['female'] * (-1)

    plt.subplot(len(tables), 1, plot_num)
    plt.subplots_adjust(hspace=0.5)
    plt.xlim(-0.05, 0.05)
    plt.title('Mortality table ' + t)

    if 'male' in list(table.columns):
        values = [0] * (max_age_ - min_age_ - 1)
        for i in range(len(table['male'])):
            values[table.index[i] - min_age_ - 1] = table.iloc[i]['male']
        p_male = plt.barh(list(range(min_age_ + 1, max_age_)),
                          values, color=color_males)

    if 'female' in list(table.columns):
        for i in range(len(table['female'])):
            values[table.index[i] - min_age_ - 1] = table.iloc[i]['female']
        p_female = plt.barh(list(range(min_age_ + 1, max_age_)),
                            values, color=color_females)
    plot_num += 1
    plt.figlegend((p_male[0], p_female[0]),
                  ('Men', 'Women'), loc='lower center')

plt.suptitle('Spouses Ages Pyramid by mortality table at year 50')
plt.show()

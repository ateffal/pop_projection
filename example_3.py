# coding: utf-8

# # Projecting slaries using projected individual numbers
# # #####################################################

# Import necessary packages
from pop_projection import Effectifs as eff
from pop_projection import Cashflows as cf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import inspect
import time


print('Début : ', time.asctime( time.localtime(time.time())))

def salaries_new_emp_1(new_employees):
    """
        Returns a data frame containing for each new employee his salary the he entered
        the population.

        Parameters:
            new_employees (DataFrame): a DataFrame containing all column data for new employees
            plus a column entrance (the year this new employee entered the population).

        Returns:
            DataFrame: A DataFrame containing projected salaries for each new employee.
    """

    ids = list(new_employees['id'])
    salaries = [0] * len(ids)

    i = 0
    for e in list(new_employees['entrance']):
        salaries[i] = 1000 * (1 + 0.02) ** e
        i = i + 1

    temp_df = pd.DataFrame()

    temp_df['id'] = ids
    temp_df['salary'] = salaries

    return temp_df


# Define law of replacement
def law_replacement1(departures_, year_):
    '''
        assumes departures_ is a dic storing number of departures by group of the year year_
        returns a list of dics having keys : key, number and data

    '''

    def nouveaux(g_):
        structure_nouveaux = {'1': [25, 25, 0.8], '2': [25, 25, 0.8], '3': [25, 25, 0.6], '4': [29, 29, 0.6],
                              '5': [28, 28, 0.5, ],
                              '6': [28, 28, 0.5], '7': [33, 33, 0.5], '8': [38, 38, 0.5], '9': [38, 38, 0.5],
                              '10': [47, 47, 0.5], '11': [49, 49, 0.5]}

        if str(g_) in structure_nouveaux:
            return structure_nouveaux[str(g_)]
        else:
            return [30, 30, 1.0]

    def taux_rempl(y, g_='0'):
        if y <= 3:
            if str(g_) in ['1', '2', '3', '5', '6', '7']:
                return 0.64
            else:
                return 1
        else:
            return 1

    new_employees = []

    for g in departures_:
        if departures_[g] > 0:
            # add a male
            if nouveaux(g)[2] > 0:
                temp = {'key': 'male_groupe_' + str(g) + '_year_' + str(year_),
                        'number': nouveaux(g)[2] * departures_[g] * taux_rempl(year_, g),
                        'data': ['active', 'male', 'not married', nouveaux(g)[0], year_, g,
                                 '01/01/' + str((2018 + year_ + 1)), '31/12/' + str((2018 + year_ - nouveaux(g)[0]))]}
                new_employees.append(temp)

            # add a female
            if nouveaux(g)[2] < 1:
                temp = {'key': 'female_groupe_' + str(g) + 'year_' + str(year_),
                        'number': (1 - nouveaux(g)[2]) * departures_[g] * taux_rempl(year_, g),
                        'data': ['active', 'female', 'not married', nouveaux(g)[1], year_, g,
                                 '01/01/' + str((2018 + year_ + 1)), '31/12/' + str((2018 + year_ - nouveaux(g)[1]))]}
                new_employees.append(temp)

    return new_employees


# Path for input data
path = "../data_2018/"

# Loading data
employees = pd.read_csv(path + "employees.csv", sep=";", decimal=",")
spouses = pd.read_csv(path + "spouses.csv", sep=";", decimal=",")
children = pd.read_csv(path + "children.csv", sep=";", decimal=",")

# Loading salaries
salaries = pd.read_csv(path + "salaries.csv", sep=";", decimal=",")

# Loading pensions
pensions = pd.read_csv(path + "pensions2.csv", sep=";", decimal=",")

print('Chargement données : ', time.asctime( time.localtime(time.time())))

# Projection of population
# Number of years to project
MAX_ANNEES = 120

# Projection
numbers_ = eff.simulerEffectif(
    employees, spouses, children, 'TV 88-90', MAX_ANNEES, law_replacement_=None)

print('Simulation effectifs : ', time.asctime( time.localtime(time.time())))

df_salaries = cf.project_salaries(numbers_[0], salaries, MAX_ANNEES, salaries_new_emp_1, 0.035)

print('Projection salaires : ', time.asctime( time.localtime(time.time())))

# rate_contr = pd.read_csv(path + "rate_contr.csv", sep=";", decimal=",")

def rate_contr(sex, year):
    if year >5:
        return 0
    if sex=='male':
        return 0
    else:
        return 0.1

df_contr = cf.project_contributions(df_salaries,rate_contr,20)

print('Projection contributions : ', time.asctime( time.localtime(time.time())))

def f_pension(data, salaries , year):
    return 1000

df_pensions = cf.project_pensions(numbers_[0], df_salaries, pensions, f_pension,MAX_ANNEES,0.0275)

print('Projection pensions : ', time.asctime( time.localtime(time.time())))

df_salaries.to_csv('./results/projected_salaries.csv', sep=';', index=False, decimal=',')
df_contr.to_csv('./results/projected_contributions.csv', sep=';', index=False, decimal=',')
df_pensions.to_csv('./results/projected_penions.csv', sep=';', index=False, decimal=',')

print('Fin : ', time.asctime( time.localtime(time.time())))

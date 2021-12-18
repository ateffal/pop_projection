

# Example 4 : Global numbers by year


# coding: utf-8

# # Global numbers by year


# Import necessary packages
from pop_projection import Effectifs as eff
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def turnover(age):
    """
    Return the probability of quitting during the following year at a given age

    """
    if age < 30:
        return 0.02
    else:
        if age < 45:
            return 0.01
        else:
            return 0


def law_mar_1(age, familyStatus):
    """
    Return the probability of getting maried  during the following year at a given age for a given sex

    """

    if familyStatus == 'married':
        return 0

    if age >= 35:
        return 1

    return 0


def law_mar_2(age, sex, type):
    """
    Return the probability of getting maried  during the following year at a given age for a given sex

    """
    if type == 'active':
        if age >= 25 and age <= 54:
            return 0.04
        else:
            return 0
    else:
        return 0


def law_mar_3(age, year_proj):
    """
    Return the probability of getting maried  during the following year at a given age for a given sex

    """

    if year_proj == 1 and (age-year_proj) >= 35:
        return 1

    if age == 35:
        return 1

    return 0


def loi_naiss_1(age):
    """
    Return the probability of having a new born  during the following year at a given age

    """
    if age < 23:
        return 0
    if age > 40:
        return 0

    temp = [0.2212, 0.08, 0.0978, 0.115, 0.1305, 0.1419, 0.148, 0.1497, 0.1434,
            0.1353, 0.1239, 0.1095, 0.095, 0.08, 0.0653, 0.0516, 0.0408, 0.086]

    return temp[age - 23]


def loi_naiss_2(age_agent, age_conjoint, sexe_agent, sexe_conjoint):
    """
    Return the probability of having a new born  during the following year at a given age

    """

    if sexe_agent == 'male':
        age = age_conjoint
    else:
        age = age_agent

    if age < 23:
        return 0
    if age > 40:
        return 0

    temp = [0.2212, 0.08, 0.0978, 0.115, 0.1305, 0.1419, 0.148, 0.1497, 0.1434,
            0.1353, 0.1239, 0.1095, 0.095, 0.08, 0.0653, 0.0516, 0.0408, 0.086]

    return temp[age - 23]


def loi_naiss_3(age):
    if age == 35:
        return 1
    else:
        return 0


def loi_naiss_4(children_number, year_proj, age, familyStatus):
    if age == 32 or age == 38:
        if children_number[year_proj-1] < 3:
            return 1
        else:
            return 0
    else:
        return 0


def loi_naiss_5(children_number, year_proj, age, familyStatus):
    if familyStatus == 'not married':
        if age >= 38:
            return 2
        if age >= 32 and age < 38:
            return 1
        if age < 32:
            return 0

    if familyStatus == 'married':
        if children_number[year_proj-1] == 0:
            if age >= 38:
                return 2
            if age >= 32 and age < 38:
                return 1
            if age < 32:
                return 0

        if children_number[year_proj-1] > 0 and children_number[year_proj-1] <= 1:
            if age >= 38:
                return (2-children_number[year_proj-1])
            else:
                return 0
        return 0
    return 0


# Define law of replacement
def law_replacement1(departures_, year_):
    '''
        assumes departures_ is a dic storing number of departures by group of the year year_
        returns a list of dics having keys : key, number and data

    '''
    def nouveaux(g_):
        structure_nouveaux = {'1': [25, 25, 0.8], '2': [25, 25, 0.8], '3': [25, 25, 0.6], '4': [29, 29, 0.6], '5': [28, 28, 0.5, ],
                              '6': [28, 28, 0.5], '7': [33, 33, 0.5], '8': [38, 38, 0.5], '9': [38, 38, 0.5], '10': [47, 47, 0.5], '11': [49, 49, 0.5]}

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
        # add a male
        if nouveaux(g)[2] > 0:
            temp = {'key': 'male_groupe_' + str(g) + 'year_' + str(year_),
                    'number': nouveaux(g)[2]*departures_[g]*taux_rempl(year_, g), 'data': ['active', 'male', 'not married', nouveaux(g)[0], year_+2018, g, 0]}
            new_employees.append(temp)

        # add a female
        if nouveaux(g)[2] < 1:
            temp = {'key': 'female_groupe_' + str(g) + 'year_' + str(year_),
                    'number': (1-nouveaux(g)[2])*departures_[g]*taux_rempl(year_, g), 'data': ['active', 'female', 'not married', nouveaux(g)[1], year_+2018, g, 0]}
            new_employees.append(temp)

    return new_employees


# Path for input data
path = "../pop_projection/data/"

# Path for exporting results
path_exp = "./results/"

# Loading data
employees = pd.read_csv(path + "employees.csv", sep=";", decimal=",")
spouses = pd.read_csv(path + "spouses.csv", sep=";", decimal=",")
children = pd.read_csv(path + "children.csv", sep=";", decimal=",")

# Diplay some data
# print('Employees :')
# print(employees.head(10))
# print('Spouses :')
# print(spouses.head(10))
# print('Children :')
# print(children.head(10))

# Projection of population
# Number of years to project
MAX_ANNEES = 50

# Projection
cols_birth = [('age', 'employees'), ('age', 'spouses'),
              ('sex', 'employees'), ('sex', 'spouses')]
numbers_ = eff.projectNumbers(employees, spouses, children, 'TV 88-90', MAX_ANNEES,
                              law_replacement_=law_replacement1,
                              law_marriage_=(law_mar_3, ['age', 'year_proj']),
                              law_birth_=loi_naiss_5, law_resignation_=turnover)


# global numbers
global_numb = eff.globalNumbers(
    numbers_[0], numbers_[1], numbers_[2], MAX_ANNEES)

# printing results
# print(global_numb)

# export global numbers
global_numb.to_csv(path_exp + "global_numbers.csv",
                   index=False, sep=";", decimal=",")


# eff.get_cols_values(numbers_[0],'id1', ['sex', 'SIR', 'age'])

indiv_empl = eff.individual_employees_numbers(numbers_[0])
indiv_empl[0].to_csv(
    path_exp + "individual_employees_lives.csv", index=False, sep=";", decimal=",")


indiv_spouses = eff.individual_spouses_numbers(numbers_[1])
indiv_spouses[4].to_csv(
    path_exp + "individual_spouses_res.csv", index=False, sep=";", decimal=",")


print("Global numbers exported successfuly !")

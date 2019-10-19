import pop_projection.Effectifs as eff
import pandas as pd


# Define law of retirement
def law_ret1(age, year_emp):
    if year_emp < 2002:
        if age+1 >= 55:
            return True
        else:
            return False
    if year_emp >= 2002:
        if age+1 >= 60:
            return True
        else:
            return False

# Define law of reignation


def law_resignation_1(age, sexe):
    if age+1 >= 50:
        return 0
    if sexe == 'female':
        if age+1 <= 30:
            return 0.02
        else:
            return 0.01
    if sexe == 'male':
        if age+1 <= 30:
            return 0.02
        else:
            return 0.01


# Define law of marriage
def law_mar1(age, sexe, typeAgent):
    """
    Return the probability of getting maried  during the following year at a given age for a given sex

    """
    if sexe == 'male':
        if typeAgent == 'active':
            if age >= 25 and age <= 54:
                return 0.095
            else:
                return 0
        else:
            return 0

    if sexe == 'female':
        if typeAgent == 'active':
            if age >= 25 and age <= 54:
                return 0.15
            else:
                return 0
        else:
            return 0

# Define law of replacement


def law_replacement1(departures_, year_):
    '''
        assumes departures_ is a dic storing number of departures by group of the year year_
        returns a list of dics having keys : sex, age, number and group

    '''
    new_employees = []

    for g in departures_:
        temp = {'sex': 'male', 'age': 30, 'number': departures_[g], 'group': g}
        new_employees.append(temp)

    return new_employees


# Path for input data
path = "./pop_projection/data/"

# Number of years to project
MAX_ANNEES = 50

# Loading data
employees = pd.read_csv(path + "employees.csv", sep=";", decimal=",")
spouses = pd.read_csv(path + "spouses.csv", sep=";", decimal=",")
children = pd.read_csv(path + "children.csv", sep=";", decimal=",")

# Projection of population
numbers_ = eff.projectNumbers(employees, spouses, children, 'TV 88-90', MAX_ANNEES, (law_ret1, ['age', 'Year_employment']),
                              (law_resignation_1, ['age', 'sex']), (law_mar1, ['age', 'sex', 'type']), law_replacement_=None)

# Global numbers
Effectifs = eff.globalNumbers(
    numbers_[0], numbers_[1], numbers_[2], MAX_ANNEES)

Effectifs.to_csv('Effectifs_python.csv', sep=';', index=False, decimal=',')

# Number of actives leaving population : deaths, resignations, and new retired
Leaving = eff.leavingNumbers(numbers_[0], numbers_[4], MAX_ANNEES)

Leaving.to_csv('Sortants_python.csv', sep=';', index=False, decimal=',')


# export projected employees
pd.DataFrame.from_dict(numbers_[0]).to_csv(
    'employees_proj.csv', sep=';', index=False, decimal=',')

# export projected spouses
pd.DataFrame.from_dict(numbers_[1]).to_csv(
    'spouses_proj.csv', sep=';', index=False, decimal=',')

# export projected children
pd.DataFrame.from_dict(numbers_[2]).to_csv(
    'children_proj.csv', sep=';', index=False, decimal=',')

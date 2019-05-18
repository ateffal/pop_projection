
# coding: utf-8

# # Projecting slaries using projected individual numbers
# # #####################################################

# Import necessary packages
from pop_projection import Effectifs as eff
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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
    salaries = [0]*len(ids)

    i = 0
    for e in list(new_employees['entrance']):
        salaries[i] = 1000 * (1+0.02)**e
        i = i+1

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
        if departures_[g] > 0 :
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

# Loading salaries
salaries = pd.read_csv(path + "salaries.csv",sep=";", decimal = ",")


# Projection of population
# Number of years to project
MAX_ANNEES = 20

# Projection
numbers_ = eff.simulerEffectif(employees, spouses, children, 'TV 88-90', MAX_ANNEES, law_replacement_ = law_replacement1)


def project_contributions(projected_salaries, rate_contribution, MAX_YEARS):

    return None


def project_salaries(employees_proj_, salaries, MAX_YEARS, salaries_new_emp = None, sal_evol = 0):
    """ 
        Returns a DataFrame containing annual projection of the salaries.
  
        Parameters: 
            employees_proj_ (dic): a dic containing projected employees in the form of those 
                                   returned by simulerEffectif.
                                   
            salaries (DataFrame) : A DataFrame containing for each employee (including new employees if 
                                   salaries_new_emp is None ) his salary at year 0 (at year of entrance 
                                   if it's a new employee).

            MAX_YEARS (int): Number of years of projection.

        Optional parameters:
            salaries_new_emp (function) : A function accepting as parameter a DataFrame containing all 
                                          columns data for new employees plus a column 'entrance' (the year this new 
                                          employee entered  the population) and returning a DataFrame containing 
                                          projected salaries for each new employee.

        sal_evol (numeric) : annual increase of the salaire. Salary at year i+1 = (Salary at year i)*(1+sal_evol)
        
        Returns: 
            DataFrame: A DataFrame containing projected salaries for each employee
    """

    # Getting new employees
    df_new = eff.new_employees(numbers_[0], MAX_YEARS)

    # if salaries_new_emp is not None, get salaries of new employees and add them to salaries
    if not salaries_new_emp is None:
        salaries_new_emp_df = salaries_new_emp_1(df_new )
        salaries = pd.concat([salaries,salaries_new_emp_df] )

    print(salaries)

    # Getting individual projected numbers for employees
    lives, deaths, resignation, type_ = eff.individual_employees_numbers(employees_proj_)

    # Join lives and salaries
    df_temp = lives.join(salaries.set_index('id'),on='id', how='inner', lsuffix='_lives', rsuffix='_salaries')

    # Get years columns
    years_columns = [c  for c in df_temp.columns if c.startswith('year_')]

    type_ = type_.set_index('id')

    # Get the number of rows
    n = len(df_temp)

    # Project salary
    for i in range(n):
        for c in years_columns:
            # year
            y = int(c[5:])
            # id 
            id_ = df_temp.loc[i,'id']
            # salaries are not zero for actives only
            if type_.loc[id_, c] == 'active':
                df_temp.loc[i, c] = df_temp.loc[i, c] * df_temp.loc[i, 'salary']*((1+sal_evol)**y)
            else:
                df_temp.loc[i, c] = 0



    return df_temp[df_temp.columns[:-1]]


df = project_salaries(numbers_[0],salaries, MAX_ANNEES, salaries_new_emp_1, 0.035)
# print(df)

df.to_csv('asupprimer.csv', sep=';', index=False, decimal=',')




# coding: utf-8

# # Projecting salaries using projected individual numbers
# # #####################################################

# Import necessary packages
from pop_projection import Effectifs as eff
from pop_projection import Cashflows as cf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import inspect
import time
from datetime import datetime


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
    n = len(ids)
    # i = 0
    entry_salaries = {1:50000, 2:50000, 3: 73000, 4:103000, 5:165000, 6:165000,
            7: 310000, 8:327000, 9:385000, 10:395000, 11:560000}

    for i in range(n):
        strate = new_employees.loc[i, 'strate']
        if strate > 11:
            strate = strate - 11
        salaries[i] = entry_salaries[strate] * (1 + 0.02) ** new_employees.loc[i, 'entrance']

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
                              '5': [28, 28, 0.5, ], '6': [28, 28, 0.5], '7': [33, 33, 0.5], '8': [38, 38, 0.5], 
                              '9': [38, 38, 0.5], '10': [47, 47, 0.5], '11': [49, 49, 0.5]}

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
                        'data': ['active', 'male', 'not married', nouveaux(g)[0], 
                                '31/12/' + str((2018 + year_ - nouveaux(g)[0])), 
                                '01/01/' + str((2018 + year_ + 1)), 0, g, g, 0]}
                new_employees.append(temp)

            # add a female
            if nouveaux(g)[2] < 1:
                temp = {'key': 'male_groupe_' + str(g) + '_year_' + str(year_),
                        'number': nouveaux(g)[2] * departures_[g] * taux_rempl(year_, g),
                        'data': ['active', 'male', 'not married', nouveaux(g)[0], 
                                '31/12/' + str((2018 + year_ - nouveaux(g)[0])), 
                                '01/01/' + str((2018 + year_ + 1)), 0, g, g, 0]}
                new_employees.append(temp)

    return new_employees



# Define law of retirement
def law_ret1(age, Date_Engagement, DateNaissance, year_proj):

    date_naiss = datetime.strptime(DateNaissance, '%d/%m/%Y')
    date_eng = datetime.strptime(Date_Engagement, '%d/%m/%Y')

    # Mois de naissance
    mois_naiss = date_naiss.month

    # jour de naissance
    jour_naiss = date_naiss.day

    # Date de départ théorique
    if date_eng.year < 2002:
        # gestion des années bissextile
        if jour_naiss == 29 and mois_naiss == 2:
            temp = '01/03/' + str(date_naiss.year + 55)
        else:
            temp = str(jour_naiss) + '/' + str(mois_naiss) + '/' + str(date_naiss.year + 55)
    else:
        temp = str(jour_naiss) + '/' + str(mois_naiss) + '/' + str(date_naiss.year + 60)

    date_dep = datetime.strptime(temp, '%d/%m/%Y')

    annee_proj = 2018 + year_proj

    if date_dep.year < annee_proj:
        return True
    
    if date_dep.year > annee_proj:
        return False
    
    if date_dep.year == annee_proj:
        if (mois_naiss < 7) or (mois_naiss == 7 and jour_naiss == 1) :
                return True
        else:
            return False


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
MAX_ANNEES = 60

# Projection
numbers_ = eff.simulerEffectif( employees, spouses, children, 'TV 88-90', MAX_ANNEES, 
                                law_replacement_=law_replacement1, law_retirement_= law_ret1)

print('Simulation effectifs : ', time.asctime( time.localtime(time.time())))

df_salaries = cf.project_salaries(numbers_[0], salaries, MAX_ANNEES, salaries_new_emp_1, 0.035)

print('Projection salaires : ', time.asctime( time.localtime(time.time())))

# rate_contr = pd.read_csv(path + "rate_contr.csv", sep=";", decimal=",")

def rate_contr(sex, year):
    return 0.325

df_contr = cf.project_contributions(df_salaries,rate_contr,20)

print('Projection contributions : ', time.asctime( time.localtime(time.time())))

def f_pension_th(data, salaries , types_):
    if 'retired' in types_:
        year_retirement = types_.index('retired')
    else:
        return 0

    if 'active' in types_:
        year_entrance = types_.index('active')
    else:
        year_entrance = 0


    # salaire final moyen
    if year_retirement > 2 :
        sal_moyen = (salaries[year_retirement-3]+salaries[year_retirement-2]+
                     salaries[year_retirement-1])/3
    if year_retirement == 2:
        sal_moyen = (salaries[year_retirement-2]/(1+0.035)+salaries[year_retirement-2]+
                     salaries[year_retirement-1])/3

    if year_retirement == 1:
        sal_moyen = (salaries[year_retirement-1]/(1+0.035)**2+salaries[year_retirement-1]/(1+0.035)+
                     salaries[year_retirement-1])/3

    # pension théorique
    pth = (sal_moyen*(data['anciennete']+year_retirement-year_entrance))*0.025

    
    return pth


def f_pension_min(data, salaries , types_):
    if 'retired' in types_:
        year_retirement = types_.index('retired')
    else:
        return 0

    if 'active' in types_:
        year_entrance = types_.index('active')
    else:
        year_entrance = 0

    # pension théorique
    pth = f_pension_th(data, salaries, types_)

    # Si agent recruté après 2002 la pension minimale est la pension théorique
    # date engagement
    date_eng = datetime.strptime(data['Date_Engagement'], '%d/%m/%Y')
    if date_eng.year >= 2002:
        return pth

    # pension catégorielle par strate
    pension_cat = {1:18000, 2:18000, 3:24000, 4:24000, 5:30000, 
                6:30000, 7:36000, 8:36000, 9:36000, 10:36000, 11: 36000}

    # calcul de la pension minimale
    # strate 
    strate = data['strate']
    if date_eng.year < 1995:
        return min(pension_cat[strate], pth/2)
    else:
        return max(pension_cat[strate], pth/2)



def f_capital(data, salaries , types_):
    if not 'retired' in types_:
        return 0

    # Si agent recruté après 2002 pas de capital
    # date engagement
    date_eng = datetime.strptime(data['Date_Engagement'], '%d/%m/%Y')
    if date_eng.year >= 2002:
        return 0

    # pension théorique
    pth = f_pension_th(data, salaries, types_)
    
    # pension catégorielle par strate
    pension_cat = {1:18000, 2:18000, 3:24000, 4:24000, 5:30000, 
                6:30000, 7:36000, 8:36000, 9:36000, 10:36000, 11: 36000}

    # calcul de la pension minimale
    # strate 
    strate = data['strate']

    # projection du SIR
    SIR_p = data['SIR']
    for s in salaries[1:]:
        SIR_p = SIR_p + s*0.13

    if date_eng.year < 1995:
        pension_min = min(pension_cat[strate], pth/2)
    else:
        pension_min = max(pension_cat[strate], pth/2)

    capital = 10*(pth- pension_min) + SIR_p*(pth-pension_min)/pth

    return capital


df_pensions = cf.project_pensions(numbers_[0], df_salaries, pensions, f_pension_min,MAX_ANNEES,0.0275)

df_pensions_th = cf.project_pensions(numbers_[0], df_salaries, pensions, f_pension_th,MAX_ANNEES,0.0275)

df_capitaux = cf.project_pensions(numbers_[0], df_salaries, pensions, f_capital,MAX_ANNEES,-1)

print('Projection pensions : ', time.asctime( time.localtime(time.time())))

df_salaries.to_csv('./results/projected_salaries.csv', sep=';', index=False, decimal=',')
df_contr.to_csv('./results/projected_contributions.csv', sep=';', index=False, decimal=',')
df_pensions.to_csv('./results/projected_penions.csv', sep=';', index=False, decimal=',')

df_pensions_th.to_csv('./results/projected_penions_th.csv', sep=';', index=False, decimal=',')

df_capitaux.to_csv('./results/projected_capitaux.csv', sep=';', index=False, decimal=',')

print('Fin : ', time.asctime( time.localtime(time.time())))

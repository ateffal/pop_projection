
"""
Created on Mon May  7 14:08:56 2018

@author: a.teffal
"""
#%%

import random
import pandas as pd
import Actuariat as act



#%%
def turnover(age) :
    """
    Return the probability of quitting during the following year at a given age

    """
    if age<30:
        return 0.02
    else:
        if age <45:
            return 0.01
        else:
            return 0

#%%
def probaMariage(age, typeAgent):
    """
    Return the probability of getting maried  during the following year at a given age

    """
    if typeAgent=='Actif':
        if age >= 35 and age <= 54:
            return 0.03
        else :
            return 0
    else:
        return 0



#%%

def is_alive(Age, Table):
    if Age > 120:
        return 0

    if Table[Age]!=0:
        p = Table[Age+1]/Table[Age]
    else:
        p = 0

    if random.random() <= p:
        return 1
    else:
        return 0

#%%
def is_present(Age):
    if random.random() < turnover(Age):
        return 0
    else:
        return 1

#%%
def willMarry(Age, typeAgent):
    if random.random() < probaMariage(Age, typeAgent):
        return 1
    else:
        return 0

#%%

def simulerEffectif(employees, spouses, children, mortalityTable, MAX_YEARS = 50):
    
    ''' assumes employees, spouses and children are pandas dataframes with at least 5 columns :
        - id   : an unique identifier of the employee
        - type : active or retired for employees. active, or retired or widow or widower for spouses and children.
                 for spouses and children, type is the type of the employee taht they are attached to if it's still alive, or widows or widower otherwise
        - sex
        - familyStatus : maried, or not maried
        - age
    '''
    
    # Numbers of each category of population
    n_e = len(employees) 
    n_s = len(spouses)
    n_c = len(children)
    
    # dics where to store survivals : ex : {id:[list of lives, one for each year]}
    employees_lives = {}
    spouses_lives = {}
    children_lives = {}
    
    # dics where to store deaths : ex : {id:[list of lives, one for each year]}
    employees_deaths = {}
    spouses_deaths = {}
    children_deaths = {}
    
    # dic where to store demmissions (actives only) : ex : {id:[list of lives, one for each year]}
    employees_dem = {}
    
    # initialisation of dics
    for i in range(n_e):
        employees_lives[employees["id"][i]] = [1] + [0]*(MAX_YEARS-1)
        
    for i in range(n_s):
        spouses_lives[spouses["id"][i]] = [1] + [0]*(MAX_YEARS-1)
        
    for i in range(n_c):
        children_lives[children["id"][i]] = [1] + [0]*(MAX_YEARS-1)
        
    for i in range(n_e):
        employees_deaths[employees["id"][i]] = [0]*MAX_YEARS
        
    for i in range(n_s):
        spouses_deaths[spouses["id"][i]] = [0]*MAX_YEARS
        
    for i in range(n_c):
        children_deaths[children["id"][i]] = [0]*MAX_YEARS
        
    for i in range(n_e):
        employees_dem[employees["id"][i]] = [0]*MAX_YEARS
        
    
    # main loop
    for i in range(1, MAX_YEARS):
        # employees
        for j in range(n_e):
            # calculate age
            age = employees["age"][j] + i
            survie = act.sfs_nPx(age,1, mortalityTable)
            employees_lives[employees["id"][j]][i] = employees_lives[employees["id"][j]][i-1] * survie
    
    return  employees_lives
    
    
    

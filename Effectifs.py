
"""
Created on Mon May  7 14:08:56 2018

@author: a.teffal
"""
#%%

import random
# import numpy as np
import pandas as pd



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

def simulerEffectif(actives, retirees, widows, conjointsActives, conjointsRetirees, childrenActives, childrenRetirees, orphans, mortalityTable, MAX_YEARS = 50):
    
    ''' assumes actives, retirees, widows, conjointsActives, conjointsRetirees, childrenActives, childrenRetirees, 
        and orphans are pandas dataframes with 2 columns, the first column is the id and the second one is the age.
        conjointsActives and conjointsRetirees have the same id as their conjoints (the active or the retiree). 
        childrenActives, childrenRetirees and orphans have the same id as their father (the active or the retiree). 
    '''
    
    # Numbers of each category of population
    n_a = len(actives) 
    n_r = len(retirees)
    n_w = len(widows)
    n_ca = len(conjointsActives) 
    n_cr = len(conjointsRetirees)
    n_cha = len(childrenActives)
    n_chr = len(childrenRetirees)
    n_o = len(orphans)
    

    

    # dics where to store survivals : ex : {id:[list of lives, one for each year]}
    actives_lives = {}
    retirees_lives = {}
    widows_lives = {}
    conjointsActives_lives = {}
    conjointsRetirees_lives = {}
    childrenActives_lives = {}
    childrenRetirees_lives = {}
    orphans_lives = {}
    
    # dics where to store deaths : ex : {id:[list of lives, one for each year]}
    actives_deaths = {}
    retirees_deaths = {}
    widows_deaths = {}
    conjointsActives_deaths = {}
    conjointsRetirees_deaths = {}
    childrenActives_deaths = {}
    childrenRetirees_deaths = {}
    orphans_deaths = {}
    
    # dic where to store demmissions (actives only) : ex : {id:[list of lives, one for each year]}
    actives_dem = {}
    
    # initialisation of dics
    # lives
    for i in range(n_a):
        actives_lives[actives["id"][i]] = [1] + [0]*(MAX_YEARS-1)
    for i in range(n_r):
        retirees_lives[retirees["id"][i]] = [1] + [0]*(MAX_YEARS-1)
    for i in range(n_w):
        widows_lives[widows["id"][i]] = [1] + [0]*(MAX_YEARS-1)
    for i in range(n_ca):
        conjointsActives_lives[conjointsActives["id"][i]] = [1] + [0]*(MAX_YEARS-1)
    for i in range(n_cr):
        conjointsRetirees_lives[conjointsRetirees["id"][i]] = [1] + [0]*(MAX_YEARS-1)
    for i in range(n_cha):
        childrenActives_lives[childrenActives["id"][i]] = [1] + [0]*(MAX_YEARS-1)
    for i in range(n_chr):
        childrenRetirees_lives[childrenRetirees["id"][i]] = [1] + [0]*(MAX_YEARS-1)
    for i in range(n_o):
        orphans_lives[orphans["id"][i]] = [1] + [0]*(MAX_YEARS-1)
    # deaths
    for i in range(n_a):
        actives_deaths[actives["id"][i]] = [0]*MAX_YEARS
    for i in range(n_r):
        retirees_deaths[retirees["id"][i]] = [0]*MAX_YEARS
    for i in range(n_w):
        widows_deaths[widows["id"][i]] = [0]*MAX_YEARS
    for i in range(n_ca):
        conjointsActives_deaths[conjointsActives["id"][i]] = [0]*MAX_YEARS
    for i in range(n_cr):
        conjointsRetirees_deaths[conjointsRetirees["id"][i]] = [0]*MAX_YEARS
    for i in range(n_cha):
        childrenActives_deaths[childrenActives["id"][i]] = [0]*MAX_YEARS
    for i in range(n_chr):
        childrenRetirees_deaths[childrenRetirees["id"][i]] = [0]*MAX_YEARS
    for i in range(n_o):
        orphans_deaths[orphans["id"][i]] = [0]*MAX_YEARS
    # demissions
    for i in range(n_a):
        actives_dem[actives["id"][i]] = [0]*MAX_YEARS
    
    
    
    
    for i in range(1,MAX_ANNEES):
        for j in range(n_a):
            print("to do for year ", i, " active ", j)
        
            
        




#%%








































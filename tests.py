# -*- coding: utf-8 -*-
"""
Created on Mon Sep  3 08:19:47 2018

@author: a.teffal
"""

import Effectifs as eff
import pandas as pd
import time
import Actuariat as act


#%%

def law_ret1(age, year_emp):
    if year_emp < 2002:
        if age >= 55:
            return True
        else:
            return False
    if year_emp >= 2002:
        if age >= 60:
            return True
        else:
            return False
        
        
def law_ret2(age):
    if age >= 55:
        return True
    else:
        return False
    

def law_ret3(age, sexe):
    if sexe == 'female':
        if age >= 55:
            return True
        else:
            return False
    if sexe == 'male':
        if age >= 60:
            return True
        else:
            return False 

    
    
    
    
################################################# Code pour les tests ############################################
path ="D:\\Shared\\a.teffal\\Application_Simulation_FS\\Application_Python\\"
t1 = time.time()

# nombre maximum d'années de projection
MAX_ANNEES = 50

# chargement des données
employees = pd.read_csv(path + "employees.csv",sep=";", decimal = ",")
spouses = pd.read_csv(path + "spouses.csv",sep=";", decimal = ",")
children = pd.read_csv(path + "children.csv",sep=";", decimal = ",")

print("employees : ", len(employees))
print(employees.head(5))
print("spouses : ", len(spouses))
print(spouses.head(5))
print("children : ", len(children))
print(children.head(5))


numbers_ = eff.simulerEffectif(employees, spouses, spouses, 'TV 88-90', MAX_ANNEES, (law_ret3, ['age', 'sexe']))


# number of actives per year
effectif_actifs = [0]*MAX_ANNEES
effectif_retraites = [0]*MAX_ANNEES
effectif_demissions = [0]*MAX_ANNEES
effectif_deces_actifs = [0]*MAX_ANNEES
effectif_deces_retraites = [0]*MAX_ANNEES

for i in range(MAX_ANNEES):
    for a in numbers_[0].values():
        if a['type'][i] == 'active':
            effectif_actifs[i] = effectif_actifs[i] + a['lives'][i]
            effectif_deces_actifs[i] = effectif_deces_actifs[i] + a['deaths'][i]
        else:
            effectif_retraites[i] = effectif_retraites[i] + a['lives'][i]
            effectif_deces_retraites[i] = effectif_deces_retraites[i] + a['deaths'][i]
            
        
        effectif_demissions[i] = effectif_demissions[i] + a['res'][i]
        

print("Effectifs des actifs : ")
print(effectif_actifs)
print("---------------------------------------------------------------")
print("Effectifs des retraites : ",effectif_retraites)
print("---------------------------------------------------------------")
print("Effectifs des démissions : ",effectif_demissions)
print("---------------------------------------------------------------")
print("Effectifs des décès des actifs : ",effectif_deces_actifs)
print("---------------------------------------------------------------")
print("Effectifs des décès des retraités : ",effectif_deces_retraites)

# for z in numbers_[3]:
#     print("Year : ",z)
#     print(len(numbers_[3][z]))
    
print([len(numbers_[3][z]) for z in numbers_[3]])
t2 = time.time()
print('Durée de calcul (minutes) : ', (t2-t1)/60)


#%%





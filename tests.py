# -*- coding: utf-8 -*-
"""
Created on Mon Sep  3 08:19:47 2018

@author: a.teffal
"""

import Effectifs as eff
import pandas as pd
import time
import Actuariat as act
from sqlalchemy.sql.expression import false




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



def law_resignation_1(age, sexe):
    if age >= 50 :
        return 0
    if sexe == 'female':
        if age <= 30:
            return 0.02
        else:
            return 0.01
    if sexe == 'male':
        if age <= 30:
            return 0.02
        else:
            return 0.01
    
    
    
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


numbers_ = eff.simulerEffectif(employees, spouses, children, 'TV 88-90', MAX_ANNEES, (law_ret1, ['age', 'Year_employment']), (law_resignation_1, ['age', 'sex']))

# number of actives per year
effectif_actifs = [0]*MAX_ANNEES
effectif_conjoints_actifs = [0]*MAX_ANNEES

# number of retired per year
effectif_retraites = [0]*MAX_ANNEES
effectif_conjoints_retraites = [0]*MAX_ANNEES

# number of quitters per year
effectif_demissions = [0]*MAX_ANNEES

#number of dying actives
effectif_deces_actifs = [0]*MAX_ANNEES
effectif_deces_conjoints_actifs = [0]*MAX_ANNEES

#number of dying retired
effectif_deces_retraites = [0]*MAX_ANNEES
effectif_deces_conjoints_retraites = [0]*MAX_ANNEES

#number of living widows
effectif_ayants_cause = [0]*MAX_ANNEES

for i in range(MAX_ANNEES):
    for a in numbers_[0].values():
        if a['type'][i] == 'active':
            effectif_actifs[i] = effectif_actifs[i] + a['lives'][i]
            effectif_deces_actifs[i] = effectif_deces_actifs[i] + a['deaths'][i]
        else:
            effectif_retraites[i] = effectif_retraites[i] + a['lives'][i]
            effectif_deces_retraites[i] = effectif_deces_retraites[i] + a['deaths'][i]
            
        
        effectif_demissions[i] = effectif_demissions[i] + a['res'][i]
        
    
    for a in numbers_[1].values():
        if a['type'][i] == 'active':
            effectif_conjoints_actifs[i] = effectif_conjoints_actifs[i] + a['lives'][i]
            effectif_deces_conjoints_actifs[i] = effectif_deces_conjoints_actifs[i] + a['deaths'][i]
            
        if a['type'][i] == 'retired':
            effectif_conjoints_retraites[i] = effectif_conjoints_retraites[i] + a['lives'][i]
            effectif_deces_conjoints_retraites[i] = effectif_deces_conjoints_retraites[i] + a['deaths'][i]
            
        if a['type'][i] == 'widow':
            effectif_ayants_cause[i] = effectif_ayants_cause[i] + a['lives'][i]
            
            
#construct DataFrame of projected numbers
totalEmployees = [sum(x) for x in zip(effectif_actifs, effectif_retraites)]
totalSpouses = [sum(x) for x in zip(effectif_conjoints_actifs, effectif_conjoints_retraites)]

Data = {'Year':list(range(MAX_ANNEES)),'effectif_actifs' : effectif_actifs, 'effectif_retraites' : effectif_retraites, 'Total Employees' : totalEmployees,
        'effectif_ayants_cause' : effectif_ayants_cause, 'effectif_conjoints_actifs' : effectif_conjoints_actifs,
        'effectif_conjoints_retraites' : effectif_conjoints_retraites, 'Total Spouses' : totalSpouses}

Effectifs = pd.DataFrame(data=Data, 
            columns=['Year', 'effectif_actifs', 'effectif_retraites', 'Total Employees' , 'effectif_ayants_cause', 
                     'effectif_conjoints_actifs', 'effectif_conjoints_retraites', 'Total Spouses' ])


print(Effectifs.head(10))

Effectifs.to_csv('Effectifs_python.csv', sep = ';', index=False, decimal=',')



#construct DataFrame of projected numbers living the pop : deaths, resignations
totalLiving = [sum(x) for x in zip(effectif_deces_actifs, effectif_demissions, effectif_deces_retraites,effectif_deces_conjoints_actifs, effectif_deces_conjoints_retraites )]


Data = {'Year':list(range(MAX_ANNEES)),'effectif_deces_actifs' : effectif_deces_actifs, 'effectif_demissions' : effectif_demissions, 
        'effectif_deces_retraites' : effectif_deces_retraites, 'effectif_deces_conjoints_actifs' : effectif_deces_conjoints_actifs, 
        'effectif_deces_conjoints_retraites' : effectif_deces_conjoints_retraites, 'Total Living' : totalLiving}

Living = pd.DataFrame(data=Data, 
            columns=['Year', 'effectif_deces_actifs', 'effectif_demissions', 'effectif_deces_retraites' , 'effectif_deces_conjoints_actifs', 
                     'effectif_deces_conjoints_retraites', 'Total Living'])


print(Living.head(10))

Living.to_csv('Sortants_python.csv', sep = ';', index=False, decimal=',')


#export projected employees
pd.DataFrame.from_dict(numbers_[0]).to_csv('employees_proj.csv', sep = ';', index=False, decimal=',')

#export projected spouses
pd.DataFrame.from_dict(numbers_[1]).to_csv('spouses_proj.csv', sep = ';', index=False, decimal=',')





t2 = time.time()
print("Début :", time.strftime("%a, %d %b %Y %H:%M:%S", time.gmtime(t1)))
print("Fin :", time.strftime("%a, %d %b %Y %H:%M:%S", time.gmtime(t2)))
print('Durée de calcul (minutes) : ', (t2-t1)/60)


#%%





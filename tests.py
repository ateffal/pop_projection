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
################################################# Code pour les tests ############################################


t1 = time.time()


# nombre maximum d'années de projection
MAX_ANNEES = 50



# chargement des données
employees = pd.read_csv("employees.csv",sep=";", decimal = ",")
spouses = pd.read_csv("conjoints.csv",sep=";", decimal = ",")

test = eff.simulerEffectif(employees, spouses, spouses, 'TV 88-90', 100)

for t in test :
    print(test[t])

t2 = time.time()
print('Durée de calcul (minutes) : ', (t2-t1)/60)


#%%



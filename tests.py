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

# nombre maximum d'années de projection
MAX_ANNEES = 50

# chargement des données
agents_0=pd.read_csv("Adherents_0.csv",sep=";",decimal=',')
conjoints_0=pd.read_csv("conjoints.csv",sep=";",decimal=',')
enfants_0=pd.read_csv("enfants.csv",sep=";",decimal=',')

#mise en forme des dates
agents_0["DateEngagement"] = pd.to_datetime(agents_0["DateEngagement"],format='%d/%m/%Y')


#importation du type et des ages de depart
ages_depart = {}
with open('AgeDepart.csv') as f:
    for line in f:
        (key, val) = line.split(sep=';')
        if not val == '':
            ages_depart[key] = int(val.strip())


#%%

t1 = time.time()

survie_agents, survie_conjoints, deces_agents, dem_agents, deces_conjoints  = eff.simulerEffectif(agents_0, conjoints_0, enfants_0, act.TV_88_90,1000,MAX_ANNEES)
t2 = time.time()

print('Durée de calcul (minutes) : ', (t2-t1)/60)


#%%


effectifs_actifs =[0]*MAX_ANNEES
effectifs_retraites =[0]*MAX_ANNEES
effectifs_nouveaux_retraites = [0]*MAX_ANNEES
deces_actifs =  [0]*MAX_ANNEES
dem_actifs =  [0]*MAX_ANNEES

#Annee 0
for a in survie_agents:
    if (agents_0[agents_0['Identifiant']==a]['Type'].any() == 'Actif'):
        effectifs_actifs[0] +=1
    else:
        effectifs_retraites[0] +=1


for a in survie_agents:
    age_actuel = int(agents_0[agents_0['Identifiant']==a]['Age']) +1 # car Age correspond a annee = 0
    age_depart = ages_depart[a]
    for i in range(1,MAX_ANNEES): # on commence a partir de annee 1
        if age_actuel < age_depart:
            effectifs_actifs[i] += survie_agents[a][i]
            deces_actifs[i] += deces_agents[a][i]
            dem_actifs[i] += dem_agents[a][i]
        else:
            effectifs_retraites[i] += survie_agents[a][i]
            if age_actuel == age_depart:
                effectifs_nouveaux_retraites[i] += survie_agents[a][i]
        age_actuel += 1

print('Effectifs des actifs : ')
print(effectifs_actifs)

print('Effectifs des retraites : ')
print(effectifs_retraites)


print('Effectifs des nouveaux retraites : ')
print(effectifs_nouveaux_retraites)



########################################################################################
effectifs_conjoints =[0]*MAX_ANNEES

for a in survie_conjoints:
    effectifs_conjoints = [i + j for i, j in zip(effectifs_conjoints, survie_conjoints[a])]

print(effectifs_conjoints)

###########################################################################################

effectifs_conjoints_deces =[0]*MAX_ANNEES

for a in deces_conjoints:
    effectifs_conjoints_deces = [i + j for i, j in zip(effectifs_conjoints_deces, deces_conjoints[a])]

print(effectifs_conjoints_deces)

#############################################################################################

#%%

effectifs_conjoints_nouveaux =[0]*MAX_ANNEES

for a in survie_conjoints:
    if a[1] >=101 :
        effectifs_conjoints_nouveaux = [i + j for i, j in zip(effectifs_conjoints_nouveaux, survie_conjoints[a])]

print(effectifs_conjoints_nouveaux)




#%%

# export survie_conjoints to csv file
(pd.DataFrame.from_dict(data=survie_conjoints, orient='index').to_csv('survie_conjoints.csv', header=False))






#%%




































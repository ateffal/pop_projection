# -*- coding: utf-8 -*-
"""
Created on Mon May  7 14:08:56 2018

@author: a.teffal
"""
#%%
import pandas as pd
import numpy as np
import Actuariat as act
import random
import time


#%%

MAX_ANNEES = 60

agents_0=pd.read_csv("Actifs_0.csv",sep=";",decimal=',')

def is_alive_old(Age, Table):
    p = act.sfs_nPx(Age, 1, Table)
    if random.random() <= p:
        return 1
    else:
        return 0
    
#%%


def is_alive(Age, Table):
    
    if Table[Age]!=0:
        p = Table[Age+1]/Table[Age]
    else:
        p = 0

    if random.random() <= p:
        return 1
    else:
        return 0
       
#%%

def simulerEffectif_old(Agents):
    n = len(Agents)
    survie = np.zeros((n,MAX_ANNEES),dtype=int)
    deces_annuels = np.zeros(MAX_ANNEES,dtype=int)
    
    #L'année 0 les agents sont évidemment vivants
    for i in range(n):
        survie[i,0] = 1
    
    for j in range(1,MAX_ANNEES):
        for i in range(n):
            if survie[i, j-1] == 1 :
                survie[i, j] = is_alive(Agents['Age'][i] + j, 'TD 73-77')
                deces_annuels[j] = deces_annuels[j] + (1-survie[i, j])
            else:
                survie[i, j] = 0
    return np.sum(survie,axis=0), deces_annuels


#%%
def simulerEffectif(Agents, Table, n_simulation):
    n = len(Agents)
#    survie = np.zeros((n,MAX_ANNEES),dtype=int)
#    deces_annuels = np.zeros(MAX_ANNEES,dtype=int)
    
    survie_total = np.zeros((n,MAX_ANNEES),dtype=int)
    survie_total_N_1 = np.zeros(n, dtype=int)
    deces_annuels_total = np.zeros(MAX_ANNEES,dtype=int)
    
#    survie_annuels = np.zeros(MAX_ANNEES,dtype=int)
    
    #L'année 0 les agents sont évidemment vivants
    
        
    for k in range(n_simulation):
        for j in range(0,MAX_ANNEES):
            for i in range(n):
                if j==0:
                    survie_total[i,j] = survie_total[i,j] + 1
                    survie_total_N_1[i] = 1
                else:
                    if survie_total_N_1[i] == 1 :
                        temp = is_alive(Agents[i] + j, Table)
                        survie_total[i,j] = survie_total[i,j] + temp
                        deces_annuels_total[j] = deces_annuels_total[j] + (1-temp)
                        survie_total_N_1[i] = temp
        
    return survie_total/n_simulation, deces_annuels_total/n_simulation


        
#%%

t1 = time.time()

survie = np.zeros((MAX_ANNEES),dtype=float)

deces_annuels = np.zeros(MAX_ANNEES,dtype=float)

x = np.array(agents_0['Age'])

n_sim = 1000

for s in range(n_sim):
    temp1, temp2 = simulerEffectif(x, act.TD_73_77)
    survie = survie + temp1
    deces_annuels = deces_annuels + temp2
    
survie = survie/n_sim

deces_annuels = deces_annuels/n_sim

t2 = time.time()

print('Durée de calcul (minutes) : ', (t2-t1)/60)

#%%

t1 = time.time()
survie = np.zeros((MAX_ANNEES),dtype=float)
deces_annuels = np.zeros(MAX_ANNEES,dtype=float)
x = np.array(agents_0['Age'])
survie, deces_annuels = simulerEffectif(x, act.TV_88_90,1000)
t2 = time.time()

print('Durée de calcul (minutes) : ', (t2-t1)/60)


#%%
















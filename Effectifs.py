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

class Personne:
    def __init__(self, identifiant, age, sexe):
        self.identifiant = identifiant
        self.Age = age
        self.Sexe = sexe
        self.Vivant = 1
        
    def getAge(self):
        return self.Age
    
    def getSexe(self):
        return self.Sexe
    
    def getIdentifiant(self):
        return self.identifiant
    
    def getVivant(self):
        return self.Vivant
    
    def decede(self):
        self.Vivant = 0
    
    
    def setVivant(self):
        self.Vivant = 1
        
    def projeter_old(self, table, n = 1):
        if self.Vivant == 1:
            vivant = is_alive(self.getAge() + n , table)
            temp = Personne(self.identifiant, self.Age + n, self.Sexe)
            
            if vivant == 0:
                temp.decede()    
            
            return temp
        else:
            temp = Personne(self.identifiant, self.Age + n, self.Sexe)
            temp.decede()
            return temp
        
    def projeter(self, table, n = 1):
        
        if self.Vivant == 1:
            survie = is_alive(self.getAge() + n , table)
            if survie == 0:
                self.decede() 
        else:
            survie = 0
        
        return survie
            
        
            
        
        
    
#%%

class Conjoint(Personne):
    def __init__(self, identifiant, rang, age, sexe):
        Personne.__init__(self, identifiant, age, sexe)
        self.Rang = rang
        
    def getRang(self):
        return self.Rang
    
    def getIdentifiant(self):
        return (self.Identifiant, self.Rang)

#%%
        
class Enfant:
    def __init__(self, identifiant, rang, age, sexe):
        Personne.__init__(self, identifiant, age, sexe)
        self.Rang = rang
    
    def getRang(self):
        return self.Rang
    
    def getIdentifiant(self):
        return (self.Identifiant, self.Rang)
        

#%%

class Agent(Personne):
    
    def __init__(self,identifiant,age, sexe):
        Personne.__init__(self, identifiant, age, sexe)
        self.Conjoints = []
        self.Enfants = []
        self.maxRangConjoint = 0
        self.maxRangEnfant = 0
        
    def ajouterConjoint(self, age, sexe, rang = None):
        self.maxRangConjoint += 1
        if rang == None:
            self.Conjoints.append(Conjoint(self.identifiant,self.maxRangConjoint, age, sexe))
        else:
            self.Conjoints.append(Conjoint(self.identifiant,rang, age, sexe))
        
    def ajouterEnfant(self, age, sexe, rang = None):
        self.maxRangEnfant += 1
        if rang == None:
            self.Enfants.append(Enfant(self.identifiant,self.maxRangEnfant, age, sexe))
        else:
            self.Enfants.append(Enfant(self.identifiant,rang, age, sexe))
        
    def setVivantConjoints(self):
        for conj in self.Conjoints:
            conj.setVivant()
    

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
def simulerEffectif_old(Adherents, Conjoints, Enfants, Table, n_simulation, MAX_ANNEES = 50):
    
    # Nombre d'adhérents, de conjoints et d'enfants
    n_a = len(Adherents)
    n_c = len(Conjoints)
    n_e = len(Enfants)
    
    # Constructuion des Agents à partir des data frame Adherents, Conjoints et Enfants
    Agents =[]
    
    # dic stockant les indices des agents pour pouvoir les retrouver facilement
    indices_agents = {}
    
    # Chargements des agents (avec zero conjoints et zeros enfants)
    for i in range(n_a):
        agent = Agent(Adherents['Identifiant'][i], Adherents['Age'][i], Adherents['Sexe'][i])
        indices_agents[Adherents['Identifiant'][i]] = i
        Agents.append(agent)
        
    #Ajout des conjoints
    for i in range(n_c):
        #conjoint = Conjoint(Conjoints['Identifiant'][i], Conjoints['Rang'][i], Conjoints['Age'][i], Conjoints['Sexe'][i])
        #indice de agent correspondant dans Agents
        if Conjoints['Identifiant'][i] in indices_agents:
            indice_a = indices_agents[Conjoints['Identifiant'][i]]
            Agents[indice_a].ajouterConjoint(Conjoints['Age'][i], Conjoints['Sexe'][i], Conjoints['Rang'][i])
        
    #Ajout des enfants
    for i in range(n_e):
        #indice de agent correspondant dans Agents
        if Enfants['Identifiant'][i] in indices_agents:
            indice_a = indices_agents[Enfants['Identifiant'][i]]
            Agents[indice_a].ajouterEnfant(Enfants['Age'][i], Enfants['Sexe'][i], Enfants['Rang'][i] )
        
        
    # tableaux pour stocker les survies
    survie_adherents_total = np.zeros((n_a,MAX_ANNEES),dtype=int)
    #survie_conjoints_total = np.zeros((n_c,MAX_ANNEES),dtype=int)
    #survie_enfants_total = np.zeros((n_c,MAX_ANNEES),dtype=int)
    
    
    
    
    for k in range(n_simulation):
        
        #initialisation des tableaux de survie
        survie_adherents = np.zeros((n_a,MAX_ANNEES),dtype=int)
        survie_conjoints = np.zeros((n_c,MAX_ANNEES),dtype=int)
        survie_enfants = np.zeros((n_c,MAX_ANNEES),dtype=int)
    
        for j in range(0,MAX_ANNEES):
            for i in range(n_a):
                if j==0:
                    survie_adherents[i,j] = 1
                    survie_conjoints[i,j] = 1
                    survie_enfants[i,j] = 1
                    survie_adherents_total[i, j] += 1
                else:
                    if survie_adherents[i, j-1] == 1 :
                        temp = is_alive(Agents[i].getAge() + j, Table)
                        survie_adherents[i, j] = temp
                        survie_adherents_total[i, j] += temp
        
    return survie_adherents_total/n_simulation


        
#%%

def simulerEffectif(Adherents, Conjoints, Enfants, Table, n_simulation, MAX_ANNEES = 50):
    
    # Nombre d'adhérents, de conjoints et d'enfants
    n_a = len(Adherents)
    n_c = len(Conjoints)
    n_e = len(Enfants)
    
    # Constructuion des Agents à partir des data frame Adherents, Conjoints et Enfants
    Agents =[]
    
    # dic stockant les indices des agents pour pouvoir les retrouver facilement
    indices_agents = {}
    
    # Chargements des agents (avec zero conjoints et zeros enfants)
    for i in range(n_a):
        agent = Agent(Adherents['Identifiant'][i], Adherents['Age'][i], Adherents['Sexe'][i])
        indices_agents[Adherents['Identifiant'][i]] = i
        Agents.append(agent)
        
    #Ajout des conjoints
    for i in range(n_c):
        #conjoint = Conjoint(Conjoints['Identifiant'][i], Conjoints['Rang'][i], Conjoints['Age'][i], Conjoints['Sexe'][i])
        #indice de agent correspondant dans Agents
        if Conjoints['Identifiant'][i] in indices_agents:
            indice_a = indices_agents[Conjoints['Identifiant'][i]]
            Agents[indice_a].ajouterConjoint(Conjoints['Age'][i], Conjoints['Sexe'][i], Conjoints['Rang'][i])
        
    #Ajout des enfants
    for i in range(n_e):
        #indice de agent correspondant dans Agents
        if Enfants['Identifiant'][i] in indices_agents:
            indice_a = indices_agents[Enfants['Identifiant'][i]]
            Agents[indice_a].ajouterEnfant(Enfants['Age'][i], Enfants['Sexe'][i], Enfants['Rang'][i])
        
        
    # tableaux pour stocker les survies
    Agents_projetes = {}
    Conjoints_projetes = {}
    #Enfants_projetes = {}
    
    for i in range(n_a):
        Agents_projetes[Agents[i].getIdentifiant()] = [n_simulation] + [0]*(MAX_ANNEES-1)
        
    for i in range(n_a):
        for conj in Agents[i].Conjoints:
            Conjoints_projetes[(Agents[i].getIdentifiant(), conj.getRang())] = [n_simulation] + [0]*(MAX_ANNEES-1)
    
    def resetAgents():
        for i in range(n_a):
            Agents[i].setVivant()
            Agents[i].setVivantConjoints()
    
    
    for k in range(n_simulation):
        resetAgents()
        for j in range(1,MAX_ANNEES):
            for i in range(n_a):
                Agents_projetes[Agents[i].getIdentifiant()][j] += Agents[i].projeter(Table, j)
                for conj in Agents[i].Conjoints:
                    Conjoints_projetes[(Agents[i].getIdentifiant(), conj.getRang())][j] += conj.projeter(Table, j)
        
    return {w : [z/n_simulation for z in Agents_projetes[w]] for w in Agents_projetes}, {w : [z/n_simulation for z in Conjoints_projetes[w]] for w in Conjoints_projetes}
            


#%%

def calculerEffectif(AgentsProjetes):
    survie_Agents = {}
    #survie_Conjoint = {}
    #survie_Enfants = {}
    
    print(AgentsProjetes)
    
    n_agents, n_annees, n_sim = AgentsProjetes.shape
    
    for i in range(n_agents):
        temp = [0]*n_annees
        for j in range(n_annees):
            temp_sum = 0
            for k in range(n_sim):
                temp_sum = temp_sum + AgentsProjetes[i,j,k].getVivant()
            temp_sum = temp_sum/n_sim
            temp[j] = temp_sum
        survie_Agents[AgentsProjetes[i,0,0].getIdentifiant()] = temp
                #survie_Agents[AgentsProjetes[i,j,k]]

    return survie_Agents

#%%
################################################# Code pour les tests ############################################

# nombre maximum d'années de projection
MAX_ANNEES = 60

# chargement des données
agents_0=pd.read_csv("Actifs_0.csv",sep=";",decimal=',')
conjoints_0=pd.read_csv("conjoints.csv",sep=";",decimal=',')
enfants_0=pd.read_csv("enfants.csv",sep=";",decimal=',')


#%%


t1 = time.time()

survie_agents, survie_conjoints = simulerEffectif(agents_0, conjoints_0, enfants_0, act.TV_88_90,1000,MAX_ANNEES=60)
t2 = time.time()

print('Durée de calcul (minutes) : ', (t2-t1)/60)


#%%
















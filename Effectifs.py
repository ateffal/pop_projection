
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
def turnover(age) :
    if age<30:
        return 0.02
    else:
        if age <45:
            return 0.01
        else:
            return 0


#%%

class Personne:
    def __init__(self, identifiant, age, sexe):
        self.identifiant = identifiant
        self.Age_0 = age
        self.Age = age
        self.Sexe = sexe
        self.Vivant = 1
        
        
    def getAge(self):
        return self.Age
    
    def getAge0(self):
        return self.Age_0
    
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
        
    def setAge(self, age):
        self.Age = age
    
    def resetAge(self):
        self.Age = self.Age_0
        
        
    def avancerAge(self):
        self.Age = self.Age + 1
        
    def will_survive(self, table, n = 1):
        
        if self.Vivant == 1 :
            survie = is_alive(self.getAge() + n , table)
            if survie == 0:
                self.decede()
        else:
            survie = 0
        
        #self.Age = self.Age + n
        return survie
            
        
            

#%%

class Conjoint(Personne):
    def __init__(self, identifiant, rang, age, sexe):
        Personne.__init__(self, identifiant, age, sexe)
        self.Rang = rang
        
    def getRang(self):
        return self.Rang
    
    def getIdentifiant(self):
        return (self.identifiant, self.Rang)

#%%
        
class Enfant(Personne):
    def __init__(self, identifiant, rang, age, sexe):
        Personne.__init__(self, identifiant, age, sexe)
        self.Rang = rang
    
    def getRang(self):
        return self.Rang
    
    def getIdentifiant(self):
        return (self.identifiant, self.Rang)
        

#%%

class Agent(Personne):
    
    def __init__(self,identifiant,age, sexe):
        Personne.__init__(self, identifiant, age, sexe)
        self.Conjoints = []
        self.Enfants = []
        self.maxRangConjoint = 0
        self.maxRangEnfant = 0
        self.Present = 1
    
    def getPresent(self):
        return self.Present
    
    def setPresent(self, present = 1):
        self.Vivant = present
        
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
            
#    def setPresentConjoints(self, present):
#        for conj in self.Conjoints:
#            conj.setPresent(present)
            
    def projeter(self, table, n = 1):
        # return (survie, deces, demission) 
        vivant = Personne.will_survive(self, table, n)
        if vivant == 0:
            return (0, 1, 0) # agent decede
        
        present = is_present(self.Age)
        if present == 0 :
            self.setPresent(0)
            return (0, 0, 1) 
        
        return (1, 0, 0) # agent present et vivant
    

#%%

def is_alive(Age, Table):
    global a_supprimer_1
    global a_supprimer_2
   
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
        else:
            print('Conjoint ' + Conjoints['Identifiant'][i] + ' ne correspond à aucun agent.')
        
    #Ajout des enfants
    for i in range(n_e):
        #indice de agent correspondant dans Agents
        if Enfants['Identifiant'][i] in indices_agents:
            indice_a = indices_agents[Enfants['Identifiant'][i]]
            Agents[indice_a].ajouterEnfant(Enfants['Age'][i], Enfants['Sexe'][i], Enfants['Rang'][i])
        else:
            print('Enfant ' + Enfants['Identifiant'][i] + ' ne correspond à aucun agent.')
        
        
    # dics pour stocker les survies : {id:[tableau de survies]}
    Agents_survie = {}
    Agents_deces = {}
    Agents_dem = {}
    Conjoints_survie = {}
    Conjoints_deces = {}
    
    #Enfants_projetes = {}
    
    for i in range(n_a):
        Agents_survie[Agents[i].getIdentifiant()] = [n_simulation] + [0]*(MAX_ANNEES-1)
        Agents_deces[Agents[i].getIdentifiant()] = [0] + [0]*(MAX_ANNEES-1)
        Agents_dem[Agents[i].getIdentifiant()] = [0] + [0]*(MAX_ANNEES-1)
        
    for i in range(n_a):
        for conj in Agents[i].Conjoints:
            Conjoints_survie[(Agents[i].getIdentifiant(), conj.getRang())] = [n_simulation] + [0]*(MAX_ANNEES-1)
            Conjoints_deces[(Agents[i].getIdentifiant(), conj.getRang())] = [0] + [0]*(MAX_ANNEES-1)
    
    def resetAgents():
        for i in range(n_a):
            Agents[i].setVivant()
            Agents[i].setPresent()
            Agents[i].resetAge()
            Agents[i].setVivantConjoints()
            for conj in Agents[i].Conjoints:
                conj.resetAge()
            
    for k in range(n_simulation):
        resetAgents()
        for j in range(1,MAX_ANNEES):
            for i in range(n_a):
                
                s, d, dem = Agents[i].projeter(Table, 1)
                Agents_survie[Agents[i].getIdentifiant()][j] += s
                Agents_deces[Agents[i].getIdentifiant()][j] += d
                Agents_dem[Agents[i].getIdentifiant()][j] += dem
                Agents[i].avancerAge()
#                if Agents[i].getIdentifiant() == 'id112996' and j == 2:
#                    print('Age agent = ' + str(Agents[i].getVivant()))
                
                for conj in Agents[i].Conjoints:
                    s_c = conj.will_survive(Table, 1)
                    Conjoints_survie[(Agents[i].getIdentifiant(), conj.getRang())][j] += s_c
                    Conjoints_deces[(Agents[i].getIdentifiant(), conj.getRang())][j] += (1-s_c)
                    conj.avancerAge()
        
    return {w : [z/n_simulation for z in Agents_survie[w]] for w in Agents_survie}, \
           {w : [z/n_simulation for z in Conjoints_survie[w]] for w in Conjoints_survie}, \
           {w : [z/n_simulation for z in Agents_deces[w]] for w in Agents_deces}, \
           {w : [z/n_simulation for z in Agents_dem[w]] for w in Agents_dem}, \
           {w : [z/n_simulation for z in Conjoints_deces[w]] for w in Conjoints_deces}
           
            


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
agents_0=pd.read_csv("Adherents_0.csv",sep=";",decimal=',')
conjoints_0=pd.read_csv("conjoints.csv",sep=";",decimal=',')
enfants_0=pd.read_csv("enfants.csv",sep=";",decimal=',')

#mise en forme des dates
agents_0["DateEngagement"] = pd.to_datetime(agents_0["DateEngagement"],format='%d/%m/%Y')


#%%

t1 = time.time()

survie_agents, survie_conjoints, deces_agents, dem_agents, deces_conjoints  = simulerEffectif(agents_0, conjoints_0, enfants_0, act.TV_88_90,1000,MAX_ANNEES=60)
t2 = time.time()

print('Durée de calcul (minutes) : ', (t2-t1)/60)


#%%

# aggregation des projections annuelles

effectifs_actifs =[0]*MAX_ANNEES
effectifs_retraites =[0]*MAX_ANNEES

n = len(agents_0)

for i in range(n):
    age = agents_0['Age'][i]
    for j in range(MAX_ANNEES):
        if 1:
            
        


effectifs_agents =[0]*MAX_ANNEES           
    
for a in survie_agents:
    effectifs_agents = [i + j for i, j in zip(effectifs_agents, survie_agents[a])]
    
print(effectifs_agents)

effectifs_conjoints =[0]*MAX_ANNEES   

for a in survie_conjoints:
    effectifs_conjoints = [i + j for i, j in zip(effectifs_conjoints, survie_conjoints[a])]

print(effectifs_conjoints)


effectifs_agents_deces =[0]*MAX_ANNEES           
    
for a in deces_agents:
    effectifs_agents_deces = [i + j for i, j in zip(effectifs_agents_deces, deces_agents[a])]
    
print(effectifs_agents_deces)






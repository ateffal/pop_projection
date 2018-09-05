
"""
Created on Mon May  7 14:08:56 2018

@author: a.teffal
"""
#%%

import random


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

def probaMariage(age, typeAgent = 'Actif'):
    """
    Return the probability of getting maried  during the following year at a given age

    """
    if typeAgent == None or typeAgent=='Actif':
        if age >= 35 and age <= 65:
            return 1
        else :
            return 0
    else:
        return 0


    # initialisation des probabilités de mariage annuelles
#    probamariabge = {}
#    for i in range(25,55):
#        probamariabge[str(i)] = 0.0950338528553041
#    age = str(age)
#    if not age in probamariabge:
#        return 0
#    return probamariabge[age]




#%%

class Personne:
    def __init__(self, identifiant, age, sexe, situationFamille):
        self.identifiant = identifiant
        self.Age_0 = age
        self.Age = age
        self.Sexe = sexe
        self.Vivant = 1
        self.SituationFamille_0 = situationFamille
        self.SituationFamille = situationFamille


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

    def getSituationFamille0(self):
        return self.SituationFamille

    def getSituationFamille(self):
        return self.SituationFamille

    def decede(self):
        self.Vivant = 0

    def setVivant(self):
        self.Vivant = 1

    def setAge(self, age):
        self.Age = age

    def resetAge(self):
        self.Age = self.Age_0

    def setSituationFamille(self, sitFam):
        self.SituationFamille = sitFam

    def resetSituationFamille(self):
        self.SituationFamille = self.SituationFamille_0


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
    def __init__(self, identifiant, rang, age, sexe, situationFamille):
        Personne.__init__(self, identifiant, age, sexe, situationFamille)
        self.Rang = rang

    def getRang(self):
        return self.Rang

    def getIdentifiant(self):
        return (self.identifiant, self.Rang)

#%%

class Enfant(Personne):
    def __init__(self, identifiant, rang, age, sexe):
        Personne.__init__(self, identifiant, age, sexe, 'Célibataire')
        self.Rang = rang

    def getRang(self):
        return self.Rang

    def getIdentifiant(self):
        return (self.identifiant, self.Rang)


#%%

class Agent(Personne):

    def __init__(self,identifiant,age, sexe, situationFamille, type_):
        Personne.__init__(self, identifiant, age, sexe, situationFamille)
        self.Conjoints = []
        self.Conjoints_0 = []
        self.Enfants = []
        self.maxRangConjoint = 0
        self.maxRangConjoint_0 = 0
        self.maxRangEnfant = 0
        self.Present = 1
        self.Type = type_

    def getPresent(self):
        return self.Present

    def setPresent(self, present = 1):
        self.Vivant = present

    def getType(self):
        return self.Type

    def ajouterConjoint_0(self, age, sexe, rang = None):
        self.maxRangConjoint += 1
        self.maxRangConjoint_0 += 1
        if rang == None:
            rang = self.maxRangConjoint

        self.Conjoints.append(Conjoint(self.identifiant,rang, age, sexe, 'Marié(e)'))
        self.Conjoints_0.append(Conjoint(self.identifiant,rang, age, sexe, 'Marié(e)'))

        return rang

    def ajouterConjoint(self, age, sexe, rang = None):
        self.maxRangConjoint += 1
        if rang == None:
            rang = self.maxRangConjoint

        self.Conjoints.append(Conjoint(self.identifiant,rang, age, sexe, 'Marié(e)'))

        return rang

    def ajouterEnfant(self, age, sexe, rang = None):
        self.maxRangEnfant += 1
        if rang == None:
            self.Enfants.append(Enfant(self.identifiant,self.maxRangEnfant, age, sexe))
        else:
            self.Enfants.append(Enfant(self.identifiant,rang, age, sexe))

    def setVivantConjoints(self):
        for conj in self.Conjoints:
            conj.setVivant()

    def resetConjoints(self):
        self.Conjoints = self.Conjoints_0.copy()

    def resetMaxRang(self):
        self.maxRangConjoint = self.maxRangConjoint_0

    def projeter(self, table, n = 1):
        if Personne.getVivant(self) == 0:
            return (0, 0, 0)

        vivant = Personne.will_survive(self, table, n)
        if vivant == 0:
            return (0, 1, 0) # agent decede

        present = is_present(self.Age)
        if present == 0 :
            self.setPresent(0)
            return (0, 0, 1)

        # si l'agent est present on va voir s'il va se marier
#        marie = willMarry(self.Age)
#        if marie == 1 :
#            if self.getSexe() == 'Masculin':
#                self.ajouterConjoint(self.getAge() - 5, 'Féminin')
#            else :
#                self.ajouterConjoint(self.getAge() + 5, 'Masculin')

        # agent present et vivant
        return (1, 0, 0)


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
def willMarry(Age, typeAgent):
    if random.random() < probaMariage(Age, typeAgent):
        return 1
    else:
        return 0


#%%

def simulerEffectif(Adherents, Conjoints, Enfants, Table, n_simulation, MAX_ANNEES = 50):

    #a supprimer
    nb_mariages = 0

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
        agent = Agent(Adherents['Identifiant'][i], Adherents['Age'][i], Adherents['Sexe'][i], Adherents['SituationFamiliale'][i], Adherents['Type'][i])
        indices_agents[Adherents['Identifiant'][i]] = i
        Agents.append(agent)

    #Ajout des conjoints
    for i in range(n_c):
        if Conjoints['Identifiant'][i] in indices_agents:
            indice_a = indices_agents[Conjoints['Identifiant'][i]]
            Agents[indice_a].ajouterConjoint_0(Conjoints['Age'][i], Conjoints['Sexe'][i], Conjoints['Rang'][i])
        else:
            print('Conjoint ' + Conjoints['Identifiant'][i] + ' ne correspond à aucun agent.')

    print('Lenght Conjoints : ' + str(len(Conjoints)))

    #Ajout des enfants
    for i in range(n_e):
        #indice de agent correspondant dans Agents
        if Enfants['Identifiant'][i] in indices_agents:
            indice_a = indices_agents[Enfants['Identifiant'][i]]
            Agents[indice_a].ajouterEnfant(Enfants['Age'][i], Enfants['Sexe'][i], Enfants['Rang'][i])
#        else:
#            print('Enfant ' + Enfants['Identifiant'][i] + ' ne correspond à aucun agent.')


    # dics pour stocker les probabliytés de survies, décès et démissions : ex : {id:[tableau de survies]}
    Agents_survie = {}
    Agents_deces = {}
    Agents_dem = {}
    Conjoints_survie = {}
    Conjoints_deces = {}

    #Enfants_projetes = {}

    # initialisation des dics
    for i in range(n_a):
        Agents_survie[Agents[i].getIdentifiant()] = [n_simulation] + [0]*(MAX_ANNEES-1)
        Agents_deces[Agents[i].getIdentifiant()] = [0] + [0]*(MAX_ANNEES-1)
        Agents_dem[Agents[i].getIdentifiant()] = [0] + [0]*(MAX_ANNEES-1)

    for i in range(n_a):
        for conj in Agents[i].Conjoints:
            Conjoints_survie[(Agents[i].getIdentifiant(), conj.getRang())] = [n_simulation] + [0]*(MAX_ANNEES-1)
            Conjoints_deces[(Agents[i].getIdentifiant(), conj.getRang())] = [0] + [0]*(MAX_ANNEES-1)

    print('Lenght survie_conjoints : ' + str(len(Conjoints_survie)))

    # remise à l'état initial des agents( appelée à la fin de chaque simulation)
    def resetAgents():
        for i in range(n_a):
            Agents[i].setVivant()
            Agents[i].setPresent()
            Agents[i].resetAge()
            # Agents[i].resetSituationFamille()
            Agents[i].setVivantConjoints()
            Agents[i].resetMaxRang()
            for conj in Agents[i].Conjoints:
                conj.resetAge()
                #conj.resetSituationFamille()

    for k in range(n_simulation):
        for j in range(1,MAX_ANNEES):
            for i in range(n_a):
                # probilités de survie (s), décès (d) et démission (dem)
                s, d, dem = Agents[i].projeter(Table, 1)
                Agents_survie[Agents[i].getIdentifiant()][j] += s
                Agents_deces[Agents[i].getIdentifiant()][j] += d
                Agents_dem[Agents[i].getIdentifiant()][j] += dem

                # si l'agent est vivant voir s'il va se marier mais seulement
                #s'il est non Marié(e)
                if not Agents[i].getSituationFamille() == 'Marié(e)' :
                    age = Agents[i].getAge()
                    marie = willMarry(age, Agents[i].getType())
                    if marie == 1 :
                        # a supprimer
                        if j==1:
                            nb_mariages += 1
                        if Agents[i].getSexe() == 'Masculin':
                            rang = Agents[i].ajouterConjoint(age - 5, 'Féminin')
                        else :
                            rang = Agents[i].ajouterConjoint(age + 5, 'Masculin')

                        #mettre à jour la situation de famille
                        Agents[i].setSituationFamille('Marié(e)')

                        # ajouter l'id du nouveau conjoint dans Conjoints_survie et Conjoints_deces
                        Conjoints_survie[(Agents[i].getIdentifiant(), rang)] = [0]*MAX_ANNEES
                        Conjoints_deces[(Agents[i].getIdentifiant(), rang)] = [0]*MAX_ANNEES
                        Conjoints_survie[(Agents[i].getIdentifiant(), rang)][j] = 1 # le conjoint est vivant lors de son mariage !

                # mise à jour de l'âge de l'agent
                Agents[i].avancerAge()


                for conj in Agents[i].Conjoints:
                    # probilités de survie (s_c)
                    s_c = conj.will_survive(Table, 1)
                    Conjoints_survie[(Agents[i].getIdentifiant(), conj.getRang())][j] += s_c
                    Conjoints_deces[(Agents[i].getIdentifiant(), conj.getRang())][j] += (1-s_c)
                    conj.avancerAge()
        resetAgents()

    # a supprimer
    print('nombre de nouveaux mariages : ' + str(nb_mariages))
    return {w : [z/n_simulation for z in Agents_survie[w]] for w in Agents_survie}, \
           {w : [z/n_simulation for z in Conjoints_survie[w]] for w in Conjoints_survie}, \
           {w : [z/n_simulation for z in Agents_deces[w]] for w in Agents_deces}, \
           {w : [z/n_simulation for z in Agents_dem[w]] for w in Agents_dem}, \
           {w : [z/n_simulation for z in Conjoints_deces[w]] for w in Conjoints_deces}




#%%








































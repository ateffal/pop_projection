# # Projections des effectifs de la CRP en groupe ouvert
# # #####################################################

# Importation des packages
from pop_projection import Effectifs as eff
import pandas as pd
import numpy as np
import inspect
import time
from datetime import datetime

def file_name_csv(path_exp, file_name):
    temp  =time.strftime("%Y%m%d_%H%M%S")
    return path_exp + file_name + '_' + temp + '.csv'

def file_name(path_exp, file_name):
    # temp  =time.strftime("%Y%m%d_%H%M%S")
    temp = ''
    return path_exp + file_name + '.xlsx'


def law_ret1(age, DateNaissance, DateEngagement, year_proj):

    date_naiss = datetime.strptime(DateNaissance, '%d/%m/%Y')
    date_eng = datetime.strptime(DateEngagement, '%d/%m/%Y')

    # Mois de naissance
    mois_naiss = date_naiss.month

    # jour de naissance
    jour_naiss = date_naiss.day

    # Date de départ théorique
    if date_eng.year < 2002:
        # gestion des années bissextile
        if jour_naiss == 29 and mois_naiss == 2:
            temp = '01/03/' + str(date_naiss.year + 55)
        else:
            temp = str(jour_naiss) + '/' + str(mois_naiss) + '/' + str(date_naiss.year + 55)
    else:
        temp = str(jour_naiss) + '/' + str(mois_naiss) + '/' + str(date_naiss.year + 60)

    date_dep = datetime.strptime(temp, '%d/%m/%Y')

    annee_proj = 2018 + year_proj

    if date_dep.year < annee_proj:
        return True
    
    if date_dep.year > annee_proj:
        return False
    
    if date_dep.year == annee_proj:
        if (mois_naiss < 7) or (mois_naiss == 7 and jour_naiss == 1) :
                return True
        else:
            return False

# Loi de naissance
def loi_naiss_1(age):
    """
    Return the probability of having a new born  during the following year at a given age

    """
    if age < 23:
        return 0
    if age > 40:
        return 0
    
    temp = [0.2212, 0.08, 0.0978, 0.115, 0.1305, 0.1419, 0.148, 0.1497, 0.1434, 0.1353, 0.1239, 0.1095, 0.095, 0.08, 0.0653, 0.0516, 0.0408, 0.086]
    # temp = [0, 0, 0, 0, 0, 0, 0, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0, 0, 0, 0, 0]
    
    return temp[age -23]


def loi_naiss_2(age):
    return 0

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



# Define law of replacement
def law_replacement_SC(departures_, year_):
    
    '''
        assumes departures_ is a dic storing number of departures by group of the year year_
        returns a list of dics having keys : key, number and data
        
    '''
    def nouveaux(g_):
        structure_nouveaux = {'1':[25,25,0.5],'2':[25,25,0.5],'3':[25,25,0.5],'4':[29,29,0.5],'5':[28,28,0.5,],
        '6':[28,28,0.5],'7':[33,33,0.5],'8':[38,38,0.5],'9':[38,38,0.5],'10':[47,47,0.5],'11':[49,49,0.5]}

        if str(g_) in structure_nouveaux:
            return structure_nouveaux[str(g_)]
        else:
            return [30, 30, 1.0]

    def taux_rempl(y, g_ = '0'):
        if y <= 3 :
            if str(g_) in ['1','2','3','5','6','7']:
                return 0.64
            else:
                return 1
        else:
            return 1

    new_employees = []

    for g in departures_:
        if departures_[g] > 0 :
            # add a male
            if nouveaux(g)[2] > 0:
                temp = {'key':'NE_Strate_' + str(g) + '_H__'+'année_' + str(year_), 
                'number':nouveaux(g)[2]*departures_[g]*taux_rempl(year_, g),'data':['active', 'male', 'not married', nouveaux(g)[0], '31/12/'+str((2018+year_-nouveaux(g)[0])), '31/12/'+str((2018+year_)), 0, g, g, 0]}
                new_employees.append(temp)

            # add a female
            if nouveaux(g)[2] < 1:
                temp = {'key':'NE_Strate_' + str(g) + '_F__'+'année_' + str(year_), 
                'number':(1-nouveaux(g)[2])*departures_[g]*taux_rempl(year_, g),'data':['active', 'female', 'not married', nouveaux(g)[1], '31/12/'+str((2018+year_-nouveaux(g)[1])), '31/12/'+str((2018+year_)),0, g, g, 0]}
                new_employees.append(temp)
    
    return new_employees

# Chemin des données
path = "../data_2018/"

# Chargement des données
employees = pd.read_csv(path + "employees.csv", sep=";", decimal=",")
spouses = pd.read_csv(path + "spouses.csv", sep=";", decimal=",")
children = pd.read_csv(path + "children.csv", sep=";", decimal=",")

# Projection of population
# Number of years to project
MAX_ANNEES = 60

# Projection
numbers_ = eff.simulerEffectif( employees, spouses, children, 'TV 88-90', MAX_ANNEES, 
                                law_replacement_=law_replacement_SC, law_retirement_= law_ret1, 
                                law_resignation_=turnover)


#Chemin export
path_export = './results/CRP/Python/'

# Effectifs global
effectifs_global = eff.globalNumbers(numbers_[0], numbers_[1], numbers_[2], MAX_ANNEES)
effectifs_global.to_excel(file_name(path_export,'effectifs_global_SC'), index=False)

# Sortants
effectifs_sortants = eff.leavingNumbers(numbers_[0], numbers_[4], MAX_ANNEES)
effectifs_sortants.to_excel(file_name(path_export,'effectifs_sortants_SC'), index=False)



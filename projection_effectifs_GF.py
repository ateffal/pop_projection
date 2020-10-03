# # Projections des effectifs de la CRP en groupe fermé
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
                                law_replacement_=None, law_retirement_= law_ret1, 
                                law_resignation_=turnover)


#Chemin export
path_export = './results/CRP/Python/'

# Effectifs global
effectifs_global = eff.globalNumbers(numbers_[0], numbers_[1], numbers_[2], MAX_ANNEES)
effectifs_global.to_excel(file_name(path_export,'effectifs_global_GF_SC'), index=False)

# Sortants
effectifs_sortants = eff.leavingNumbers(numbers_[0], numbers_[4], MAX_ANNEES)
effectifs_sortants.to_excel(file_name(path_export,'effectifs_sortants_GF_SC'), index=False)




from pop_projection import Effectifs as eff
import pandas as pd
import numpy as np
from datetime import datetime
from pop_projection import sample_laws as sl

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


# Define law of replacement
def law_replacement1(departures_, year_):
    
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
        # add a male
        if nouveaux(g)[2] > 0:
            temp = {'key':'NE_Strate_' + str(g) + '_H__'+'année_' + str(year_), 
            'number':nouveaux(g)[2]*departures_[g]*taux_rempl(year_, g),'data':['active', 'male', 'not married', nouveaux(g)[0], 2018 + year_,g,'31/12/'+str((2018+year_-nouveaux(g)[0])), '31/12/'+str((2018+year_))]}
            new_employees.append(temp)

        # add a female
        if nouveaux(g)[2] < 1:
            temp = {'key':'NE_Strate_' + str(g) + '_F__'+'année_' + str(year_), 
            'number':(1-nouveaux(g)[2])*departures_[g]*taux_rempl(year_, g),'data':['active', 'female', 'not married', nouveaux(g)[1], 2018 + year_,g,'31/12/'+str((2018+year_-nouveaux(g)[1])), '31/12/'+str((2018+year_))]}
            new_employees.append(temp)
    
    return new_employees


# Path for input data
path ="./pop_projection/test/data/"

# employees
ids = ['id1', 'id2', 'id3']
types = ['active', 'retired', 'active']
sexes = ['male', 'female', 'male']
familystatus = ['married', 'married', 'not married']
ages = [30, 65, 45]
Data = {'id':ids,'type' : types, 'sex' : sexes, 'familyStatus' : familystatus, 'age' : ages}
employees = pd.DataFrame(data=Data, columns=['id', 'type', 'sex', 'familyStatus' ,'age'])

# spouses 
ids = ['id1', 'id2']
rangs = [1,1]
sexes = ['female', 'male']
ages = [25, 70]
types = ['active', 'retired']
familystatus = ['married', 'married']
Data = {'id':ids,'rang' : rangs, 'sex' : sexes, 'age' : ages, 'type' : types, 'familyStatus' : familystatus}
spouses = pd.DataFrame(data=Data, columns=['id', 'rang' , 'sex' , 'age' , 'type','familyStatus'])

# children 
ids = []
rangs = []
sexes = []
ages = []
types = []
familystatus = []
Data = {'id':ids,'rang' : rangs, 'sex' : sexes, 'age' : ages, 'type' : types, 'familyStatus' : familystatus}
children = pd.DataFrame(data=Data, columns=['id', 'rang' , 'sex' , 'age' , 'type', 'familyStatus'])

# Projection of population
# Number of years to project
MAX_ANNEES = 60

# Projection
numbers_ = eff.simulerEffectif(employees, spouses, children, MAX_YEARS=MAX_ANNEES)

# global numbers
global_numb = eff.globalNumbers(numbers_[0], numbers_[1], numbers_[2], MAX_ANNEES)

global_numb.to_excel('./pop_projection/test/results/glob_num_toy.xlsx', index=False)


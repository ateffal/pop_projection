from pop_projection import Effectifs as eff
import pandas as pd
import numpy as np
from datetime import datetime

from pop_projection import sample_laws as sl
import pytest


# Define law of retirement
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
path ="./pop_projection/data/"

# tests for insuring that projectNumbers execute correctly
def test_simulerEffectif_1():

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
    ages = [25, 65]
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
    numbers_ = eff.projectNumbers(employees, spouses, children, MAX_YEARS=MAX_ANNEES)

    # global numbers
    global_numb = eff.globalNumbers(numbers_[0], numbers_[1], numbers_[2], MAX_ANNEES)


def test_simulerEffectif_2():

    # Path for input data
    path ="./pop_projection/test/data/"

    # Loading data
    employees = pd.read_csv(path + "employees.csv",sep=";", decimal = ",")
    spouses = pd.read_csv(path + "spouses.csv",sep=";", decimal = ",")
    children = pd.read_csv(path + "children.csv",sep=";", decimal = ",")

    # Projection of population
    # Number of years to project
    MAX_ANNEES = 60

    # Projection
    numbers_ = eff.projectNumbers(employees, spouses, children)

    # global numbers
    global_numb = eff.globalNumbers(numbers_[0], numbers_[1], numbers_[2], MAX_ANNEES)


def test_walk_actives():

    # Path for input data
    path ="./pop_projection/test/data/"

    # Loading data
    employees = pd.read_csv(path + "employees.csv",sep=";", decimal = ",")
    spouses = pd.read_csv(path + "spouses.csv",sep=";", decimal = ",")
    children = pd.read_csv(path + "children.csv",sep=";", decimal = ",")

    # Projection of population
    # Number of years to project
    MAX_ANNEES = 50

    # Projection
    numbers_ = eff.projectNumbers(employees, spouses, children, 'TV 88-90', 
                MAX_ANNEES, law_replacement_ = None)

    # global numbers
    global_numb = eff.globalNumbers(numbers_[0], numbers_[1], numbers_[2], MAX_ANNEES)

    # departures
    departures = eff.leavingNumbers(numbers_[0], numbers_[4], MAX_ANNEES)

    # employees_walk
    employees_walk = pd.merge(global_numb.loc[:,['Year', 'effectif_actifs']],
                              departures, on='Year')
    
    # In case of no replacement, employees numbers must satisfy :
    # Numbers(year N + 1 ) = Numbers(year N) - Deaths(year N) - 
    #                        Reignations(year N) - New Retirees(year N)

    for i in range(1,MAX_ANNEES):
        temp = (employees_walk.loc[i-1, 'effectif_actifs']-
               employees_walk.loc[i, 'Total Leaving']-
               employees_walk.loc[i, 'effectif_deces_nouveaux_retraites'])
        temp_diff = abs(temp-employees_walk.loc[i, 'effectif_actifs'])
        assert temp_diff<0.00001, "Walk equality not satisfaied in year " + str(i ) + " diff : " + str(temp_diff)

# Global numbers - no replacement
def test_glob_num_no_rep():

    # Path for input data
    path ="./pop_projection/test/data/"

    # Loading data
    employees = pd.read_csv(path + "employees.csv",sep=";", decimal = ",")
    spouses = pd.read_csv(path + "spouses.csv",sep=";", decimal = ",")
    children = pd.read_csv(path + "children.csv",sep=";", decimal = ",")

    # Projection of population
    # Number of years to project
    MAX_ANNEES = 60

    # Projection
    numbers_ = eff.projectNumbers(employees, spouses, children, 'TV 88-90', MAX_ANNEES, law_replacement_ = None,
                                  law_resignation_=sl.turnover, law_retirement_=law_ret1)

    # global numbers
    global_numb = eff.globalNumbers(numbers_[0], numbers_[1], numbers_[2], MAX_ANNEES)

    # load expected numbers
    expected_global_numbers = pd.DataFrame(pd.read_csv("./pop_projection/test/expected_glob_num_no_rep.csv",
                              sep=";", decimal = ","))

    cols = list(expected_global_numbers.columns)

    for c in cols[1:4]:
        res = list(global_numb[c])
        expected_res = list(expected_global_numbers[c])
        for i in range(len(res)):
            assert abs(res[i]-expected_res[i]) < 0.000001, "Numbers in column " + c + " far from expected at year " + str(i) + " !"


# Global numbers - with replacement
def test_glob_num_with_rep():

    # Path for input data
    path ="./pop_projection/test/data/"

    # Loading data
    employees = pd.read_csv(path + "employees.csv",sep=";", decimal = ",")
    spouses = pd.read_csv(path + "spouses.csv",sep=";", decimal = ",")
    children = pd.read_csv(path + "children.csv",sep=";", decimal = ",")

    # Projection of population
    # Number of years to project
    MAX_ANNEES = 60

    # Projection
    numbers_ = eff.projectNumbers(employees, spouses, children, 'TV 88-90', MAX_ANNEES, law_replacement_ = law_replacement1,
                                  law_resignation_=sl.turnover, law_retirement_=law_ret1)

    # global numbers
    global_numb = eff.globalNumbers(numbers_[0], numbers_[1], numbers_[2], MAX_ANNEES)

    # load expected numbers
    expected_global_numbers = pd.DataFrame(pd.read_csv("./pop_projection/test/expected_glob_num_with_rep.csv",
                              sep=";", decimal = ","))

    cols = list(expected_global_numbers.columns)
    for c in cols[1:4]:
        res = list(global_numb[c])
        expected_res = list(expected_global_numbers[c])
        for i in range(len(res)):
            assert abs(res[i]-expected_res[i]) < 0.00001, "Numbers in column " + c + " far from expected at year " + str(i) + " !"


def test_individual_numbers():
    # Loading data
    employees = pd.read_csv(path + "employees.csv",sep=";", decimal = ",")
    spouses = pd.read_csv(path + "spouses.csv",sep=";", decimal = ",")
    children = pd.read_csv(path + "children.csv",sep=";", decimal = ",")

    # Projection of population
    # Number of years to project
    MAX_ANNEES = 10

    # Projection
    numbers_ = eff.projectNumbers(employees, spouses, children, 'TV 88-90', MAX_ANNEES, law_replacement_ = law_replacement1)

    # global numbers
    global_numb = eff.globalNumbers(numbers_[0], numbers_[1], numbers_[2], MAX_ANNEES)


    # verify first id in live individual numbers
    indiv_lives = eff.individual_employees_numbers(numbers_[0])[0]

    res = list(indiv_lives.iloc[0,8:])

    expected_res = [1, 0.99945, 0.99887, 0.99825, 0.99761, 0.99695, 0.99623, 0.99542, 0.99452, 0.99359]

    diff = [abs(i-j) for i,j in zip(res, expected_res)]

    assert max(diff) < 5

    # strict comparaison of global numbers
    # load expected numbers
    expected_global_numbers = pd.DataFrame(pd.read_csv("./pop_projection/test/expected_global_numbers.csv",sep=";", decimal = ","))

    # assert expected_global_numbers.equals(global_numb)

    cols = list(expected_global_numbers.columns)

    for c in cols:
        res = list(global_numb[c])
        expected_res = list(expected_global_numbers[c])
        diff = [abs(i-j) for i,j in zip(res, expected_res)]
        assert max(diff) < 5, "Numbers in column " + c + " far from expected!" 


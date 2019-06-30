from pop_projection import Effectifs as eff
import pandas as pd
import numpy as np

from pop_projection import sample_laws as sl



def law_ret1(age, Date_Engagement, DateNaissance, year_proj):

    date_naiss = datetime.strptime(DateNaissance, '%d/%m/%Y')
    date_eng = datetime.strptime(Date_Engagement, '%d/%m/%Y')

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
        structure_nouveaux = {'1':[25,25,0.8],'2':[25,25,0.8],'3':[25,25,0.6],'4':[29,29,0.6],'5':[28,28,0.5,],
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
            temp = {'key':'male_groupe_' + str(g) + 'year_' + str(year_), 
            'number':nouveaux(g)[2]*departures_[g]*taux_rempl(year_, g),'data':['active', 'male', 'not married', nouveaux(g)[0], year_,g,'01/01/'+str((2018+year_+1)),'31/12/'+str((2018+year_-nouveaux(g)[0]))]}
            new_employees.append(temp)

        # add a female
        if nouveaux(g)[2] < 1:
            temp = {'key':'female_groupe_' + str(g) + 'year_' + str(year_), 
            'number':(1-nouveaux(g)[2])*departures_[g]*taux_rempl(year_, g),'data':['active', 'female', 'not married', nouveaux(g)[1], year_,g,'01/01/'+str((2018+year_+1)),'31/12/'+str((2018+year_-nouveaux(g)[1]))]}
            new_employees.append(temp)
    
    return new_employees

# Path for input data
path ="./pop_projection/data/"


def test_simulerEffectif_1():
    # Loading data
    employees = pd.read_csv(path + "employees.csv",sep=";", decimal = ",")
    spouses = pd.read_csv(path + "spouses.csv",sep=";", decimal = ",")
    children = pd.read_csv(path + "children.csv",sep=";", decimal = ",")

    # Projection of population
    # Number of years to project
    MAX_ANNEES = 60

    # Projection
    numbers_ = eff.simulerEffectif(employees, spouses, children, 'TV 88-90', MAX_ANNEES, law_replacement_ = sl.law_replacement1,
                                  law_resignation_=sl.turnover)

    # global numbers
    global_numb = eff.globalNumbers(numbers_[0], numbers_[1], numbers_[2], MAX_ANNEES)

    # load expected numbers
    expected_global_numbers = pd.DataFrame(pd.read_csv("./pop_projection/test/expected_global_numbers_2.csv",
                              sep=";", decimal = ","))

    cols = list(expected_global_numbers.columns)

    for c in cols:
        res = list(global_numb[c])
        expected_res = list(expected_global_numbers[c])
        diff = [abs(i-j) for i,j in zip(res, expected_res)]
        assert max(diff) < 0.001, "Numbers in column " + c + " far from expected!" 


def test_simulerEffectif_2():
    # Loading data
    employees = pd.read_csv(path + "employees.csv",sep=";", decimal = ",")
    spouses = pd.read_csv(path + "spouses.csv",sep=";", decimal = ",")
    children = pd.read_csv(path + "children.csv",sep=";", decimal = ",")

    # Projection of population
    # Number of years to project
    MAX_ANNEES = 10

    # Projection
    numbers_ = eff.simulerEffectif(employees, spouses, children, 'TV 88-90', MAX_ANNEES, law_replacement_ = law_replacement1)

    # global numbers
    global_numb = eff.globalNumbers(numbers_[0], numbers_[1], numbers_[2], MAX_ANNEES)


    # verify first id in live individual numbers
    indiv_lives = eff.individual_employees_numbers(numbers_[0])[0]

    res = list(indiv_lives.iloc[0,8:])

    expected_res = [1, 0.99945, 0.99887, 0.99825, 0.99761, 0.99695, 0.99623, 0.99542, 0.99452, 0.99359]

    diff = [abs(i-j) for i,j in zip(res, expected_res)]

    assert max(diff) < 0.0001

    # strict comparaison of global numbers
    # load expected numbers
    expected_global_numbers = pd.DataFrame(pd.read_csv("./pop_projection/test/expected_global_numbers.csv",sep=";", decimal = ","))

    # assert expected_global_numbers.equals(global_numb)

    cols = list(expected_global_numbers.columns)

    for c in cols:
        res = list(global_numb[c])
        expected_res = list(expected_global_numbers[c])
        diff = [abs(i-j) for i,j in zip(res, expected_res)]
        assert max(diff) < 0000000.1, "Numbers in column " + c + " far from expected!" 

def test_simulerEffectif_3():
    # Loading data
    employees = pd.read_csv(path + "employees.csv",sep=";", decimal = ",")
    spouses = pd.read_csv(path + "spouses.csv",sep=";", decimal = ",")
    children = pd.read_csv(path + "children.csv",sep=";", decimal = ",")

    # Projection of population
    # Number of years to project
    MAX_ANNEES = 10

    # Projection
    numbers_ = eff.simulerEffectif(employees, spouses, children, 'TV 88-90', MAX_ANNEES, law_replacement_ = law_replacement1)

    # global numbers
    global_numb = eff.globalNumbers(numbers_[0], numbers_[1], numbers_[2], MAX_ANNEES)

    # strict comparaison of global numbers
    # load expected numbers
    expected_global_numbers = pd.DataFrame(pd.read_csv("./pop_projection/test/expected_global_numbers.csv",sep=";", decimal = ","))

    cols = list(expected_global_numbers.columns)

    for c in cols:
        res = list(global_numb[c])
        expected_res = list(expected_global_numbers[c])
        diff = [abs(i-j) for i,j in zip(res, expected_res)]
        assert max(diff) < 0000000.1, "Numbers in column " + c + " far from expected!" 


def test_walk_actives():
    # Loading data
    employees = pd.read_csv(path + "employees.csv",sep=";", decimal = ",")
    spouses = pd.read_csv(path + "spouses.csv",sep=";", decimal = ",")
    children = pd.read_csv(path + "children.csv",sep=";", decimal = ",")

    # Projection of population
    # Number of years to project
    MAX_ANNEES = 50

    # Projection
    numbers_ = eff.simulerEffectif(employees, spouses, children, 'TV 88-90', 
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
               employees_walk.loc[i, 'Total Leaving'])

        assert abs(temp-employees_walk.loc[i, 'effectif_actifs'])<0.02, "Walk equality not respected in year " + str(i )



def test_simulerEffectif_5():

    # Path of data
    path ="./pop_projection/test/"

    # Loading data
    employees = pd.read_csv(path + "employees_id1.csv",sep=";", decimal = ",")
    spouses = pd.read_csv(path + "spouses_id1.csv",sep=";", decimal = ",")
    children = pd.read_csv(path + "children_id1.csv",sep=";", decimal = ",")

    # Projection of population
    # Number of years to project
    MAX_ANNEES = 10

    # Projection
    numbers_ = eff.simulerEffectif(employees, spouses, children, 'TV 88-90', 
                                   MAX_ANNEES, law_replacement_ = None, 
                                   law_resignation_=sl.turnover)

    # global numbers
    global_numb = eff.globalNumbers(numbers_[0], numbers_[1], numbers_[2], MAX_ANNEES)

    # verify last year global numbers
    res = list(global_numb['effectif_actifs'])

    expected_result = [1, 0.9882544, 0.986335262, 0.984314041, 0.982211155, 0.979934729, 
                       0.97745414, 0.97475918, 0.971839639, 0.968675101]

    diff = [abs(i-j) for i,j in zip(res, expected_result)]

    assert max(diff) < 0.00001
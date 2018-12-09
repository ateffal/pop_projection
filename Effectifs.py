
"""
Created on Mon May  7 14:08:56 2018

@author: a.teffal

"""
#%%

import pandas as pd
from pop_projection import Actuariat as act
import inspect




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

#%%
def probaMariage(age, typeAgent):
    """
    Return the probability of getting maried  during the following year at a given age

    """
    if typeAgent=='active':
        if age >= 25 and age <= 54:
            return 0.095
        else :
            return 0
    else:
        return 0
    

def probaNaissance(age):
    """
    Return the probability of having a new born  during the following year at a given age

    """
    if age < 23:
        return 0
    if age > 40:
        return 0
    
    # temp = [0.2212, 0.08, 0.0978, 0.115, 0.1305, 0.1419, 0.148, 0.1497, 0.1434, 0.1353, 0.1239, 0.1095, 0.095, 0.08, 0.0653, 0.0516, 0.0408, 0.086]
    temp = [0, 0, 0, 0, 0, 0, 0, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0, 0, 0, 0, 0]
    
    return temp[age -23]
    
#%%

def is_alive(Age, Table):
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

def verifyCols(data_, cols):
    '''
    verify that list of cols exist in data_

    '''
    temp = []
    cols_data = list(data_.columns)
    for c in cols:
        if not c in cols_data:
            temp.append(c)
    
    return temp



def simulerEffectif(employees, spouses, children, mortalityTable = 'TV 88-90', MAX_YEARS = 50, law_retirement_ = None, 
                    law_resignation_ = None, law_marriage_ = None, law_birth_ = None, law_replacement_ =  None):
    
    ''' assumes employees, spouses and children are pandas dataframes with at least 6 columns :
        - id   : an unique identifier of the employee
        - type : active or retired for employees. active, or retired or widow or widower for spouses and children.
                 for spouses and children, type is the type of the employee taht they are attached to if it's still alive, or widower otherwise
        - sex  : male or female
        - familyStatus : maried, or not maried
        - age
        - group : a sub-population. ex : group of employees recruted before 2002, group of directors,...
                  if we don't have groups, just set it to id
        
        if supplied, law_retirement_ is a tuple : (a function, list of columns of employees to be passed to this function )
        if supplied, law_resignation_ is a tuple : (a function, list of columns of employees to be passed to this function )
        if supplied, law_marriage_ is a tuple : (a function, list of columns of employees to be passed to this function )
        if supplied, law_birth_ is a tuple : (a function, list of columns of employees to be passed to this function )
        
    '''
    #setting law of retirement
    if law_retirement_ == None:
        law_retirement = ret.retire
        cols_ret = ['age'] 
    else:
        law_retirement = law_retirement_[0] if type(law_retirement_) is tuple else law_retirement_
        #cols_ret = law_retirement_[1]
        cols_ret = law_retirement_[1] if type(law_retirement_) is tuple else inspect.getfullargspec(law_retirement)[0]

    # verify that columns exist in dataframe
    unfound_cols = verifyCols(employees, cols_ret)
    if len(unfound_cols) > 0:
        print('Unfound columns in emmloyees : ', unfound_cols)
        return None
        
    #setting law of resignation
    if law_resignation_ == None:
        law_resignation = turnover
        cols_res = ['age']
    else:
        law_resignation = law_resignation_[0] if type(law_resignation_) is tuple else law_resignation_
        cols_res = law_resignation_[1] if type(law_resignation_) is tuple else inspect.getfullargspec(law_resignation)[0]

    # verify that columns exist in dataframe
    unfound_cols = verifyCols(employees, cols_res)
    if len(unfound_cols) > 0:
        print('Unfound columns in emmloyees : ', unfound_cols)
        return None
        
    #setting law of marriage
    if law_marriage_ == None:
        law_marriage = probaMariage
        cols_mar = ['age', 'type']
    else:
        law_marriage = law_marriage_[0] if type(law_marriage_) is tuple else law_marriage_
        cols_mar = law_marriage_[1] if type(law_marriage_) is tuple else inspect.getfullargspec(law_marriage)[0]
        
    # verify that columns exist in dataframe
    unfound_cols = verifyCols(employees, cols_mar)
    if len(unfound_cols) > 0:
        print('Unfound columns in emmloyees : ', unfound_cols)
        return None

    #setting law of birth
    if law_birth_ == None:
        law_birth = probaNaissance
        cols_birth = ['age']
    else:
        law_birth = law_birth_[0] if type(law_birth_) is tuple else law_birth_
        cols_birth = law_birth_[1] if type(law_birth_) is tuple else inspect.getfullargspec(law_birth)[0]
        
    # verify that columns exist in dataframe
    unfound_cols = verifyCols(spouses, cols_birth)
    if len(unfound_cols) > 0:
        print('Unfound columns in spouses : ', unfound_cols)
        return None

    # Numbers of each category of population
    n_e = len(employees) 
    n_s = len(spouses)
    n_c = len(children)
    
    # dics where to store survivals : ex : {id:[list of lives, one for each year]}
    employees_proj = {}
    spouses_proj = {}
    children_proj = {}
    
    
    # initialisation of dics
    #dic of employees. For employees, keys are id (first column)
    for i in range(n_e):
        if employees["type"][i] == "active":
            employees_proj[employees["id"][i]] = {'data':dict(zip(employees.columns[1:],list(employees.iloc[i])[1:])), 'exist':1, 
                'entrance':0, 'lives':[1] + [0]*(MAX_YEARS-1), 'deaths' : [0]*MAX_YEARS, 'res':[0]*MAX_YEARS, 'type':['active'] + ['']*(MAX_YEARS-1)}  
        else:
            employees_proj[employees["id"][i]] = {'data':dict(zip(employees.columns[1:],list(employees.iloc[i])[1:])), 'exist':1, 
                'entrance':0, 'lives':[1] + [0]*(MAX_YEARS-1), 'deaths' : [0]*MAX_YEARS, 'res':[0]*MAX_YEARS, 'type':['retired']*MAX_YEARS}  
            
    #dic of spouses. For spouses, keys are tuples (id, rang) : (first column, second column)
    for i in range(n_s):
        spouses_proj[(spouses["id"][i], spouses["rang"][i])] = {'data':dict(zip(spouses.columns[2:],list(spouses.iloc[i])[2:])), 'exist':1, 
            'entrance':0, 'lives':[1] + [0]*(MAX_YEARS-1), 'deaths' : [0]*MAX_YEARS, 'type':[spouses["type"][i]] + ['']*(MAX_YEARS-1)}
        
        
    print('lenth of spouses_proj at begining : ', len(spouses_proj))
    
    #dic of children. For children, keys are tuples (id, rang) : (first column, second column)
    for i in range(n_c):
        children_proj[(children["id"][i], children["rang"][i])] = {'data':dict(zip(children.columns[2:],list(children.iloc[i])[2:])), 'exist':1, 
            'entrance':0, 'lives':[1] + [0]*(MAX_YEARS-1), 'deaths' : [0]*MAX_YEARS, 'type':[children["type"][i]] + ['']*(MAX_YEARS-1)}
        
    # dic where to store retired of each year : {year : [list of employees that retired that year (their ids)] }
    new_retirees = dict(zip([i for i in range(1, MAX_YEARS)],list([[]]*(MAX_YEARS - 1))))
    
    #number of retirees for each year
    n_new_retirees = [0] * MAX_YEARS

    def add_new_employee(id, year_, sex_, age_, ponderation, group_):
        """Adds a new employee in the employees_proj dic.
        
        Args:
        id: The id of the employee to be added (key of the dic).
        year_: year of projection when this employee is added : 1, 2,...
        sex_ : sex of the employee
        age : age at of the employee at year year_
        ponderation : if 0.5 for example,add 50% of an employee. This is used to handle 'rate' of replacement 

        """
        employees_proj[id] = {'data':dict(zip(['type','sex', 'familyStatus','age', 'Year_employment', 'group'],['active',sex_, 'not married',age_, 2017 + year_, group_  ])), 'exist':0, 
            'entrance':year_, 'lives':[0] * MAX_YEARS, 'deaths' : [0]*MAX_YEARS, 'res':[0]*MAX_YEARS,
            'type':[''] * MAX_YEARS}
        
        # updating lives and type
        employees_proj[id]['lives'][year_] = ponderation
        employees_proj[id]['type'][year_] = 'active'
        
    def add_new_spouse(employee_id, year_, probMar=1):
        """Adds a new spouse in the spouses_proj dic.
        
        Args:
        employee_id: The id of the employee attached to this spouse.
        year_: year of projection when this spouse is added : 1, 2,...
        entrance : year of entrance

        """
        
        if probMar == 0:
            return
        
        # sex
        if employees_proj[employee_id]["data"]["sex"] == 'male':
            sex_temp = 'female'
        else:
            sex_temp = 'male'
            
        #live employee (employee will marry only if still alive)
        live_emp = employees_proj[employee_id]["lives"][year_]
        
        #age. It supposed that difference between ages is -/+ 5 year depending on sex
        if sex_temp == 'female':
            age_temp = employees_proj[employee_id]["data"]["age"] - 5 
        else:
            age_temp = employees_proj[employee_id]["data"]["age"] + 5
        
        #type
        type_temp = employees_proj[employee_id]["type"][i]
        
        #if not already added add it
        if not (employee_id, 1) in spouses_proj:
            spouses_proj[(employee_id, 1)] = {'data':dict(zip(['sex', 'age', 'type', 'familyStatus'],[sex_temp, age_temp, type_temp,'married'])), 'exist':1, 
                'entrance':(year_+1), 'lives':[0] * year_ + [live_emp * probMar] + [0] * (MAX_YEARS- year_ - 1), 'deaths' : [0]*MAX_YEARS,  
                'type':[''] * year_ + [type_temp] + [''] * (MAX_YEARS- year_ - 1)}
        else:
            spouses_proj[(employee_id, 1)]['lives'][year_] = spouses_proj[(employee_id, 1)]['lives'][year_] + live_emp * probMar
    
    
    def add_new_child(employee_id, rang_, year_):
        """Adds a new child in the children_proj dic.
        
        Args:
        employee_id: The id of the employee attached to this child.
        year_: year of projection when this child is added : 1, 2,...
        
        """
        
        if employees_proj[employee_id]["data"]["type"] == "active" or employees_proj[employee_id]["data"]["type"] == "retired" :
            if employees_proj[employee_id]["data"]["sex"] == 'female':
                args_ = tuple([employees_proj[employee_id]["data"][z] for z in cols_birth])
                probBirth = law_birth(*args_)
            else:
                args_ = tuple([spouses_proj[(employee_id, rang_)]["data"][z] for z in cols_birth])
                probBirth = law_birth(*args_)
        else:
            return
                
        if probBirth == 0:
            return
        
        #live employee (or his spouse) (employee or spouse will give birth only if still alive)
        if employees_proj[employee_id]["data"]["sex"] == 'male':
            live_emp = spouses_proj[(employee_id, rang_)]["lives"][year_]
        else:
            live_emp = employees_proj[employee_id]["lives"][year_]
        
        #type
        type_temp = employees_proj[employee_id]["type"][i]
        
        #if not already added add it
        if not (employee_id, 1) in children_proj:
            children_proj[(employee_id, 1)] = {'data':dict(zip(['sex', 'age', 'type', 'familyStatus'],['female', 0, type_temp,'not married'])), 'exist':1, 
                'entrance':(year_+1), 'lives':[0] * year_ + [live_emp * probBirth] + [0] * (MAX_YEARS- year_ - 1), 'deaths' : [0]*MAX_YEARS,  
                'type':[''] * year_ + [type_temp] + [''] * (MAX_YEARS- year_ - 1)}
        else:
            children_proj[(employee_id, 1)]['lives'][year_] = children_proj[(employee_id, 1)]['lives'][year_] + live_emp * probBirth
        
        
    # main loop
    for i in range(1, MAX_YEARS):
        # employees
        n_retired = 0
        n_death = 0
        n_resignation = 0
        n_marriage = 0
        total_departures = 0
        departures = {} # a dic storing the number of departures for a group each year
        
        #projection of employees
        for id, employee in employees_proj.items():
               
            #update age of employee
            #employee["data"]['age'] = employee["data"]['age'] + 1
            age = employee["data"]['age']
            
            #probability of surviving
            survie = act.sfs_nPx(age,1, mortalityTable)
            
            #probability of dying
            death = act.sfs_nQx(age,1, mortalityTable)
            if employee["type"][i-1] == "active":
                n_death += death * employee['lives'][i-1]
                # departure by group
                if employee['data']['group'] in departures:
                    departures[employee['data']['group']] += death * employee['lives'][i-1]
                else:
                    departures[employee['data']['group']] = death * employee['lives'][i-1]
               
                
            
            #probability of quitting for actives only
            if employee["type"][i-1] == "active" or employee["type"][i-1] == "":
                args_ = tuple([employee["data"][z] for z in cols_res])
                
                resignation = law_resignation(*args_)#turnover(age)
                #resignation = turnover(age)
            else:
                resignation = 0
                
            n_resignation += resignation * employee['lives'][i-1]
            
            # departures by group
            if employee['data']['group'] in departures:
                departures[employee['data']['group']] += resignation * employee['lives'][i-1]
            else:
                departures[employee['data']['group']] = resignation * employee['lives'][i-1]
               
            # if the employee is active check if he will retire
            if employee["type"][i-1] == "active" or employee["type"][i-1] == "":
                args_ = tuple([employee["data"][z] for z in cols_ret])
                
                if law_retirement(*args_):
                    #update number of retired
                    n_retired += 1* employee['lives'][i-1]
                    new_retirees[i] = new_retirees[i] + [id]
                    
                    # departures by group
                    if employee['data']['group'] in departures:
                        departures[employee['data']['group']] += employee['lives'][i-1]
                    else:
                        departures[employee['data']['group']] = employee['lives'][i-1]
                    
                    #update type
                    employee["type"][i] = "retired"
                    
                    #update lives
                    employee["lives"][i] = employee["lives"][i-1] * survie * (1-resignation)
                    
                    #update deaths
                    employee["deaths"][i] = employee["lives"][i-1] * death
                    
                    #update number of new retirees
                    n_new_retirees[i] =  n_retired
                    
                    #if just retired we are done, but before update age
                    employee["data"]['age'] = employee["data"]['age'] + 1
                    continue
      
            #type remains the same as last year
            employee["type"][i] = employee["type"][i-1]
            
            #update lives
            employee["lives"][i] = employee["lives"][i-1] * survie * (1-resignation)
            
            #update deaths
            employee["deaths"][i] = employee["lives"][i-1] * death
            
            #update res
            employee["res"][i] = resignation* employee['lives'][i-1]
            
            #handling marriage
            if employee["data"]["familyStatus"] == "not married":
                args_ = tuple([employee["data"][z] for z in cols_mar])
                add_new_spouse(id, i, law_marriage(*args_))
                n_marriage += 1
                
            #update age of employee
            employee["data"]['age'] = employee["data"]['age'] + 1
            
        #projection of spouses
        for id, spouse in spouses_proj.items():
            
            # if new spouse continue (treate next year)
            if spouse['entrance'] > i:
                continue

            age = spouse["data"]['age']
            
            #probability of surviving
            survie = act.sfs_nPx(age,1, mortalityTable)
            
            #probability of dying
            death = act.sfs_nQx(age,1, mortalityTable)
            
            # the type of spouse is that of his related employee (but only if not widow)
            if spouse["type"][i-1] == "active" or spouse["type"][i-1] == "retired" or spouse["type"][i-1] == '':
                spouse["type"][i] = employees_proj[id[0]]["type"][i]
            else:
                spouse["type"][i] = "widow"
            
            #probability of quitting (probability that the related employee will quit
            if spouse["type"][i] == "active":
                # we have to recalculate resignation because employees_proj[id[0]]['res'][i] contains res of many employees (new recrutes)
                 args_ = tuple([employees_proj[id[0]]["data"][z] for z in cols_res])
                
                 resignation = law_resignation(*args_)
            else:
                resignation = 0
           
            #update lives
            spouse["lives"][i] = spouse["lives"][i-1] * survie * (1-resignation)
            
            #update deaths
            spouse["deaths"][i] = spouse["lives"][i-1] * death
            
            
            #handling births for active and retired only
            if spouse["data"]["type"] == "active" or spouse["data"]["type"] == "retired" :
                add_new_child(id[0],id[1], i)
            
            #update age of spouse
            spouse["data"]['age'] = spouse["data"]['age'] + 1
            
         
        #projection of children
        for id, child in children_proj.items():
            
            # if new child continue (treate next year)
            if child['entrance'] > i:
                continue
            
            #update age of children
            age = child["data"]['age']
            
            #probability of surviving
            survie = act.sfs_nPx(age,1, mortalityTable)
            
            #probability of dying
            death = act.sfs_nQx(age,1, mortalityTable)
            
            # the type of child is that of his related employee (but only if not widow)
            if child["type"][i-1] == "active" or child["type"][i-1] == "retired" or child["type"][i-1] == '':
                child["type"][i] = employees_proj[id[0]]["type"][i]
            else:
                child["type"][i] = "widow"
            
            #probability of quitting (probability that the related employee will quit)
            if child["type"][i] == "active":
                # we have to recalculate resignation because employees_proj[id[0]]['res'][i] contains res of many employees (new recrues)
                 args_ = tuple([employees_proj[id[0]]["data"][z] for z in cols_res])
                
                 resignation = law_resignation(*args_)
            else:
                resignation = 0
           
            #update lives
            child["lives"][i] = child["lives"][i-1] * survie * (1-resignation)
            
            #update deaths
            child["deaths"][i] = child["lives"][i-1] * death
            
            #update age of spouses
            child["data"]['age'] = child["data"]['age'] + 1 
            
        
        
        #total departures
        total_departures = n_retired + n_resignation + n_death
        #print('Year : ',i,'total_departures : ', total_departures)
        # departures by group
        #print('Year : ',i,' Departures by group : ', departures)
        
        
        # if law_replacement = None, replacement of departures 50% males, 50% females age 23 in each group
        if law_replacement_ == None:
#             for g in departures:
#                 add_new_employee('new_employee_year_males_' + str(i) + '_group_' + str(g) + '_male', i, 'male', 23, 0.5 * departures[g],g)
#                 add_new_employee('new_employee_year_males_' + str(i)  + '_group_'+ str(g) + '_female', i, 'female', 23, 0.5 * departures[g],g)
            x = 0
        else:
            new_emp = law_replacement_(departures, i) # new_emp is a list of dics having keys : sex, age, number and group
            for ne in new_emp:
                add_new_employee('new_employee_year_males_' + str(i) + '_group_' + str(ne['group']), i, ne['sex'], ne['age'], ne['number'],ne['group']) 
        
        #add_new_employee('new_employee_year_males_' + str(i), i, 'male', 23, total_departures,1)
        
    return  employees_proj, spouses_proj, children_proj, new_retirees, n_new_retirees
    
    
def globalNumbers(employees_proj_, spouses_proj_, children_proj_, MAX_YEARS):
    """ 
        Assumes parameters are of the form of those returned by simulerEffectif
  
        Parameters: 
            employees_proj_ (dic): a dic containing projected employees
            spouses_proj_ (dic): a dic containing projected spouses
            children_proj_ (dic): a dic containing projected children
          
        Returns: 
            DataFrame: A DataFrame containing global numbers by year : 
                       Actives, Retirees, Wives, Widows, Children 
    """
    
    
    # number of actives per year
    effectif_actifs = [0] * MAX_YEARS
    effectif_conjoints_actifs = [0] * MAX_YEARS
    effectif_enfants_actifs = [0] * MAX_YEARS

    # number of retired per year
    effectif_retraites = [0] * MAX_YEARS
    effectif_conjoints_retraites = [0] * MAX_YEARS
    effectif_enfants_retraites = [0] * MAX_YEARS

    # number of quitters per year
    effectif_demissions = [0] * MAX_YEARS

    # number of dying actives
    effectif_deces_actifs = [0] * MAX_YEARS
    effectif_deces_conjoints_actifs = [0] * MAX_YEARS
    effectif_deces_enfants_actifs = [0] * MAX_YEARS
    
    # number of dying retired
    effectif_deces_retraites = [0] * MAX_YEARS
    effectif_deces_conjoints_retraites = [0] * MAX_YEARS
    effectif_deces_enfants_retraites = [0] * MAX_YEARS

    # number of living widows
    effectif_ayants_cause = [0] * MAX_YEARS

    for i in range(MAX_YEARS):
        for a in employees_proj_.values():
            if a['type'][i] == 'active':
                effectif_actifs[i] = effectif_actifs[i] + a['lives'][i]
                effectif_deces_actifs[i] = effectif_deces_actifs[i] + a['deaths'][i]
            else:
                effectif_retraites[i] = effectif_retraites[i] + a['lives'][i]
                effectif_deces_retraites[i] = effectif_deces_retraites[i] + a['deaths'][i]
            
            effectif_demissions[i] = effectif_demissions[i] + a['res'][i]
        
        for a in spouses_proj_.values():
            if a['type'][i] == 'active':
                effectif_conjoints_actifs[i] = effectif_conjoints_actifs[i] + a['lives'][i]
                effectif_deces_conjoints_actifs[i] = effectif_deces_conjoints_actifs[i] + a['deaths'][i]
                
            if a['type'][i] == 'retired':
                effectif_conjoints_retraites[i] = effectif_conjoints_retraites[i] + a['lives'][i]
                effectif_deces_conjoints_retraites[i] = effectif_deces_conjoints_retraites[i] + a['deaths'][i]
                
            if a['type'][i] == 'widow':
                effectif_ayants_cause[i] = effectif_ayants_cause[i] + a['lives'][i]
                
        for a in children_proj_.values():
            if a['type'][i] == 'active':
                effectif_enfants_actifs[i] = effectif_enfants_actifs[i] + a['lives'][i]
                effectif_deces_enfants_actifs[i] = effectif_deces_enfants_actifs[i] + a['deaths'][i]
                
            if a['type'][i] == 'retired':
                effectif_enfants_retraites[i] = effectif_enfants_retraites[i] + a['lives'][i]
                effectif_deces_enfants_retraites[i] = effectif_deces_enfants_retraites[i] + a['deaths'][i]
            
    # construct DataFrame of projected numbers
    totalEmployees = [sum(x) for x in zip(effectif_actifs, effectif_retraites)]
    totalSpouses = [sum(x) for x in zip(effectif_conjoints_actifs, effectif_conjoints_retraites)]
    totalChildren = [sum(x) for x in zip(effectif_enfants_actifs, effectif_enfants_retraites)]

    Data = {'Year':list(range(MAX_YEARS)), 'effectif_actifs' : effectif_actifs, 'effectif_retraites' : effectif_retraites, 'Total Employees' : totalEmployees,
            'effectif_ayants_cause' : effectif_ayants_cause, 'effectif_conjoints_actifs' : effectif_conjoints_actifs,
            'effectif_conjoints_retraites' : effectif_conjoints_retraites, 'Total Spouses' : totalSpouses, 'effectif_enfants_actifs' : effectif_enfants_actifs,
            'effectif_enfants_retraites' : effectif_enfants_retraites, 'Total Children' : totalChildren}

    Effectifs = pd.DataFrame(data=Data,
                columns=['Year', 'effectif_actifs', 'effectif_retraites', 'Total Employees' , 'effectif_ayants_cause',
                         'effectif_conjoints_actifs', 'effectif_conjoints_retraites', 'Total Spouses', 'effectif_enfants_actifs', 'effectif_enfants_retraites', 'Total Children' ]) 
    return Effectifs
    
    

def leavingNumbers(employees_proj_, n_new_retirees_, MAX_YEARS):
    """ 
        Assumes parameter employees_proj_ is of the form of that returned by simulerEffectif
  
        Parameters: 
            employees_proj_ (dic): a dic containing projected employees
            n_new_retirees_ (list) : number of new retired per year
        Returns: 
            DataFrame: A DataFrame containing global numbers leaving population of employees by year : 
                       deaths, resignation, new retirees 
    """
    
    # number of quitters (resignations) per year
    effectif_demissions = [0] * MAX_YEARS
    
    # number of dying actives per year
    effectif_deces_actifs = [0] * MAX_YEARS
    
    for i in range(MAX_YEARS):
        for a in employees_proj_.values():
            if a['type'][i] == 'active':
                effectif_deces_actifs[i] = effectif_deces_actifs[i] + a['deaths'][i]
            
            effectif_demissions[i] = effectif_demissions[i] + a['res'][i]
    
    
    
    #construct DataFrame of projected numbers leaving the pop : deaths, resignations and new retirees
    totalLeaving = [sum(x) for x in zip(effectif_deces_actifs, effectif_demissions, n_new_retirees_ )]
    
    Data = {'Year':list(range(MAX_YEARS)),'effectif_deces_actifs' : effectif_deces_actifs, 'effectif_demissions' : effectif_demissions, 
            'new_retirees' : n_new_retirees_, 'Total Living' : totalLeaving}

    Leaving = pd.DataFrame(data=Data, 
            columns=['Year', 'effectif_deces_actifs', 'effectif_demissions', 'new_retirees' , 'Total Living'])
    
    return Leaving
    

    
    
    

    


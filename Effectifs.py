
"""
Created on Mon May  7 14:08:56 2018

@author: a.teffal
"""
#%%

import random
import pandas as pd
import Actuariat as act
import Retraite as ret
from nbconvert.exporters.base import export
from _ast import arg



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

def simulerEffectif(employees, spouses, children, mortalityTable = 'TV 88-90', MAX_YEARS = 50, law_retirement_ = None, 
                    law_resignation_ = None, law_marriage_ = None, law_birth_ = None):
    
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
        law_retirement = law_retirement_[0]
        cols_ret = law_retirement_[1]
        
    #setting law of resignation
    if law_resignation_ == None:
        law_resignation = turnover
        cols_res = ['age']
    else:
        law_resignation = law_resignation_[0]
        cols_res = law_resignation_[1]
        
    #setting law of marriage
    if law_marriage_ == None:
        law_marriage = probaMariage
        cols_mar = ['age', 'type']
    else:
        law_marriage = law_marriage_[0]
        cols_mar = law_marriage_[1]
        
    
    #setting law of birth
    if law_birth_ == None:
        law_birth = probaNaissance
        cols_birth = ['age']
    else:
        law_birth = law_birth_[0]
        cols_birth = law_birth_[1]
        
    
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

    def add_new_employee(id, year_, sex_, age_, ponderation):
        """Adds a new employee in the employees_proj dic.
        
        Args:
        id: The id of the employee to be added (key of the dic).
        year_: year of projection when this employee is added : 1, 2,...
        sex_ : sex of the employee
        age : age at of the employee at year year_
        ponderation : if 0.5 for example,add 50% of an employee. This is used to handle 'rate' of replacement 

        """
        employees_proj[id] = {'data':dict(zip(['type','sex', 'familyStatus','age', 'Year_employment'],['active',sex_, 'not married',age_, 2017 + year_  ])), 'exist':0, 
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
                
            
            #probability of quitting for actives only
            if employee["type"][i-1] == "active" or employee["type"][i-1] == "":
                args_ = tuple([employee["data"][z] for z in cols_res])
                
                resignation = law_resignation(*args_)#turnover(age)
                #resignation = turnover(age)
            else:
                resignation = 0
                
            n_resignation += resignation * employee['lives'][i-1]
               
            # if the employee is active check if he will retire
            if employee["type"][i-1] == "active" or employee["type"][i-1] == "":
                args_ = tuple([employee["data"][z] for z in cols_ret])
                #print(args_)
                
                if law_retirement(*args_):
                    #update number of retired
                    n_retired += 1* employee['lives'][i-1]
                    new_retirees[i] = new_retirees[i] + [id]
                    
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
        print('Year : ',i,'total_departures : ', total_departures)
        
        #Replacement of this departures 50% males, 50% females
        add_new_employee('new_employee_year_males_' + str(i), i, 'male', 30, 1 * total_departures)
        
        
    return  employees_proj, spouses_proj, children_proj, new_retirees, n_new_retirees
    
    
    
    
    
    
    
    
    

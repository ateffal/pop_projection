
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
            return 0.0950338528553041
        else :
            return 0
    else:
        return 0



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

def simulerEffectif(employees, spouses, children, mortalityTable = 'TV 88-90', MAX_YEARS = 50, law_retirement_ = None):
    
    ''' assumes employees, spouses and children are pandas dataframes with at least 5 columns :
        - id   : an unique identifier of the employee
        - type : active or retired for employees. active, or retired or widow or widower for spouses and children.
                 for spouses and children, type is the type of the employee taht they are attached to if it's still alive, or widows or widower otherwise
        - sex
        - familyStatus : maried, or not maried
        - age
        
        if supplied, law_retirement is a tuple : (a function, list of columns of employees to be passed to this function )
    '''
    
    if law_retirement_ == None:
        law_retirement = ret.retire
        cols = ['age']
    else:
        law_retirement = law_retirement_[0]
        cols = law_retirement_[1]
        
    
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
            'entrance':0, 'lives':[1] + [0]*(MAX_YEARS-1), 'deaths' : [0]*MAX_YEARS}
        
    # dic where to store retired of each year : {year : [list of employees that retired that year (their ids)] }
    new_retired = dict(zip([i for i in range(1, MAX_YEARS)],list([[]]*(MAX_YEARS - 1))))

    def add_new_employee(id, data, entrance, type_):
        employees_proj[id] = {'data':data, 'exist':1, 'entrance':entrance, 'lives':[0]*MAX_YEARS, 
                'deaths' : [0]*MAX_YEARS, 'res':[0]*MAX_YEARS, 'type':['']*MAX_YEARS}
        employees_proj[id]['lives'][entrance] = 1
        employees_proj[id]['type'][entrance] = type_
        
    def add_new_spouse(employee_id, year_):
        #global employees_proj
        #global spouses_proj
        
        # sex
        if employees_proj[employee_id]["data"]["sex"] == 'male':
            sex_temp = 'female'
        else:
            sex_temp = 'male'
            
        #live employee (employee will marry only if still alive)
        live_emp = employees_proj[employee_id]["lives"][year_]
        
        #age
        if sex_temp == 'female':
            age_temp = employees_proj[employee_id]["data"]["age"] - 5 
        else:
            age_temp = employees_proj[employee_id]["data"]["age"] + 5
        
        #type
        type_temp = employees_proj[employee_id]["type"][i]
        
        spouses_proj[(employee_id, 1)] = {'data':dict(zip(['sex', 'age', 'type', 'familyStatus'],[sex_temp, age_temp, type_temp,'married'])), 'exist':1, 
            'entrance':(year_+1), 'lives':[0] * year_ + [live_emp] + [0] * (MAX_YEARS- year_ - 1), 'deaths' : [0]*MAX_YEARS, 
            'type':[''] * year_ + [type_temp] + [''] * (MAX_YEARS- year_ - 1)}
        
        #print(spouses_proj[(employee_id, 1)])
        
        
    
    # main loop
    for i in range(1, MAX_YEARS):
        # employees
        n_retired = 0
        n_death = 0
        n_resignation = 0
        n_marriage = 0
        
        #projection of employees
        for id, employee in employees_proj.items():
               
            #update age of employee
            employee["data"]['age'] = employee["data"]['age'] + 1
            age = employee["data"]['age']
            
            #probability of surviving
            survie = act.sfs_nPx(age,1, mortalityTable)
            
            #probability of dying
            death = act.sfs_nQx(age,1, mortalityTable)
            
            #probability of quitting for actives only
            if employee["type"][i-1] == "active":
                resignation = turnover(age)
            else:
                resignation = 0
               
            # if the employee is active check if he will retire
            if employee["type"][i-1] == "active":
                args_ = tuple([employee["data"][z] for z in cols])
                #print(args_)
                
                if law_retirement(*args_):
                    #update number of retired
                    n_retired += 1
                    new_retired[i] = new_retired[i] + [id]
                    
                    #update type
                    employee["type"][i] = "retired"
                    
                    #update lives
                    employee["lives"][i] = employee["lives"][i-1] * survie * (1-resignation)
                    
                    #update deaths
                    employee["deaths"][i] = employee["lives"][i-1] * death
                    
                    
                    #if just retired we are done
                    continue
      
            #type remains the same as last year
            employee["type"][i] = employee["type"][i-1]
            
            #update lives
            employee["lives"][i] = employee["lives"][i-1] * survie * (1-resignation)
            
            #update deaths
            employee["deaths"][i] = employee["lives"][i-1] * death
            
            #update res
            employee["res"][i] = resignation
            
            #handling mariage
            if employee["data"]["familyStatus"] == "not married":
                if willMarry(age, employee["type"][i]):
                    employee["data"]["familyStatus"] = "married"
                    n_marriage += 1
                    # Add new spouse
                    add_new_spouse(id, i)
            
            
        #projection of spouses
        for id, spouse in spouses_proj.items():
            
            # if new spouse continue (treate next year)
            if spouse['entrance'] > i:
                continue
            
            #update age of spouses
            spouse["data"]['age'] = spouse["data"]['age'] + 1
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
                resignation = employees_proj[id[0]]['res'][i]
            else:
                resignation = 0
           
            #update lives
            spouse["lives"][i] = spouse["lives"][i-1] * survie * (1-resignation)
            
            #update deaths
            spouse["deaths"][i] = spouse["lives"][i-1] * death
            
            
        #print(n_retired)
        #print("mariages de l'annee : ", n_marriage)
    
#     print('lenth of spouses_proj at the end : ', len(spouses_proj))
#     for s in spouses_proj:
#         print(spouses_proj[s])
        
    return  employees_proj, spouses_proj, children_proj, new_retired
    
    
    

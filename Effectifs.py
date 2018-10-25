
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

def simulerEffectif(employees, spouses, children, mortalityTable = 'TV 88-90', MAX_YEARS = 50, law_retirement_ = None, law_resignation_ = None):
    
    ''' assumes employees, spouses and children are pandas dataframes with at least 5 columns :
        - id   : an unique identifier of the employee
        - type : active or retired for employees. active, or retired or widow or widower for spouses and children.
                 for spouses and children, type is the type of the employee taht they are attached to if it's still alive, or widower otherwise
        - sex
        - familyStatus : maried, or not maried
        - age
        
        if supplied, law_retirement_ is a tuple : (a function, list of columns of employees to be passed to this function )
        if supplied, law_resignation_ is a tuple : (a function, list of columns of employees to be passed to this function )
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
        law_resignation_ = law_resignation_[0]
        cols_res = law_resignation_[1]
        
    
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
        
    def add_new_spouse(employee_id, year_):
        """Adds a new spouse in the spouses_proj dic.
        
        Args:
        employee_id: The id of the employee attached to this spouse.
        year_: year of projection when this spouse is added : 1, 2,...
        entrance : year of entrance

        """
        
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
            employee["res"][i] = resignation* employee['lives'][i-1]
            
            #handling mariage
            if employee["data"]["familyStatus"] == "not married":
                if willMarry(age, employee["type"][i]):
                    employee["data"]["familyStatus"] = "married"
                    n_marriage += 1
                    # Add new spouse
                    add_new_spouse(id, i)
            
            #update age of employee
            employee["data"]['age'] = employee["data"]['age'] + 1
            
        #projection of spouses
        for id, spouse in spouses_proj.items():
            
            # if new spouse continue (treate next year)
            if spouse['entrance'] > i:
                continue
            
            #update age of spouses
            #spouse["data"]['age'] = spouse["data"]['age'] + 1
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
                # we have to recalculate resignation because employees_proj[id[0]]['res'][i] contains res of many employees (new recrues)
                 args_ = tuple([employees_proj[id[0]]["data"][z] for z in cols_res])
                
                 resignation = law_resignation(*args_)
                
                 #resignation = employees_proj[id[0]]['res'][i]
            else:
                resignation = 0
           
            #update lives
            spouse["lives"][i] = spouse["lives"][i-1] * survie * (1-resignation)
            
            #update deaths
            spouse["deaths"][i] = spouse["lives"][i-1] * death
            
            #update age of spouses
            spouse["data"]['age'] = spouse["data"]['age'] + 1
            
            
        print('Year : ',i,' Retired :', n_retired, ' Deaths : ', n_death, ' Resignation : ', n_resignation, ' Total : ', (n_retired+n_death+n_resignation))
        
        #total departures
        total_departures = n_retired + n_resignation + n_death
        
        #Replacement of this departures 50% males, 50% females
        add_new_employee('new_employee_year_males_' + str(i), i, 'male', 40, total_departures)
        
        #add_new_employee('new_employee_year_females_' + str(i), i, 'female', 30, 0.6*total_departures)
        
        
        #print("mariages de l'annee : ", n_marriage)
    
#     print('lenth of spouses_proj at the end : ', len(spouses_proj))
#     for s in spouses_proj:
#         print(spouses_proj[s])
        
    return  employees_proj, spouses_proj, children_proj, new_retired
    
    
    

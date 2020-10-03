

def projectGroups(employees, spouses=None, children=None, mortalityTable = 'TV 88-90', MAX_YEARS = 50, law_retirement_ = None, 
                    law_resignation_ = None, law_marriage_ = None, age_diff = 5, law_birth_ = None,  law_replacement_ =  None):
    
    """ Main function that project population of a retirement plan (employees their spouses and their children) given laws of :
        mortality, retirement, resignation, marriage, birth and replacement.

    assumes employees, spouses and children are pandas dataframes with at least 6 columns :
        - id   : an unique identifier of the employee
        - type : active or retired for employees. active, or retired or widow or widower for spouses and children.
                 for spouses and children, type is the type of the employee that they are attached to 
                 if it's still alive, or widower otherwise.
        - sex  : male or female
        - familyStatus : married, or not married
        - age
        - group (optional) : a sub-population. ex : group of employees recruted before 2002, group of directors,...

    Parameters
    ----------
    employees : pandas dataframe
                dataframe of employees having at least columns: id, type, sexe, familyStatus, age and group (optional).
    spouses   : pandas dataframe
                dataframe of spouses having at least columns : id, type, sexe, familyStatus and age.
    children   : pandas dataframe
                dataframe of children having at least columns : id, type, sexe, familyStatus and age.
    mortalityTable : string
                name of the mortality table. 
                View existing mortality tables with Actuariat.mortality_tables.
                Add a mortality table with Actuariat.add_mortality_table

    MAX_YEARS  : int
                number of years of projection
    law_retirement_ : function or tuple
                    a function returning a boolean (the employee will retire yes or no), or a 
                    tuple : (function, liste of it's parameters that have same name in the employees data frame)
    law_resignation_ : function or tuple
                    a function returning a number between 0 and 1 (probability that the employee will resign next year), or a 
                    tuple : (function, liste of it's parameters that have same name in the employees data frame)
    law_marriage_ : function or tuple
                    a function returning a number between 0 and 1 (probability that the employee will marry next year), or a 
                    tuple : (function, liste of it's parameters that have same name in the employees data frame)
    age_diff (int) : Age difference between male and female for new marriages
    marriage_periode : list. A sub-list of ['active', 'retired']. Types to which apply law of marriage.
    law_birth_ : function or tuple
                a function returning a number between 0 and 1 (probability that the employee (or spouse)  
                will  give birth next year), or a  tuple : (function, liste of it's parameters 
                that have same name in the employees or spouses data frame)
    birth_periode : list. A sub-list of ['active', 'retired']. Types to which apply law of birth.
    law_replacement_ : function
                    function having parameters :
                    - departures_ : a dic storing number of departures by group of the year year_
                    - year_ : year of projection
                    this function returns a list of employees to add to population. Each
                    employee in this list is a dic with keys : 'key' (to uniquely define the employee), 
                    'number' and 'data' (list of values that corresponds to columns in employee except id)
    
    Returns
    -------
    tuple
        a tuple of projected population as dics: 
        - projected employees, a dic with key id and value is a dic with keys: data, exist, entrance, lives, deaths, res, type.
        - projected spouses, a dic with key (id, rang) and value is a dic with keys : data, exist, entrance, lives, deaths, type.
        - projected children, a dic with key (id, rang) and value is a dic with keys : data, exist, entrance, lives, deaths, type.
        - new retirees a dic : {year : [list of employees that retired that year (their ids)] }
        - n_new_retirees a list storing number of retirees for each year 
    """

    # if group doesn't exist in employees create it and set it to be id
    if not 'group' in list(employees):
        employees['group'] = employees['id']

    #setting law of retirement
    if law_retirement_ == None:
        law_retirement = retire
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
        law_resignation = turnover0
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
        law_marriage = probaMariage0
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
        law_birth = probaNaissance0
        cols_birth = ['age']
    else:
        law_birth = law_birth_[0] if type(law_birth_) is tuple else law_birth_
        cols_birth = law_birth_[1] if type(law_birth_) is tuple else inspect.getfullargspec(law_birth)[0]
        
    # verify that columns exist in dataframe
    unfound_cols = verifyCols(spouses, cols_birth)
    if len(unfound_cols) > 0:
        print('Unfound columns in spouses : ', unfound_cols)
        return None
    
    # initialization of projected employees, spouses and children
    employees_proj = tools.init_employees_proj(employees, MAX_YEARS)
    spouses_proj = tools.init_spouses_proj(spouses, MAX_YEARS)
    children_proj = tools.init_children_proj(children, MAX_YEARS)
        
    # main loop
    for i in range(1, MAX_YEARS):
        # employees
        n_retired = 0.0
        n_death = 0.0
        n_resignation = 0.0
        n_marriage = 0.0
        departures = {} # a dic storing the number of departures for a group each year
        
        #projection of employees
        for id_e, employee in employees_proj.items():
               
            #age of employee
            age = employee["data"]['age']

            #probability of quitting (for actives only)
            if employee["type"][i-1] == "active" or employee["type"][i-1] == "":
                args_ = tuple([employee["data"][z] for z in cols_res])
                
                resignation = law_resignation(*args_) #turnover(age)
            else:
                resignation = 0
            
            #probability of dying
            death = act.sfs_nQx(age,1, mortalityTable)

            # retirement
            if employee["type"][i-1] == "active" or employee["type"][i-1] == "":
                if not 'year_proj' in cols_ret:
                    args_ = tuple([employee["data"][z] for z in cols_ret])
                else:
                    args_ = tuple([employee["data"][z] for z in cols_ret[:-1]]) + (i,)
            retirement = law_retirement(*args_)

            if retirement:
                #update number of retired
                n_retired += employee['lives'][i-1] * survie * (1-resignation) # was 1* employee['lives'][i-1]
                new_retirees[i] = new_retirees[i] + [id_e]  # add id of the employee to the list
                    
                # departures by group
                if employee['data']['group'] in departures:
                    departures[employee['data']['group']] += employee['lives'][i-1]*(1-death)*(1-resignation)
                else:
                    departures[employee['data']['group']] = employee['lives'][i-1]*(1-death)*(1-resignation)
                
                #update type
                employee["type"][i] = "retired"


            # number of deaths
            employee["deaths"][i] = employee["numbers"][i-1] * death * (1-resignation)

            if employee["type"][i-1] == "active":
                n_death += employee["deaths"][i]
                # departure by group
                if employee['data']['group'] in departures:
                    departures[employee['data']['group']] += employee["deaths"][i]
                else:
                    departures[employee['data']['group']] = employee["deaths"][i]
               
            
                
            n_resignation += resignation * employee['lives'][i-1]
            
            # departures by group
            if employee['data']['group'] in departures:
                departures[employee['data']['group']] += resignation * employee['lives'][i-1]*(1-death)
            else:
                departures[employee['data']['group']] = resignation * employee['lives'][i-1]*(1-death)
               
            
            #type remains the same as last year
            employee["type"][i] = employee["type"][i-1]
            
            #update lives
            employee["lives"][i] = employee["lives"][i-1] * survie * (1-resignation)
            
            #update deaths
            employee["deaths"][i] = employee["lives"][i-1] * death * (1-resignation) # was employee["lives"][i-1] * death
            
            #update res
            employee["res"][i] = resignation* employee['lives'][i-1]
            
            #handling marriage
            if employee["type"][i] in marriage_periode:
                if employee["data"]["familyStatus"] == "not married" : 
                    args_ = tuple([employee["data"][z] for z in cols_mar])
                    prob_mar = law_marriage(*args_)  # if equals 1 set familyStatus of employee to married
                    add_new_spouse(id_e, i, law_marriage(*args_))
                    n_marriage += 1
                    if prob_mar==1:
                        employee["data"]["familyStatus"] = "married"

            #update age of employee
            employee["data"]['age'] = employee["data"]['age'] + 1
        
        
    return employees_proj, spouses_proj, children_proj, new_retirees, n_new_retirees
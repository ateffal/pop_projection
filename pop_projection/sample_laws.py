"""
Created on 2019

@author: a.teffal

"""

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
	
	
	
def law_mar1(age, sex, type):
    """
    Return the probability of getting maried  during the following year at a given age for a given sex

    """
    if sex == 'male':
        if type=='active':
            if age >= 25 and age <= 54:
                return 0.1
            else :
                return 0
        else:
            return 0
    
    if sex == 'female':
        if type=='active':
            if age >= 25 and age <= 54:
                return 0.15
            else :
                return 0
        else:
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



def loi_naiss_2(age):
    
    taux = [0.17,0.44,0.94,1.90,2.89,4.00,5.27,6.80,8.72,10.82,12.61,13.88,14.23,13.76,12.76,
            11.50,10.01,8.36,7.06,5.93,4.89,3.74,2.97,2.23,1.63,1.10,0.71,0.41,0.22,0.12,0.05,0.02,0.01,0.01,0.00]

    taux = [i/100 for i in taux]

    if age > 49 or age < 15:
        return 0
    else:
        return taux[age-15]
"""
Created on 2018

@author: a.teffal

"""

import numpy as np
from datetime import date


#%%
TD_73_77 = np.array([100000, 98471, 98360, 98281, 98220, 98167, 98120, 98076, 98035, 97997,
            97961, 97927, 97892, 97855, 97814, 97761, 97691, 97594, 97460, 97290,
            97105, 96921, 96745, 96576, 96419, 96270, 96127, 95988, 95849, 95707,
            95559, 95406, 95251, 95092, 94921, 94734, 94533, 94316, 94076, 93810,
            93516, 93192, 92836, 92440, 91996, 91503, 90966, 90391, 89772, 89103,
            88380, 87605, 86778, 85893, 84938, 83909, 82812, 81654, 80435, 79146,
            77772, 76296, 74706, 73007, 71208, 69302, 67276, 65127, 62855, 60473,
            57981, 55369, 52642, 49815, 46887, 43872, 40798, 37688, 34560, 31441,
            28364, 25351, 22424, 19602, 16916, 14398, 12063, 9938, 8054, 6407,
            4986, 3790, 2819, 2059, 1481, 1048, 728, 497, 333, 218, 103, 46, 19,
            7, 3, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])


TD_90_92 = np.array([100000, 99179, 99110, 99066, 99034, 99008, 98983, 98961, 98942, 98923,
            98905, 98886,98865,98843,98820,98788,98746,98688,98610,98500,98375,98242,
            98095, 97944, 97795, 97643, 97488, 97330, 97170, 97004, 96833, 96655,
            96469, 96283, 96093, 95892, 95678, 95454, 95221, 94971, 94704, 94420,
            94118, 93800, 93450, 93069, 92663, 92227, 91761, 91270, 90740, 90169,
            89552, 88882, 88154, 87364,86509,85597, 84624, 83570, 82432, 81204,
            79886, 78485, 77012, 75476, 73877, 72204, 70412, 68547, 66599, 64558,
            62369, 60061, 57622, 55075, 52392, 49620, 46736, 43738, 40644, 37468,
            34167, 30874, 27552, 24302, 21181, 18203, 15385, 12762, 10394, 8316,
            6507, 4941, 3662, 2654, 1882, 1302, 884, 594, 430, 280,182, 116,72,
            43, 24, 13, 7, 3, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0,0])

TV_88_90 = np.array([100000, 99352, 99294, 99261, 99236, 99214, 99194, 99177, 99161, 99145,
            99129, 99112, 99096, 99081, 99062, 99041, 99018, 98989, 98955, 98913,
            98869, 98823, 98778, 98734, 98689, 98640, 98590, 98537, 98482, 98428,
            98371, 98310, 98247, 98182, 98111, 98031, 97942, 97851, 97753, 97648,
            97534, 97413, 97282, 97138, 96981, 96810, 96622, 96424, 96218, 95995,
            95752, 95488, 95202, 94892, 94560, 94215, 93848, 93447, 93014, 92545,
            92050, 91523, 90954, 90343, 89687, 88978, 88226, 87409, 86513, 85522,
            84440, 83251, 81936, 80484, 78880, 77104, 75136, 72981, 70597, 67962,
            65043, 61852, 58379, 54614, 50625, 46455, 42130, 37738, 33340, 28980,
            24739, 20704, 16959, 13580, 10636, 8118, 6057, 4378, 3096, 2184, 1479,
            961, 599, 358, 205, 113, 59, 30, 14, 6, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
            
USA_2009 = np.array([100000,99363,99322,99295,99274,99259,99244,99230,99218,99207,99198,99189,
            99180,99167,99148,99121,99084,99039,98986,98925,98857,98780,98697,98608,98516,
            98424,98332,98240,98148,98053,97957,97857,97754,97647,97536,97419,97297,97167,
            97029,96881,96722,96550,96364,96160,95936,95690,95422,95133,94819,94477,94103,93695,
            93252,92775,92265,91723,91147,90534,89881,89184,88439,87645,86797,85893,84928,83895,
            82784,81587,80302,78930,77474,75926,74276,72517,70634,68621,66485,64224,61823,59272,
            56572,53736,50775,47676,44448,41112,37648,34120,30569,27044,23595,20275,17135,14223,
            11578,9228,7192,5471,4058,2929,2056,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
])

#%%
mortality_tables = {'TD 73-77':TD_73_77, 'TD 90-92':TD_90_92, 'TV 88-90':TV_88_90, 'Sans':[1]*121, 'USA_2009' : USA_2009}

def add_mortality_table(Nom, lx):
    if len(lx) > 121:
        print('La longuer de lx doit être inférieure ou égale à 121')
        return False
    n = len(lx)
    for i in range(n-1):
        if lx[i+1] > lx[i]:
            print("Error : ","lx[%d] > lx[%d]"%(i+1,i))
            return False

    temp=[0]*121
    
    for i in range(n):
        temp[i]=lx[i]
    
    mortality_tables[Nom] = temp
    print('Mortality table ', Nom, ' added successfully.')
#%%

def sfs_lx(Age, Table):

    if Age > 120:
        return 0
    if Age < 0:
        raise NameError('Age invalide !')
    if Table not in mortality_tables:
        raise NameError('Table introuvable !')
    return mortality_tables[Table][Age]

#%%

def sfs_nPx(Age, n, Table):
    l1 = sfs_lx(Age + n, Table)
    l2 = sfs_lx(Age, Table)
    if l2 != 0:
        return sfs_lx(Age + n, Table) / sfs_lx(Age, Table)
    else:
        return 0
        
    


#%%

def sfs_nQx(Age, n, Table):

    if sfs_lx(Age, Table) != 0:
        return (1 - sfs_lx(Age + n, Table) / sfs_lx(Age, Table))
    else:
        return 1

#%%


def dateDepart(dDate):

    '''
        Retourne le debut de semestre qui suit immediatement
        la date donnee en parametre.
    '''
    # Si Date de départ = 1/1/N alors sortie le 1/1/N*/
    if dDate.day == 1 and dDate.month == 1 :
        return date(dDate.year,1,1)

    # Si Date de départ = 1/7/N alors sortie le 1/7/N*/
    if dDate.day == 1 and dDate.month == 7 :
        return date(dDate.year,7,1)

    if dDate.month <= 6 :
       return date(dDate.year,7,1)
    else :
        return date(dDate.year + 1, 1, 1)

#%%
#
def dateDepartEffective(dDateNaissance, dDateEngagement, nAgeDepartAv2002 = 55, nAgeDepartAp2002 = 60) :

    '''
        Retourne la date de retraite theorique ( age de retraite)
    '''

    # Calcul de la date de départ théorique
    date2002 = date(2002 ,1,1)

    if (dDateEngagement - date2002).days <= 0 :
        dDateDepartTheorique = date(dDateNaissance.year + nAgeDepartAv2002, dDateNaissance.month, dDateNaissance.day)
    else:
        dDateDepartTheorique = date(dDateNaissance.year + nAgeDepartAp2002, dDateNaissance.month, dDateNaissance.day)

    # Calcul de la date de départ effective
    return dateDepart(dDateDepartTheorique)


#%%










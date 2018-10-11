# -*- coding: utf-8 -*-
"""
Created on Wed May  2 08:59:26 2018

@author: a.teffal
"""
#%%
import datetime

#%%
def sfs_PensionMinimale(dDateEngagement, dPensionCategorielle, PensionTh):
    a_2002 = datetime.date(2002,1,1)
    a_1995 = datetime.date(1995,1,1)
    if (dDateEngagement-a_2002).days < 0:
        if (dDateEngagement - a_1995).days >= 0:
            return  max(dPensionCategorielle, PensionTh / 2)
        else:
            return min(dPensionCategorielle, PensionTh / 2)
        
    else:
        return PensionTh
    
#%%  
def sfs_PensionCategorielle(Strate):
    if Strate in [1,2]:
        return 18000
    if Strate in [3,4]:
        return 24000
    if Strate in [5,6]:
        return 30000
    if Strate in range(7,12):
        return 36000
    return None

#%%
def sfs_DateDepart(dDate):
    # Si Date de départ = 1/1/N alors sortie le 1/1/N
    if dDate.day == 1 and dDate.month == 1:
        return datetime.date(dDate.year, 1, 1)
    
    
    # Si Date de départ = 1/7/N alors sortie le 1/7/N
    if dDate.day == 1 and dDate.month == 7:
        return datetime.date(dDate.year, 7, 1)
    
    if dDate.month <= 6:
        return datetime.date(dDate.year, 7, 1)
    else:
        return datetime.date(dDate.year + 1, 1, 1)
    


#%%
def sfs_DateDepartEffective(dDateNaissance, dDateEngagement):
    # Ceci sert a gerer le probleme de fevrier lors de depart a 55 ans car 55 ans n'est pas divisible par 4
    # Jour et mois de naissance a utiliser pour la date de depart
    if dDateNaissance.day == 29 and dDateNaissance.month == 2:
        jour_dep = 1
        mois_dep = 3
    else:
        jour_dep = dDateNaissance.day
        mois_dep = dDateNaissance.month
    
    # Calcul de la date de départ théorique
    a_2002 = datetime.date(2002,1,1)
    if (dDateEngagement - a_2002).days < 0:
        dsfs_DateDepartTheorique = datetime.date(dDateNaissance.year+55, mois_dep, jour_dep)
    else:
        dsfs_DateDepartTheorique = datetime.date(dDateNaissance.year+60, dDateNaissance.month, dDateNaissance.day)
   
    # Calcul de la date de départ effective
    return sfs_DateDepart(dsfs_DateDepartTheorique)



#%%

def sfs_CalcAnciennete(DateEngagement, DateCalcul, AnnuitesMax = 35):
    return min((DateCalcul-DateEngagement).days / 365.25, AnnuitesMax)

#%%

def CalculSalaireMoyen(SalaireN, SalaireN_1, SalaireN_2,TauxEvolSalaire = 0.035, NbAnnees = 0):
    if NbAnnees == 0:
        if SalaireN_1 != -1 and SalaireN_2 != -1:
            return (SalaireN + SalaireN_1 + SalaireN_2) / 3
        else:
            if SalaireN_1 != -1:
               return (SalaireN + SalaireN_1 + SalaireN_1 / (1 + TauxEvolSalaire)) / 3
            else:
               return (SalaireN + SalaireN / (1 + TauxEvolSalaire) + SalaireN / (1 + TauxEvolSalaire) ** 2) / 3
    else:
        temp = 0
        for i in range(0,NbAnnees):
            temp = temp + SalaireN / (1 + TauxEvolSalaire) ** i
        return temp / NbAnnees


#%%

def sfs_PensionTheorique(dDateEngagement, dDateNaissance, SalaireActuel, dDateCalcul, TauxEvolutionSalaire = 0.035, TauxLiquidation = 0.025, NombreAnneesSalaireMoyenCRP = 3):
    # Calcul de l'ancienneté et mois de depart
    dDateProjection = sfs_DateDepartEffective(dDateNaissance, dDateEngagement)
    Anciennete = sfs_CalcAnciennete(dDateEngagement, dDateProjection)
    nMoisDepart_ = dDateProjection.month
    
    # Calcul de NbAnnees
    if nMoisDepart_ == 7:
        NbAnnees = ((dDateProjection-dDateCalcul).days / 365.25) + 1
    else:
        NbAnnees = ((dDateProjection-dDateCalcul).days / 365.25)
    
    SalaireProjete = SalaireActuel * ((1 + TauxEvolutionSalaire)**NbAnnees)
    SalaireMoyenProjete = CalculSalaireMoyen(SalaireProjete, -1, -1, TauxEvolutionSalaire, NombreAnneesSalaireMoyenCRP)
    
    return TauxLiquidation * Anciennete * SalaireMoyenProjete


#%%

def sfs_CalcAgeAdherent(DateNaissance, DateCalcul):
    return (DateCalcul-DateNaissance).days / 365.25

#%%

def sfs_CapitalTheorique(dDateEngagement, PensionTheorique, PensionMinimale,SIRP):
    if (dDateEngagement - datetime.date(2002, 1, 1)).days < 0:
        if PensionTheorique >= PensionMinimale and PensionTheorique != 0:
            return 10 * (PensionTheorique - PensionMinimale) + SIRP * (PensionTheorique - PensionMinimale) / PensionTheorique
        else:
            return 0
    else:
        return 0

#%%

def sfs_SalaireFinal(SalaireActuel, dDateCalcul, dDateDepart, TauxEvolutionSalaire = 0.035, nMoisDepart_ = 1):

    NbAnnees = 0
    
    if nMoisDepart_ != 1 and nMoisDepart_ != 7:
        nMoisDepart_ = 1

    # Calcul du nombre d'années selon le mois de sortie
    if nMoisDepart_ == 7:
        NbAnnees = int((dDateDepart - dDateCalcul).days / 365.25) + 1
    else:
        NbAnnees = int((dDateDepart - dDateCalcul).days / 365.25)

    return SalaireActuel * (1 + TauxEvolutionSalaire) ** NbAnnees
    

#%%

def sfs_SalaireFinalMoyen(SalaireActuel, dDateCalcul, dDateDepart, TauxEvolutionSalaire = 0.035, nMoisDepart_ = 1, NbAnnees = 3):
 
    sf = sfs_SalaireFinal(SalaireActuel, dDateCalcul, dDateDepart, TauxEvolutionSalaire, nMoisDepart_)
    
    if NbAnnees == 1:
        return sf
    
    if NbAnnees <= 0 :
        return None
    
    temp = sf
    
    for i in range(1, NbAnnees):
        temp = temp + sf / (1 + TauxEvolutionSalaire) ** i
    
    return temp / NbAnnees


#%%

def sfs_SIRProjete(dDateNaissance, dDateEngagement, SalaireActuel, dDateCalcul, SIR , TauxEvolutionSalaire = 0.035, TauxCotisSalCRP = 0.13):
    
    SIRDemiAnnee = 0
    
    dsfs_DateDepart = sfs_DateDepartEffective(dDateNaissance, dDateEngagement)
    nMoisDepart_ = dsfs_DateDepart.month
    NbAnnees = int((dsfs_DateDepart - dDateCalcul).days / 365.25)
    
    if nMoisDepart_ == 7:
        if TauxEvolutionSalaire != 0:
            SIRDemiAnnee = 0.5 * SalaireActuel * TauxCotisSalCRP * (1 + TauxEvolutionSalaire) ** (NbAnnees + 1)
        else:
            SIRDemiAnnee = 0.5 * SalaireActuel * TauxCotisSalCRP
        
    if TauxEvolutionSalaire != 0:
        return SalaireActuel * TauxCotisSalCRP * (1 + TauxEvolutionSalaire) * (((1 + TauxEvolutionSalaire) ** NbAnnees - 1) / TauxEvolutionSalaire) + SIRDemiAnnee + SIR
    else:
        return SalaireActuel * TauxCotisSalCRP * NbAnnees + SIRDemiAnnee + SIR
        

#%%

def sfs_CotisRetraite(AssietteRetraite, Tauxsal, TauxPat,TauxPatAddi, ContribAddMax, dSalBase):
    
    ContributionAdd = TauxPatAddi * dSalBase
    ContributionAdd = min(ContribAddMax, ContributionAdd)
    return (Tauxsal + TauxPat) * AssietteRetraite + ContributionAdd

#%%

def sfs_PartiEnRetraite(dDateEngagement, dDateNaissance, dAnnee):
    if sfs_DateDepartEffective(dDateNaissance, dDateEngagement).year > dAnnee:
        return False
    else:
        return True


#%%


def retire(age):
    if age >= 55:
        return True
    else:
        return False
    
def isRetired(age):
    if age > 55:
        return True
    else:
        return False
    
    

































































































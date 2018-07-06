# -*- coding: utf-8 -*-
"""
Created on Fri Jul  6 11:36:25 2018

@author: a.teffal
"""


import Retraite as ret

class Actif:
    def __init__(self,identiant, Strate, Sexe, SitFam, DateNaiss, DateEng, SalBase, IR, PA, SIR, CS):
        self.identifiant = identiant
        self.Strate = Strate
        self.Sexe = Sexe
        self.SitFam = SitFam
        self.DateNaissance = DateNaiss
        self.DateEngagement = DateEng
        self.SB = SalBase
        self.IR = IR
        self.PA = PA
        self.SIR = SIR
        self.CS = CS
        self.AssietteRetraite = self.SB + self.IR + self.PA
        self.Age = None
        
    ###############  getters ##################
    
    def getIdentifiant(self):
        return self.identifiant
    
    def getStrate(self):
        return self.Strate
    
    def getSexe(self):
        return self.Sexe
    
    def getSitFam(self):
        return self.SitFam
    
    def getDateNaissance(self):
        return self.DateNaissance
    
    def getDateEngagement(self):
        return self.DateEngagement
    
    def getSB(self):
        return self.SB
    
    def getIR(self):
        return self.IR
    
    def getPA(self):
        return self.PA
    
    def getSIR(self):
        return self.SIR
    
    def getCS(self):
        return self.CS
    
     ###############  setters : only properties that can change over time ! ##################
    
    def setStrate(self, strate):
        self.Strate = strate
    
    def setSitFam(self, sitFam):
        self.SitFam = sitFam
    
    def setSB(self, sb):
        self.SB = sb
    
    def setIR(self, ir):
        self.IR = ir
    
    def setPA(self, pa):
        self.PA = pa
    
    def setSIR(self, sir):
        self.SIR =sir
    
    def setCS(self, cs):
        self.CS = cs

    ############### other functions ###########################################################
    
    def calcAge(self, dateCalcul):
        self.Age = ret.sfs_CalcAgeAdherent(self.DateNaissance, dateCalcul)
    
         
    
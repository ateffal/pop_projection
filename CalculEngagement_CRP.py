# -*- coding: utf-8 -*-
"""
Éditeur de Spyder

Ceci est un script temporaire.
"""
#%%
import pandas as pd
import numpy as np
import datetime

#%%
#Importation des données démographiques  -- Attention : Fichiers texte doivent être UTF-8 et leurs noms sans accents
actifs=pd.read_csv("actifs.txt",sep=";",decimal=',')
retraites=pd.read_csv("retraites.txt",sep=";",decimal=',')
conjoints=pd.read_csv("conjoints.txt",sep=";",decimal=',')
enfants=pd.read_csv("enfants.txt",sep=";",decimal=',')

#%%
#Mise en forme des dates
actifs["DateNaissance"] = pd.to_datetime(actifs["DateNaissance"],format='%d/%m/%Y 00:00:00')
actifs["DateEngagement"] = pd.to_datetime(actifs["DateEngagement"],format='%d/%m/%Y 00:00:00')
retraites["DateNaissance"] = pd.to_datetime(retraites["DateNaissance"],format='%d/%m/%Y 00:00:00')
retraites["DateEngagement"] = pd.to_datetime(retraites["DateEngagement"],format='%d/%m/%Y')
conjoints["DateNaissance"] = pd.to_datetime(conjoints["DateNaissance"],format='%d/%m/%Y 00:00:00')
enfants["DateNaissance"] = pd.to_datetime(enfants["DateNaissance"],format='%d/%m/%Y 00:00:00')

#%%
#Affichage des 20 premières lignes
print("Actifs")
print(actifs.head(20))
print(actifs.describe())

#%%
print("--- Retraités et ayants-cause")
print(retraites.tail(20))
print(retraites.describe())

#%%
print("--- Conjoints")
print(conjoints.tail(20))
print(conjoints.describe())
print("------------------------------------------")
#%%

#%%
print("--- Enfants")
print(enfants.tail(20))
print(enfants.describe())

#%%

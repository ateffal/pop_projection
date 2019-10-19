# -*- coding: utf-8 -*-
"""
Created on Wed Dec 12 08:35:33 2018

@author: a.teffal
"""

# Pyramides of spouses at years 1, 10, 20, ..., 50

from pop_projection import Effectifs as eff
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pop_projection import sample_laws as sl

# Path for input data
path = "./pop_projection/data/"

# Number of years to project
MAX_ANNEES = 50

# Loading data
employees = pd.read_csv(path + "employees.csv", sep=";", decimal=",")
spouses = pd.read_csv(path + "spouses.csv", sep=";", decimal=",")
children = pd.read_csv(path + "children.csv", sep=";", decimal=",")

# Projection of population
numbers_ = eff.projectNumbers(employees, spouses, children, 'TD 73-77', MAX_ANNEES,
                              law_replacement_=sl.law_replacement1, law_marriage_=sl.law_mar1)

# plot pyramides of spouses at years 1, 10, 20, ..., 50
y = [i*10 for i in range(1, 6)]
for j in y:
    eff.plot_pyramide_spouses(numbers_[1], j, MAX_ANNEES)

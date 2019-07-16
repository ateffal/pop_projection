
# coding: utf-8

# # Global numbers by year in case of no raplacement of departures

# Import necessary packages
from pop_projection import Effectifs as eff
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Path for input data
path ="./pop_projection/data/"

# Loading data
employees = pd.read_csv(path + "employees.csv",sep=";", decimal = ",")
spouses = pd.read_csv(path + "spouses.csv",sep=";", decimal = ",")
children = pd.read_csv(path + "children.csv",sep=";", decimal = ",")

# Diplay some data
print('Employees :')
print(employees.head(10))
print('Spouses :')
print(spouses.head(10))
print('Children :')
print(children.head(10))

# Projection of population
# Number of years to project
MAX_ANNEES = 100

# Projection
numbers_ = eff.simulerEffectif(employees, spouses, children, 'TV 88-90', MAX_ANNEES, law_replacement_ = None)

# global numbers
global_numb = eff.globalNumbers(numbers_[0], numbers_[1], numbers_[2], 50)

# printing results
print(global_numb)

# plotting evolution of actives
plt.xlabel('years')
plt.ylabel('numbers')
plt.plot(global_numb['Year'], global_numb['effectif_actifs'], label='Actives')
plt.plot(global_numb['Year'], global_numb['effectif_retraites'], label='Retirees')
plt.legend(loc='upper right')
plt.show()
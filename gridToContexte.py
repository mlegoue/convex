from Generation_convexes_attributs.Successeurs.find_convexes import find_attributs

from Grille.grille import trace_grille
from Grille.grid_to_contexte import grid_to_contexte

import time

import matplotlib.pyplot as plt
import numpy as np

### Grille

temps_general = []
temps_spe = []
x = []

n = 10

sum_general = {}
sum_spe = {}

for i in range(1, n):
    for j in range(1, n):
        for k in range(100):
            print(i, j, k)
            grid = trace_grille(i, j)
            t1 = time.time()
            general = find_attributs(grid)
            t2 = time.time()
            algoTree = grid_to_contexte(grid)
            t3 = time.time()
            if (i*j) in sum_general.keys():
                sum_general[i*j].append(t2 - t1)
                sum_spe[i*j].append(t3 - t2)
            else:
                sum_general[i * j] = [(t2 - t1)]
                sum_spe[i * j] = [(t3 - t2)]

print(sum_general)

for k in sum_general.keys():
    x.append(k)
    temps_general.append(sum(sum_general[k])/len(sum_general[k]))
    temps_spe.append(sum(sum_spe[k])/len(sum_spe[k]))

plt.plot(x, temps_general, '+', label='Algorithme général')
plt.plot(x, temps_spe, '+', label='Algorithme spécifique')
plt.legend()
plt.title("Temps d'exécution moyen sur 100 grilles")
plt.xlabel("Nombre de noeuds")
plt.ylabel("Temps d'exécution en s")
plt.xlim([0, max(x) + 1])
plt.xticks(x)
plt.savefig("CompGrid/comparaison_grille.png")

import csv
with open('CompGrid/grid_general.csv', 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile)
    for t1 in temps_general:
        spamwriter.writerow([t1])

with open('CompGrid/grid_spe.csv', 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile)
    for t2 in temps_spe:
        spamwriter.writerow([t2])
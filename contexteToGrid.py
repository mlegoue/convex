from Generation_convexes_attributs.Successeurs.find_convexes import find_attributs

from Grille.grille import trace_grille
from Grille.grid_to_contexte import grid_to_contexte
from Grille.contexte_to_grid import contexte_to_grid

from Concept.contexte_to_graph import find_graph

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
        if i != 1 or j != 1 :
            for k in range(100):
                print(i, j, k)
                grid = trace_grille(i, j)
                contexte = np.array(grid_to_contexte(grid)[1])
                t1 = time.time()
                general = find_graph(contexte)
                t2 = time.time()
                spe = contexte_to_grid(contexte)
                t3 = time.time()
                if (i*j) in sum_general.keys():
                    sum_general[i*j].append(t2 - t1)
                    sum_spe[i*j].append(t3 - t2)
                else:
                    sum_general[i * j] = [(t2 - t1)]
                    sum_spe[i * j] = [(t3 - t2)]


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
plt.savefig("CompGrid/comparaison_contexte_grille.png")

import csv
with open('CompGrid/contexte_grid_general.csv', 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile)
    for t1 in temps_general:
        spamwriter.writerow([t1])

with open('CompGrid/contexte_grid_spe.csv', 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile)
    for t2 in temps_spe:
        spamwriter.writerow([t2])
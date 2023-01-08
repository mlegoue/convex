from Generation_convexes_attributs.Successeurs.find_convexes import find_attributs

from Arbres.tree_to_context import arbre_to_contexte
from Arbres.tree import tree_generator


import time

import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

### Arbre

temps_general = []
temps_spe = []

n = 25

for i in range(1, n):
    sum_general = 0
    sum_spe = 0
    for k in range(100):
        print(i, k)
        tree = tree_generator(i)
        t1 = time.time()
        general = find_attributs(tree)
        t2 = time.time()
        algoTree = arbre_to_contexte(tree)
        t3 = time.time()
        sum_general = sum_general + (t2 - t1)
        sum_spe = sum_spe + (t3 - t2)
    temps_general.append(sum_general/100)
    temps_spe.append(sum_spe/100)

plt.plot(np.arange(1, n), temps_general, '+', label='Algorithme général')
plt.plot(np.arange(1, n), temps_spe, '+', label='Algorithme général')
plt.legend()
plt.title("Temps d'exécution moyen sur 100 arbres par nombre de noeuds")
plt.xlabel("Nombre de noeuds")
plt.ylabel("Temps d'exécution en s")
plt.xlim([0, n + 1])
plt.xticks(np.arange(1, n))
plt.savefig("CompTree/comparaison_arbre.png")



import csv
with open('CompTree/arbre_general.csv', 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile)
    for t1 in temps_general:
        spamwriter.writerow([t1])

with open('CompTree/arbre_spe.csv', 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile)
    for t2 in temps_spe:
        spamwriter.writerow([t2])

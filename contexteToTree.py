from Arbres.contexte_to_tree import contexte_to_arbre
from Arbres.tree_to_context import arbre_to_contexte
from Arbres.tree import tree_generator
from Concept.contexte_to_graph import find_graph

import time

import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

### Arbre

temps_general = []
temps_spe = []

n = 15

for i in range(2, n):
    sum_general = 0
    sum_spe = 0
    for k in range(100):
        print(i, k)
        tree = tree_generator(i)
        contexte = np.array(arbre_to_contexte(tree)[2])
        t1 = time.time()
        general = find_graph(contexte)
        t2 = time.time()
        spe = contexte_to_arbre(contexte)
        t3 = time.time()
        sum_general = sum_general + (t2 - t1)
        sum_spe = sum_spe + (t3 - t2)
    temps_general.append(sum_general/100)
    temps_spe.append(sum_spe/100)

plt.plot(np.arange(2, n), temps_general, '+', label='Algorithme général')
plt.plot(np.arange(2, n), temps_spe, '+', label='Algorithme général')
plt.legend()
plt.title("Temps d'exécution moyen sur 100 arbres par nombre de noeuds")
plt.xlabel("Nombre de noeuds")
plt.ylabel("Temps d'exécution en s")
plt.xlim([1, n + 1])
plt.xticks(np.arange(2, n))
plt.savefig("CompTree/comparaison_contexte_arbre.png")



import csv
with open('CompTree/contexte_arbre_general.csv', 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile)
    for t1 in temps_general:
        spamwriter.writerow([t1])

with open('CompTree/contexte_arbre_spe.csv', 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile)
    for t2 in temps_spe:
        spamwriter.writerow([t2])

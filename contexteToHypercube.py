from Generation_convexes_attributs.Successeurs.find_convexes import find_attributs

from Hypercube.hypercubeToContexte import hypercubeToContexte
from Hypercube.contexteToHypercube import contexte_to_hypercube

from Concept.contexte_to_graph import find_graph

import time
import networkx as nx

import matplotlib.pyplot as plt
import numpy as np

### Hypercube

temps_general = []
temps_spe = []

n = 15

for i in range(1, n):
    sum_general = 0
    sum_spe = 0
    for k in range(100):
        print(i, k)
        hypercube = nx.hypercube_graph(i)
        contexte = np.array(hypercubeToContexte(hypercube)[2])
        t1 = time.time()
        general = find_graph(contexte)
        t2 = time.time()
        spe = contexte_to_hypercube(contexte)
        t3 = time.time()
        sum_general = sum_general + (t2 - t1)
        sum_spe = sum_spe + (t3 - t2)
    temps_general.append(sum_general/100)
    temps_spe.append(sum_spe/100)

plt.plot(np.arange(1, n), temps_general, '+', label='Algorithme général')
plt.plot(np.arange(1, n), temps_spe, '+', label='Algorithme général')
plt.legend()
plt.title("Temps d'exécution moyen sur 100 hypercubes par dimension")
plt.xlabel("Dimension")
plt.ylabel("Temps d'exécution en s")
plt.xlim([1, n + 1])
plt.xticks(np.arange(2, n))
plt.savefig("CompHypercube/comparaison_contexte_hyper.png")



import csv
with open('CompHypercube/contexte_hypercube_general.csv', 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile)
    for t1 in temps_general:
        spamwriter.writerow([t1])

with open('CompHypercube/contexte_hypercube_spe.csv', 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile)
    for t2 in temps_spe:
        spamwriter.writerow([t2])

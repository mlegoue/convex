from Generation_convexes_attributs.Successeurs.find_convexes import find_attributs

from Hypercube.hypercubeToContexte import hypercubeToAttributs


import time

import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

### Hypercube
temps_general = []
temps_spe = []

n = 10

for i in range(1, n):
    print(i)
    hypercube = nx.hypercube_graph(i)
    t1 = time.time()
    general = find_attributs(hypercube)
    t2 = time.time()
    algoHyper = hypercubeToAttributs(hypercube)
    t3 = time.time()
    temps_general.append(t2 - t1)
    temps_spe.append(t3 - t2)
    print(t2 - t1)
    print(t3 - t2)

plt.plot(np.arange(1, n), temps_general, '+', label='Algorithme général')
plt.plot(np.arange(1, n), temps_spe, '+', label='Algorithme général')
plt.legend()
plt.title("Temps d'exécution moyen")
plt.xlabel("Dimension de l'hypercube")
plt.ylabel("Temps d'exécution en s")
plt.xlim([0, n + 1])
plt.xticks(np.arange(1, n))
plt.savefig("CompHypercube/comparaison_hypercube.png")

import csv
with open('CompHypercube/hypercube_general.csv', 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile)
    for t1 in temps_general:
        spamwriter.writerow([t1])

with open('CompHypercube/hypercube_spe.csv', 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile)
    for t2 in temps_spe:
        spamwriter.writerow([t2])
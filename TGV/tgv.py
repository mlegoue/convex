import networkx as nx
import matplotlib.pyplot as plt
import json

carte = nx.Graph()


with open('tgv.json', "r") as f:
    tgv = json.load(f)

for ligne in tgv:
    for i in range(len(tgv[ligne]) - 1):
        carte.add_edge(tgv[ligne][i], tgv[ligne][i + 1])



f = open('data/stops.txt', 'r')
start = f.readline()
arrets = {}
lines = f.readlines()
for line in lines:
    tab_arret = line.split(',')
    if tab_arret[1] in list(carte.nodes()):
        arrets[tab_arret[1]] = (float(tab_arret[4]), float(tab_arret[3]))
f.close()

in_cycle = []

for cycle in nx.cycle_basis(carte):
    for node in cycle:
        if node not in in_cycle:
            in_cycle.append(node)

bout_branche = []
branches = []

for node in carte.nodes():
    if nx.degree(carte, nbunch=node) == 1:
        bout_branche.append(node)

print(bout_branche)

for node in bout_branche:
    if node not in branches:
        branches.append(node)
    toexplore = [node]
    while toexplore:
        explore_node = toexplore.pop()
        for voisin in nx.neighbors(carte, explore_node):
            if (voisin not in in_cycle) and (voisin not in branches):
                branches.append(voisin)
                toexplore.append(voisin)

print(branches)

cycles = carte.copy()
for node in carte.nodes():
    if node in branches:
        cycles.remove_node(node)

tgv_min = carte.copy()

for node in carte.nodes():
    if carte.degree[node] == 2:
        voisins = list(nx.neighbors(tgv_min, node))
        tgv_min.add_edge(voisins[0], voisins[1])
        tgv_min.remove_node(node)

plt.figure()
nx.draw(carte, with_labels=True, pos=arrets, node_size=100, font_size=8)
plt.figure()
nx.draw(cycles, with_labels=True, pos=arrets, node_size=100, font_size=8)
plt.show()
nx.draw(tgv_min, with_labels=True, pos=arrets, node_size=100, font_size=8)
plt.show()

from floyd_warshall_2 import attributs_subset

attributs = attributs_subset(tgv_min)[1]

import csv
with open('attributs_tgv_min.csv', 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile)
    for c in attributs:
        spamwriter.writerow(c)

attributs=[]

import csv
with open('attributs_tgv_min.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        attributs.append(row)

print(attributs)






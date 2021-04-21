from floyd_warshall_2 import attributs_subset

with open("metro.txt", 'r') as file:
    lignes = file.readlines()
    metro = {}
    correspondance = {}
    for ligne in lignes:
        if ligne[0] != "#":
            x = ligne.split(":")
            if x[0] != "cor":
                if str(x[0]) + str(x[1]) in metro:
                    metro[str(x[0]) + str(x[1])].append(x[-1][:-1])
                else:
                    metro[str(x[0]) + str(x[1])] = []
                    metro[str(x[0]) + str(x[1])].append(x[-1][:-1])
            else:
                if str(x[1]) in correspondance:
                    if x[-1][:-1] not in correspondance[str(x[1])]:
                        correspondance[str(x[1])] = correspondance[str(x[1])] + ", "+ x[-1][:-1]
                else:
                    correspondance[str(x[1])] = x[-1][:-1]
    for ligne in metro:
        for i in range(len(metro[ligne])):
            for corr in correspondance:
                if metro[ligne][i] in correspondance[corr]:
                    metro[ligne][i] = correspondance[corr]
    print(metro)
    print(correspondance)

import networkx as nx
import matplotlib.pyplot as plt

metro_graphe = nx.Graph()

for ligne in metro:
    for i in range(1, len(metro[ligne])):
        metro_graphe.add_edge(metro[ligne][i-1], metro[ligne][i])

options = {
    'node_color': 'pink',
    'node_size': 50,
}

nx.draw(metro_graphe, **options)
plt.show()

print(metro_graphe.number_of_nodes(), metro_graphe.number_of_edges())

metro_min = metro_graphe.copy()

for node in metro_graphe.nodes():
    if metro_min.degree[node] == 2:
        voisins = list(nx.neighbors(metro_min, node))
        metro_min.add_edge(voisins[0], voisins[1])
        metro_min.remove_node(node)

bout_branche = []

for node in metro_min.nodes():
    if nx.degree(metro_min, nbunch=node) == 1:
        bout_branche.append(node)


for node in bout_branche:
    metro_min.remove_node(node)

# options = {
#     'node_color': 'pink',
#     'node_size': 50,
# }
#
# nx.draw(metro_min, **options, with_labels=True)
# plt.show()

print(metro_min.number_of_nodes(), metro_min.number_of_edges())

attributs = attributs_subset(metro_min)[1]

import csv
with open('attributs_metro_min.csv', 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile)
    for c in attributs:
        spamwriter.writerow(c)
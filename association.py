import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph()

import json

with open('association-1.json', "r") as f:
    associations = json.load(f)

for association in associations:
    if association["Asso1"] != association["Asso2"]:
        G.add_edge(association["Asso1"], association["Asso2"])

# for association in associations:
#    if association["Asso1"] not in list(G.nodes()):
#        G.add_node(association["Asso1"])

print(G.edges())

options = {
    'node_color': 'pink',
    'node_size': 2000,
}

nx.draw(G, with_labels=True, **options)
plt.show()

from floyd_warshall import attributs_subset, convexe_subset

convexes = convexe_subset(G)
#print(attributs_subset(G))

import csv
with open('convexes_association.csv', 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile)
    for convexe in convexes:
        spamwriter.writerow(convexe)
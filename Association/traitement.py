import csv
import networkx as nx

G = nx.Graph()

import json

with open('association-1.json', "r") as f:
    associations = json.load(f)

for association in associations:
    if association["Asso1"] != association["Asso2"]:
        G.add_edge(association["Asso1"], association["Asso2"])



attributs = []
with open('attributs_association.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile)
    for attribut in spamreader:
        attributs.append(attribut)

list_asso = []

import json

with open('association-1.json', "r") as f:
    associations = json.load(f)

for association in associations:
   if association["Asso1"] not in list_asso:
       list_asso.append(association["Asso1"])

degree_asso = {}

for asso in G.nodes():
    degree_asso[asso] = nx.degree(G, asso)

sort_degree = sorted(degree_asso.items(), key=lambda x: x[1], reverse=True)
print(sort_degree)

occ_asso = {}

for asso in list_asso:
    i = 0
    for attribut in attributs:
        if asso in attribut:
            i = i + 1
    occ_asso[asso] = i

sort_asso = sorted(occ_asso.items(), key=lambda x: x[1], reverse=True)
print(sort_asso)

plus_petit_asso = {}

for asso in list_asso:
    i = float('+inf')
    for attribut in attributs:
        if asso in attribut:
            if len(attribut) < i:
                i = len(attribut)
    plus_petit_asso[asso] = i

sort_pp_asso = sorted(plus_petit_asso.items(), key=lambda x: x[1], reverse=True)
print(sort_pp_asso)
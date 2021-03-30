import networkx as nx
import json
from floyd_warshall_2 import plus_court_chemin

G = nx.Graph()


with open('metro_lyon.json', "r") as f:
    metro = json.load(f)

for ligne in metro:
    for i in range(len(metro[ligne]) - 1):
        G.add_edge(metro[ligne][i], metro[ligne][i + 1])

print(G.edges())

def is_convexe(sous_graphe, chemins):
    convexe = True
    for origin in sous_graphe:
        for destination in sous_graphe:
            for chemin in chemins[origin][destination]:
                convexe = convexe and set(chemin).issubset(set(sous_graphe))
    return convexe


def find_convexe(graph):
    chemins = plus_court_chemin(graph)
    convexes = []
    for i1 in range(len(metro["A"])+1):
        for j1 in range(len(metro["A"])+1):
            for i2 in range(len(metro["B"])+1):
                for j2 in range(len(metro["B"])+1):
                    for i3 in range(len(metro["C"])+1):
                        for j3 in range(len(metro["C"])+1):
                            for i4 in range(len(metro["D"])+1):
                                for j4 in range(len(metro["D"])+1):
                                    sous_graphe = metro["A"][i1:j1] + metro["B"][i2:j2] + metro["C"][i3:j3] + metro["D"][i4:j4]
                                    print(len(convexes), i1, j1, i2, j2, i3, j3, i4, j4)
                                    if is_convexe(sous_graphe, chemins) and set(sous_graphe) not in convexes:
                                        convexes.append(sous_graphe)
    return convexes

#convexes = find_convexe(G)

import csv
# with open('convexes.csv', 'w', newline='') as csvfile:
#     spamwriter = csv.writer(csvfile)
#     for c in convexes:
#         spamwriter.writerow(c)

# convexes = []
#
# with open('convexes.csv', newline='') as csvfile:
#     spamreader = csv.reader(csvfile)
#     for row in spamreader:
#         convexes.append(row)
#
# def successeurs(convexe, convexes):
#     successeurs = []
#     for conv in convexes:
#         if set(convexe).issubset(conv) and set(convexe) != set(conv):
#             if successeurs == [] :
#                 successeurs.append(conv)
#             else:
#                 succ = True
#                 a_supp = []
#                 for successeur in successeurs:
#                     if set(conv).issubset(successeur):
#                         a_supp.append(successeur)
#                     elif set(successeur).issubset(conv):
#                         succ = False
#                 for s in a_supp:
#                     successeurs.remove(s)
#                 if succ:
#                     successeurs.append(conv)
#     return successeurs
#
# def find_attributs(convexes):
#     attributs = []
#     for convexe in convexes:
#         print(convexes.index(convexe), len(attributs))
#         succ = successeurs(convexe, convexes)
#         if len(succ) == 1:
#             attributs.append(convexe)
#     return attributs
#
# #print(find_attributs(convexes))
#
# # somme = 0
# # a_supp = []
# # for i in range(len(convexes)):
# #     print(i)
# #     for j in range(len(convexes)):
# #         if i != j and set(convexes[i]) == set(convexes[j]):
# #             somme = somme + 1
# #             a_supp.append(convexes[i])
# #
# # for s in a_supp:
# #     convexes.remove(s)
#
# #print(len(convexes), convexes)
#
attributs = []

with open('attributs.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile)
    for row in spamreader:
        attributs.append(row)

a_supp = []
for i in range(len(attributs)):
    for j in range(len(attributs)):
        if i != j and set(attributs[i]) == set(attributs[j]) and attributs[i] not in a_supp and attributs[j] not in a_supp:
            a_supp.append(attributs[i])

print(len(a_supp), a_supp)

for s in a_supp:
    attributs.remove(s)

dict = {}

for noeud in list(G.nodes()):
    dict[noeud] = 0
    for attribut in attributs:
        print(noeud, attribut)
        if noeud in attribut:
            dict[noeud] = dict[noeud] + 1

print(dict)

done = []



for noeud in list(G.nodes()):
    max = float('-inf')
    for node in list(G.nodes()):
        if dict[node] > max and node not in done:
            noeud_max = node
            max = dict[node]
    done.append(noeud_max)
    print(noeud_max, max)




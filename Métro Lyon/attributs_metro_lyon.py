import networkx as nx
import json
from floyd_warshall_2 import plus_court_chemin

def is_convexe(sous_graphe, chemins):
    convexe = True
    for origin in sous_graphe:
        for destination in sous_graphe:
            for chemin in chemins[origin][destination]:
                convexe = convexe and set(chemin).issubset(set(sous_graphe))
    return convexe

G = nx.Graph()


with open('metro_lyon.json', "r") as f:
    metro = json.load(f)

for ligne in metro:
    if ligne == "A":
        line_color = 'red'
    if ligne == "B":
        line_color = 'blue'
    if ligne == "C":
        line_color = 'orange'
    if ligne == "D":
        line_color = 'green'
    for i in range(len(metro[ligne]) - 1):
        G.add_edge(metro[ligne][i], metro[ligne][i + 1], color=line_color, weight=2)

attributs = []
explored_nodes = []

cycle = nx.Graph()
cycle.add_edges_from(list(nx.find_cycle(G)))

chemins = plus_court_chemin(cycle)
for node in list(cycle.nodes()):
    for node2 in list(cycle.nodes()):
        if node != node2:
            paths = nx.all_simple_paths(G, source=node, target=node2)
            for path in paths:
                if is_convexe(path, chemins) and len(path) == len(cycle.nodes())//2+1:
                    attributs.append(path)
    explored_nodes.append(node)

print(attributs)

for node in list(cycle.nodes()):
    if G.degree[node] > 2:
        neighbors = nx.neighbors(G, node)
        voisins = []
        for neighbor in neighbors:
            if neighbor not in list(cycle.nodes()):
                voisins.append(neighbor)
        for voisin in voisins:
            for attribut in attributs:
                if node in attribut:
                    attribut.append(voisin)
            attributs.append([voisin])
            attributs.append(explored_nodes.copy())
            explored_nodes.append(voisin)
            while G.degree[voisin] == 2:
                neighs = nx.neighbors(G, voisin)
                for neigh in neighs:
                    if neigh not in explored_nodes:
                        for attribut in attributs:
                            if voisin in attribut:
                                attribut.append(neigh)
                        attributs.append([neigh])
                        attributs.append(explored_nodes.copy())
                        explored_nodes.append(neigh)
                        voisin = neigh

print(attributs)

import csv
with open('attributs_metro_lyon.csv', 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile)
    for c in attributs:
        spamwriter.writerow(c)

dict = {}
dict2 = {}
dict3={}
attributsByNode = {}
nbattributsincomparables = {}
color = {}
color2 = {}

for noeud in list(G.nodes()):
    dict[noeud] = 0
    dict2[noeud] = 0
    dict3[noeud] = float('inf')
    attributsByNode[noeud] = []
    for attribut in attributs:
        if noeud in attribut:
            dict[noeud] = dict[noeud] + 1
            dict2[noeud] = dict2[noeud] + len(attribut)
            if dict3[noeud] > len(attribut):
                dict3[noeud] = len(attribut)
            attributsByNode[noeud].append(attribut)
    attributsByNode[noeud].sort(key=lambda v: len(v))
    dict2[noeud] = dict2[noeud]/dict[noeud]

for noeud in list(G.nodes()):
    attributsNode = attributsByNode[noeud].copy()
    attributsincomp = []
    for attribut in attributsNode:
        incomp = True
        for attributincomp in attributsincomp:
            if set(attributincomp).issubset(attribut):
                incomp = False
        if incomp:
            attributsincomp.append(attribut)
    nbattributsincomparables[noeud] = len(attributsincomp)



done = []
done2 = []
done3 = []
done4 = []


for noeud in list(G.nodes()):
    maximum = float('-inf')
    for node in list(G.nodes()):
        if dict[node] > maximum and node not in done:
            noeud_max = node
            maximum = dict[node]
    done.append(noeud_max)
    print(noeud_max, maximum)

inverse = [(value, key) for key, value in dict2.items()]
maxi = max(inverse)[0]
mini = min(inverse)[0]

a = 255/(maxi-mini)
b = -255*mini/(maxi-mini)

inverse2 = [(value, key) for key, value in dict3.items()]
maxi = max(inverse2)[0]
mini = min(inverse2)[0]

a2 = 255/(maxi-mini)
b2 = -255*mini/(maxi-mini)


def classement(dict):
    classement = []
    done = []
    for noeud in dict:
        max = float('-inf')
        for node in dict:
            if dict[node] > max and node not in done:
                noeud_max = node
                max = dict[node]
        classement.append((noeud_max, max))
        done.append(noeud_max)
    return classement

def classementbyfunc(G, func):
    classement = []
    done = []
    for noeud in list(G.nodes()):
        max = float('-inf')
        for node in list(G.nodes()):
            if func(G)[node] > max and node not in done:
                noeud_max = node
                max = func(G)[node]
        classement.append((noeud_max, max))
        done.append(noeud_max)
    return classement

classbymoyattr = classement(dict2)
print(classbymoyattr)
classbynbincomp = classement(nbattributsincomparables)
print(classbynbincomp)
classbycc = classementbyfunc(G, nx.closeness_centrality)
print(classbycc)
classbybc = classementbyfunc(G, nx.betweenness_centrality)
print(classbybc)

placebymoyattr = []
placebycc = []
placebybc = []

for node in list(G.nodes()):
    for i in range(len(classbymoyattr)):
        if classbymoyattr[i][0] == node:
            placebymoyattr.append(i)
        if classbycc[i][0] == node:
            placebycc.append(i)
        if classbybc[i][0] == node:
            placebybc.append(i)

Categories = ["Attributs moyens", "Closness centrality", "Betweennes centrality"] # 3 échantillons
Sous_categories = list(G.nodes()) # comparés selon 4 critères
# Valeurs pour chaque catégories
y1 = placebymoyattr ; y2 = placebycc ; y3 = placebybc
from math import *
nb_categories = len(Categories)
largeur_barre = floor(1*10/nb_categories)/10
x1 = range(len(y1))
x2 = [i + largeur_barre for i in x1]
x3 = [i + 2*largeur_barre for i in x1]
import matplotlib.pyplot as plt
plt.bar(x1, y1, width = largeur_barre, color = 'red',
           edgecolor = 'black', linewidth = 2)
plt.bar(x2, y2, width = largeur_barre, color = 'blue',
           edgecolor = 'black', linewidth = 2)
plt.bar(x3, y3, width = largeur_barre, color = 'green',
           edgecolor = 'black', linewidth = 2)
plt.xticks([r + largeur_barre / nb_categories for r in range(len(y1))],
              Sous_categories)
plt.legend(Categories,loc=2)
plt.show()


# dist_sg = {}
#
# for node in G.nodes():
#     dist_sg[node] = len(nx.shortest_path(G, source="Saxe-Gambetta", target=node)) - 1
#
# print(dist_sg)
#
# positions = {
#   "Perrache": (2, 8),
#   "Ampere": (2, 9),
#   "Bellecour": (2, 10),
#   "Cordeliers": (2, 11),
#   "Hotel de Ville": (2, 12),
#   "Foch": (3, 13),
#   "Massena": (4, 14),
#   "Charpennes": (5, 15),
#   "Republique": (6, 14),
#   "Gratte-ciel": (7, 13),
#   "Flachet": (8, 12),
#   "Cusset": (9, 11),
#   "Laurent Bonnevay": (10, 10),
#   "Brotteaux": (5, 12),
#   "Part-Dieu": (5, 10),
#   "Place Guichard": (4, 9),
#   "Saxe-Gambetta": (4, 8),
#   "Jean Mace": (4, 7),
#   "Place Jean Jaures": (4, 6),
#   "Debourg": (4, 5),
#   "Stade de Gerland": (4, 4),
#   "Cuire": (3, 16),
#   "Henon": (2, 15),
#   "Croix-Rousse": (2, 14),
#   "Croix-Paquet": (2, 13),
#   "Gare de Vaise": (0, 14),
#   "Valmy": (0, 13),
#   "Gorge de Loup": (0, 12),
#   "Vieux Lyon": (1, 11),
#   "Guillotiere": (3, 9),
#   "Garibaldi": (5, 7),
#   "Sans-Souci": (6, 6),
#   "Monplaisir-Lumiere": (7, 5),
#   "Grange Blanche": (8, 4),
#   "Laennec": (8, 3),
#   "Mermoz Pinel": (8, 2),
#   "Parilly": (8, 1),
#   "Gare de Venissieux": (8, 0)
# }
#
# color_map = []
# color_map2 = []
# for node in G:
#     h = hex(color[node])
#     couleur = h[2:]
#     if len(couleur) == 1:
#         couleur = '0' + couleur
#     color_map.append('#' + couleur + couleur + couleur)
#     h = hex(color2[node])
#     couleur = h[2:]
#     if len(couleur) == 1:
#         couleur = '0' + couleur
#     color_map2.append('#' + couleur + couleur + couleur)
#
# edges = G.edges()
# colors = [G[u][v]['color'] for u,v in edges]
#
# nx.draw(G, node_color=color_map, with_labels=False, pos=positions, edge_color=colors, width=3, node_size=100)
#
# for node in G.nodes():
#     x, y = positions[node]
#     plt.text(x+0.1,y,s=node,fontsize='small')
#
# plt.xlim([-2, 12])
# plt.ylim([-0.5, 16.5])
# plt.show()
#
# nx.draw(G, node_color=color_map2, with_labels=False, pos=positions, edge_color=colors, width=3, node_size=100)
#
# for node in G.nodes():
#     x, y = positions[node]
#     plt.text(x+0.1,y,s=node,fontsize='small')
#
# plt.xlim([-2, 12])
# plt.ylim([-0.5, 16.5])
# plt.show()
#
# x=[]
# y=[]
#
# for node in G.nodes():
#     x.append(dist_sg[node])
#     y.append(dict2[node])
#
# plt.plot(x,y,'+')
# plt.show()
#

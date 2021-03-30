import networkx as nx
import json
import matplotlib.pyplot as plt
from floyd_warshall_2 import plus_court_chemin

def is_convexe(sous_graphe, chemins):
    convexe = True
    for origin in sous_graphe:
        for destination in sous_graphe:
            for chemin in chemins[origin][destination]:
                convexe = convexe and set(chemin).issubset(set(sous_graphe))
    return convexe

G = nx.Graph()


with open('metro_marseille.json', "r") as f:
    metro = json.load(f)

for ligne in metro:
    if ligne == "M1":
        line_color = 'blue'
    if ligne == "M2":
        line_color = 'red'
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
with open('attributs_metro_marseille.csv', 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile)
    for c in attributs:
        spamwriter.writerow(c)

dict = {}
dict2 = {}
dict3 = {}
color = {}
color2 = {}

for noeud in list(G.nodes()):
    dict[noeud] = 0
    dict2[noeud] = 0
    dict3[noeud] = float('inf')
    for attribut in attributs:
        if noeud in attribut:
            dict[noeud] = dict[noeud] + 1
            dict2[noeud] = dict2[noeud] + len(attribut)
            if dict3[noeud] > len(attribut):
                dict3[noeud] = len(attribut)
    dict2[noeud] = dict2[noeud]/dict[noeud]


done = []
done2 = []
done3 = []


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



print('Moyenne taille attributs')

for noeud in list(G.nodes()):
    max = float('-inf')
    for node in list(G.nodes()):
        if dict2[node] > max and node not in done2:
            noeud_max = node
            max = dict2[node]
    color[noeud_max] = int(255 - (a * dict2[noeud_max] + b))
    done2.append(noeud_max)
    print(noeud_max, round(max, 2))

print('Taille plus petit attribut')
for noeud in list(G.nodes()):
    max = float('-inf')
    for node in list(G.nodes()):
        if dict3[node] > max and node not in done3:
            noeud_max = node
            max = dict3[node]
    color2[noeud_max] = int(int(255 - (a2 * dict3[noeud_max] + b2)))
    done3.append(noeud_max)
    print(noeud_max, max)

positions = {
    "La Fourragere": (8, 6),
    "Saint-Barnabe": (7, 6),
    "Louis Armand": (6, 5),
    "La Blancarde": (5, 4),
    "La Timone": (4, 3),
    "Baille": (3, 2),
    "Castellane": (2, 2),
    "Estrangin": (1, 3),
    "Vieux-Port": (1, 4),
    "Colbert": (1, 5),
    "Saint-Charles": (2, 5),
    "Reformes Canebiere": (3, 5),
    "Cinq Avenues Longchamp": (4, 5),
    "Chartreux": (5, 6),
    "Saint-Just": (6, 7),
    "Malpasse": (7, 8),
    "Frais Vallon": (8, 9),
    "La Rose": (9, 10),
    "Geze": (1, 11),
    "Bougainville": (1, 10),
    "National": (1, 9),
    "Desiree Clary": (1, 8),
    "Joliette": (1, 7),
    "Jules Guesde": (1, 6),
    "Noailles": (2, 4),
    "Notre-Dame du Mont": (2, 3),
    "Perier": (2, 1),
    "Rond-Point du Prado": (2, 0),
    "Sainte-Marguerite Dromel": (3, 0)
}

color_map = []
color_map2 = []
for node in G:
    h = hex(color[node])
    couleur = h[2:]
    if len(couleur) == 1:
        couleur = '0' + couleur
    color_map.append('#' + couleur + couleur + couleur)
    h = hex(color2[node])
    couleur = h[2:]
    if len(couleur) == 1:
        couleur = '0' + couleur
    color_map2.append('#' + couleur + couleur + couleur)

edges = G.edges()
colors = [G[u][v]['color'] for u,v in edges]

nx.draw(G, node_color=color_map, with_labels=False, pos=positions,edge_color=colors, width=3, node_size=100)

for node in G.nodes():
    x, y = positions[node]
    plt.text(x,y+0.3,s=node,fontsize='small', horizontalalignment='center')

plt.show()

nx.draw(G, node_color=color_map2, with_labels=False, pos=positions, edge_color=colors, width=3, node_size=100)

for node in G.nodes():
    x, y = positions[node]
    plt.text(x,y+0.3,s=node,fontsize='small', horizontalalignment='center')

plt.show()

dist_sc = {}

for node in G.nodes():
    dist_sc[node] = len(nx.shortest_path(G, source="Saint-Charles", target=node)) - 1

print(dist_sc)

x=[]
y=[]
couleur = []

for node in G.nodes():
    x.append(dist_sc[node])
    y.append(dict2[node])
    if node in cycle.nodes():
        couleur.append('red')
    else:
        couleur.append('blue')

plt.scatter(x,y, color=couleur)
plt.show()
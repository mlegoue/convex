import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph()

import json

with open('metro_min_marseille.json', "r") as f:
    metro = json.load(f)

for ligne in metro:
    for i in range (len(metro[ligne]) - 1):
        G.add_edge(metro[ligne][i], metro[ligne][i+1])

options = {
    'node_color': 'pink',
    'node_size': 2000,
}

nx.draw(G, with_labels=True, **options)
plt.show()

def plus_court_chemin(graphe):
    chemin = {}
    for origin in graphe.nodes():
        chemin[origin] = {}
        for destination in graphe.nodes():
            chemin[origin][destination] = list(nx.all_shortest_paths(graphe, origin, destination))
    return chemin

def convexe_subset(graph):
    chemins = plus_court_chemin(graph)
    convexes = []
    i, imax = 0, 2 ** len(list(graph.nodes())) - 1
    while i <= imax:
        sous_graphe = []
        j, jmax = 0, len(list(graph.nodes())) - 1
        convexe = True
        while j <= jmax:
            if (i >> j) & 1 == 1:
                sous_graphe.append(list(graph.nodes())[j])
            j += 1
        for origin in sous_graphe:
            for destination in sous_graphe:
                for chemin in chemins[origin][destination]:
                    convexe = convexe and set(chemin).issubset(set(sous_graphe))
        if convexe:
            convexes.append(sous_graphe)
            print(len(convexes), i, imax, i*100/imax)
        i += 1
    return convexes


def complementaire(sous_liste, liste):
    for noeud in sous_liste:
        liste.remove(noeud)
    return liste


def attributs_subset(graph):
    convexes = convexe_subset(graph)
    attributs = []
    for convexe in convexes:
        attribut = True
        compl = complementaire(convexe, list(graph.nodes()))
        successeurs = []
        i, imax = 0, 2 ** len(compl) - 1
        while attribut and i <= imax:
            partie = []
            j, jmax = 0, len(compl) - 1
            while j <= jmax:
                if (i >> j) & 1 == 1:
                    partie.append(compl[j])
                j += 1
            if partie != []:
                k = 0
                while attribut and k < len(convexes):
                    convexe2 = convexes[k]
                    if set(convexe + partie) == set(convexe2):
                        if successeurs == []:
                            successeurs.append(convexe2)
                        else:
                            if not set(successeurs[0]).issubset(set(convexe2)):
                                successeurs.append(convexe2)
                                attribut = False
                    k = k + 1
            i = i + 1
        if attribut and len(successeurs) == 1:
            attributs.append(convexe)
            print(len(attributs))
    return convexes, attributs


convexes, attributs = attributs_subset(G)

print("convexes", len(convexes))
print("attributs", len(attributs))

import csv
with open('convexes_marseille.csv', 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile)
    for convexe in convexes:
        spamwriter.writerow(convexe)

with open('attributs_marseille_tramway.csv', 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile)
    for attribut in attributs:
        spamwriter.writerow(attribut)
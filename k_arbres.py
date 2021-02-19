import networkx as nx
import random

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
        i += 1
    return convexes


#convexes = convexe_subset(G)


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
    return convexes, attributs

def deux_arbres(n):
    graph = nx.Graph()
    graph.add_edges_from([(0, 1), (0, 2), (1, 2)])
    for i in range(3, n):
        edge = random.choice(list(graph.edges()))
        graph.add_edges_from([(edge[0], i), (edge[1],i)])
    return graph

def deux_arbres_const(n, graph = None):
    if not graph:
        graph = nx.Graph()
        graph.add_edges_from([(0, 1), (0, 2), (1, 2)])
    construction = [graph.copy()]
    for i in range(graph.number_of_nodes(), n):
        edge = random.choice(list(graph.edges()))
        graph.add_edges_from([(edge[0], i), (edge[1], i)])
        construction.append(graph.copy())
    return construction


H6 = nx.Graph()
H6.add_edges_from([(0, 1), (0, 2), (1, 2), (1, 3), (1, 4), (1, 5), (1, 7), (2, 3), (2, 5), (2, 7), (3, 4), (3, 6), (4, 6)])

graphes = deux_arbres_const(12, H6)
all_attributs = []
for graphe in graphes:
    print(graphe.edges())
    convexes, attributs = attributs_subset(graphe)
    print(len(attributs), attributs)
    all_attributs.append(attributs)

# import csv
# with open('convexes.csv', 'w', newline='') as csvfile:
#     spamwriter = csv.writer(csvfile)
#     for convexe in convexes:
#         spamwriter.writerow(convexe)
#
# print(len(attributs), attributs)
#
# with open('attributs.csv', 'w', newline='') as csvfile:
#     spamwriter = csv.writer(csvfile)
#     for attribut in attributs:
#         spamwriter.writerow(attribut)

# H1 = nx.Graph()
# H1.add_edges_from([(0, 1), (0, 2), (1, 2)])
# print(len(convexe_subset(H1)), len(attributs_subset(H1)[1]))
#
# H2 = nx.Graph()
# H2.add_edges_from([(0, 1), (0, 2), (1, 2), (1, 3), (2, 3)])
# print(len(convexe_subset(H2)), len(attributs_subset(H2)[1]))
#
# H3 = nx.Graph()
# H3.add_edges_from([(0, 1), (0, 2), (1, 2), (1, 3), (1, 4), (2, 3), (3, 4)])
# print(len(convexe_subset(H3)), len(attributs_subset(H3)[1]))
#
# H4 = nx.Graph()
# H4.add_edges_from([(0, 1), (0, 2), (1, 2), (1, 3), (1, 4), (1, 5), (2, 3), (2, 5), (3, 4)])
# print(len(convexe_subset(H4)), len(attributs_subset(H4)[1]))
#
# H5 = nx.Graph()
# H5.add_edges_from([(0, 1), (0, 2), (1, 2), (1, 3), (1, 4), (1, 5), (2, 3), (2, 5), (3, 4), (3, 6), (4, 6)])
# print(len(convexe_subset(H5)), len(attributs_subset(H5)[1]))




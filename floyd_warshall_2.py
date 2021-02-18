import numpy
import networkx as nx

# def floyd_warshall(graph):
#     M = []
#     chemin = {}
#     for i in range (graph.number_of_nodes()):
#         M.append([float('inf')]*graph.number_of_nodes())
#     for origin in graph.nodes():
#         chemin[origin] = {}
#         voisins_origin = [n for n in graph[origin]]
#         for destination in graph.nodes():
#             if origin == destination:
#                 M[origin][destination] = 0
#                 chemin[origin][destination] = []
#             elif destination in voisins_origin:
#                 M[origin][destination] = 1
#                 chemin[origin][destination] = [[origin, destination]]
#     for k in graph.nodes():
#         for i in graph.nodes():
#             for j in graph.nodes():
#                 ancien_min = M[i][j]
#                 M[i][j] = min(M[i][j], M[i][k] + M[k][j])
#                 if i != k and k !=j and i != j and M[i][j] != float('inf'):
#                     if M[i][k] + M[k][j] < ancien_min:
#                         chemin[i][j] = [chemin[i][k][0] + chemin[k][j][0][1:]]
#                     elif ancien_min == M[i][k] + M[k][j]:
#                         chemin[i][j].append(chemin[i][k][0] + chemin[k][j][0][1:])
#     return M, chemin


# G = nx.Graph()
# G.add_edge(0, 1)
# G.add_edge(0, 2)
# G.add_edge(1, 2)
# G.add_edge(0, 3)
# G.add_edge(1, 3)
# G.add_edge(1, 4)
# G.add_edge(3, 4)

def plus_court_chemin(graphe):
    chemin = {}
    for origin in graphe.nodes():
        chemin[origin] = {}
        for destination in graphe.nodes():
            chemin[origin][destination] = list(nx.all_shortest_paths(graphe, origin, destination))
    return chemin


def partiesliste(seq):
    p = []
    i, imax = 0, 2**len(seq)-1
    while i <= imax:
        s = []
        j, jmax = 0, len(seq)-1
        while j <= jmax:
            if (i>>j)&1 == 1:
                s.append(seq[j])
            j += 1
        p.append(s)
        i += 1
    return p


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
    return attributs


# print(attributs_subset(G))
#
# H = nx.erdos_renyi_graph(8, 0.7)
# I = nx.binomial_graph(8, 0.5)
# J = nx.connected_watts_strogatz_graph(8, 4, 0.5)
# print(H.edges())
#
# import matplotlib.pyplot as plt
#
# nx.draw(H, with_labels=True, font_weight='bold')
#
# plt.show()
#
# nx.draw(J, with_labels=True, font_weight='bold')
# nx.draw(nx.watts_strogatz_graph(8, 4, 0.5), with_labels=True, font_weight='bold')
#
# plt.show()
#
# resultats = []
#
# for k in range (5, 20):
#     for j in range (2, k//2):
#         I = nx.connected_watts_strogatz_graph(k, j, 0.1)
#         resultats.append((k, j, len(convexe_subset(I)), len(attributs_subset(I))))
#         print(k, j)
#
# import csv
# with open('resultat.csv', 'w', newline='') as csvfile:
#     spamwriter = csv.writer(csvfile)
#     for resultat in resultats:
#         spamwriter.writerow(resultat)

# from k_arbres import deux_arbres
#
# for i in range(5, 6):
#     arbre = deux_arbres(i)
#     print("arbre =", arbre.edges())
#     print("attributs =", attributs_subset(arbre))

# H = nx.Graph()
# H.add_edges_from([(1, 2), (1, 3), (2, 3), (1, 4), (2, 4), (2, 5), (3, 5), (2, 6), (4, 6)])
# convexes = convexe_subset(H)
# print(convexes)
# print(len(convexes))
# print(attributs_subset(H))
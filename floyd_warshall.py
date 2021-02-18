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

def is_in_list(G, list):
    if list == []:
        return False
    for g in list:
        if (set(G.edges()) == set(g.edges())) and (set(G.nodes()) == set(g.nodes())):
            return True
    return False


def is_in_list_nodes(G, list):
    if list == []:
        return False
    for g in list:
        if (set(G.nodes()) == set(g.nodes())):
            return True
    return False

def generate_sous_graphe(G, sous_graphes = []):
    aretes = G.edges()
    for arete in aretes:
        H = G.copy()
        H.remove_edge(*arete)
        components = (H.subgraph(c).copy() for c in nx.connected_components(H))
        for c in components:
            if not is_in_list(c, sous_graphes):
                sous_graphes.append(c.copy())
                if c.number_of_nodes() > 1:
                    generate_sous_graphe(c, sous_graphes)
    return sous_graphes


def convexe_subset(graph):
    chemins = plus_court_chemin(graph)
    sous_graphes = generate_sous_graphe(graph)
    convexes = []
    for sous_graphe in sous_graphes:
        convexe = True
        for origin in sous_graphe:
            for destination in sous_graphe:
                for chemin in chemins[origin][destination]:
                    convexe = convexe and set(chemin).issubset(set(sous_graphe.nodes()))
        if convexe and not is_in_list_nodes(sous_graphe, convexes):
            convexes.append(sous_graphe)
            print(sous_graphe.nodes(), len(convexes))
    return convexes


#convexes = convexe_subset(G)


def complementaire(sous_liste, liste):
    for noeud in sous_liste:
        liste.remove(noeud)
    return liste


def attributs_subset(graph):
    convexes = convexe_subset(graph)
    print("convexes", len(convexes))
    attributs = []
    for convexe in convexes:
        compl = complementaire(list(convexe.nodes()), list(graph.nodes()))
        parties = generate_sous_graphe(graph.subgraph(compl))
        successeurs = []
        attribut = True
        i = 0
        for partie in parties:
            partie = parties[i]
            if list(partie.nodes()) != []:
                j = 0
                for convexe2 in convexes:
                    convexe2 = convexes[j]
                    if set(list(convexe.nodes()) + list(partie.nodes())) == set(list(convexe2.nodes())):
                        if successeurs == []:
                            successeurs.append(convexe2.copy())
                        else:
                            for successeur in successeurs:
                                if set(convexe2.nodes()).issubset(set(successeur.nodes())):
                                    successeurs.remove(successeur)
                                    successeurs.append(convexe2.copy())
                                elif not set(list(successeur.nodes())).issubset(set(list(convexe2.nodes()))):
                                    successeurs.append(convexe2)
                    j = j + 1
                    print(i,j)
            i = i + 1
        print(attribut, len(successeurs))
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
# for i in range(3, 10):
#     arbre = deux_arbres(i)
#     print("arbre =", arbre.edges())
#     print("attributs =", attributs_subset(arbre))
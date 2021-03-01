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


# H6 = nx.Graph()
# H6.add_edges_from([(0, 1), (0, 2), (1, 2), (1, 3), (1, 4), (1, 5), (1, 7), (2, 3), (2, 5), (2, 7), (3, 4), (3, 6), (4, 6)])
#
# graphes = deux_arbres_const(12, H6)
# all_attributs = []
# for graphe in graphes:
#     print(graphe.edges())
#     convexes, attributs = attributs_subset(graphe)
#     print(len(attributs), attributs)
#     all_attributs.append(attributs)

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

def equidistant(graph, x, y):
    equi = []
    for node in list(graph.nodes()):
        if nx.shortest_path_length(graph, x, node) == nx.shortest_path_length(graph, y, node):
            equi.append(node)
    return equi

def successeurs(graph, convexe, convexes):
    successeurs = []
    gconv = float('+inf')
    for conv in convexes:
        if successeurs == [] and set(convexe).issubset(conv):
            successeurs.append(conv)
        else:
            succ = False
            for successeur in successeurs:
                if set(conv).issubset(successeur):
                    succ = True
                    successeurs.remove(successeur)
            if succ:
                successeurs.append(conv)
    return successeurs


def find_attributs_from_attributs(old_graph, old_attributs, x, y, i):
    attributs = []
    equi = equidistant(old_graph, x, y)
    for attribut in old_attributs:
        if (not x in attribut) and (not y in attribut):
            attributs.append(attribut)
        elif x in attribut and y in attribut:
            attributs.append(attribut + [i])
        else:
            equidist = False
            j = 0
            while not equidist and j < len(attribut):
                if attribut[j] in equi:
                    equidist = True
                j = j + 1
            if equidist:
                attributs.append(attribut)
            else:
                attributs.append(attribut + [i])
    return attributs

def list_in_list(x, listes):
    is_in = False
    for liste in listes:
        if set(x) == set(liste):
            is_in = True
    return is_in

def voisin_direct(graph, sommet, x, y, convexe):
    for edge in (list(graph.edges())):
        edge_voisins = []
        if edge[0] == sommet or edge[1] == sommet:
            for node in list(graph.nodes()):
                if nx.shortest_path_length(graph, edge[0], node) == 1 and nx.shortest_path_length(graph, edge[1], node) == 1 and edge != (x, y) and edge != (y, x) and node not in convexe:
                    edge_voisins.append(node)
        if len(edge_voisins) >= 2:
            return True
    return False


def find_attributs_from_convexes(old_graph, old_attributs, old_convexes, x, y, i):
    attributs = []
    equi = equidistant(old_graph, x, y)
    for convexe in old_convexes:
        equidist = False
        j = 0
        if (x in convexe and y not in convexe) or (x not in convexe and y in convexe):
            while not equidist and j < len(convexe):
                if convexe[j] in equi:
                    equidist = True
                j = j + 1
            voisindirect = False
            for node in convexe:
                voisindirect = voisindirect or voisin_direct(old_graph, node, x, y, convexe)
            if not equidist and convexe != [] and not(list_in_list(convexe, old_attributs)) and not voisindirect:
                attributs.append(convexe + [i])
    return attributs

def deux_arbres_attributs(n):
    graph = nx.Graph()
    graph.add_edges_from([(0, 1), (0, 2), (1, 2)])
    attributs_const = [[0, 1], [0, 2], [1, 2]]
    construction = [graph.copy()]
    attributs = [attributs_const]
    convexe, attribut = attributs_subset(graph)
    real_attributs = [attribut]
    real_convexes = [convexe]
    for i in range(graph.number_of_nodes(), n):
        x, y = random.choice(list(graph.edges()))
        attributs.append(find_attributs_from_attributs(graph, attributs[-1], x, y, i) + [list(graph.nodes())] + find_attributs_from_convexes(graph, attributs[-1], real_convexes[-1], x, y, i ))
        graph.add_edges_from([(x, i), (y, i)])
        construction.append(graph.copy())
        realc, reala = attributs_subset(graph)
        real_attributs.append(reala)
        real_convexes.append(realc)
    return construction, attributs, real_attributs


construction, attributs, real_attributs = deux_arbres_attributs(10)

for i in range(len(construction)):
    print(construction[i].edges())
    print(attributs[i])
    print(real_attributs[i])
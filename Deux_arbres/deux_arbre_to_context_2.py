import networkx as nx
import random
import time


def deux_arbres(n):
    graph = nx.Graph()
    graph.add_edges_from([(0, 1), (0, 2), (1, 2)])
    construction = [graph.copy()]
    for i in range(graph.number_of_nodes(), n):
        x, y = random.choice(list(graph.edges()))
        graph.add_edges_from([(x, i), (y, i)])
        construction.append(graph.copy())
    return construction

def find_intention(attributs, extension):
    intention = []
    for attribut in attributs:
        if set(extension).issubset(attribut):
            intention.append(attribut)
    return intention


def find_extension(objets, intention):
    extension = []
    for objet in objets:
        in_attribut = True
        for attribut in intention:
            if objet not in attribut:
                in_attribut = False
        if in_attribut:
            extension.append(objet)
    return extension


def find_concept_u(u, objets, attributs):
    intention = find_intention(attributs, [u])
    extension = find_extension(objets, intention)
    return extension


def is_equi(graph, x, y, n):
    xn = nx.shortest_path_length(graph, x, n)
    yn = nx.shortest_path_length(graph, y, n)
    return xn == yn


def find_new_attr(u, equi, objets, attributs, x, y, graph):
    concept_u = find_concept_u(u, objets, attributs)
    new_attr = []
    if concept_u == [u]:
        return None
    concept_u.remove(u)
    for n in concept_u:
        if len(equi) == 2:
            if n == x:
                new_attr.append([y, u])
            else:
                new_attr.append([x, u])
        else:
            for attribut in attributs:
                for e in equi:
                    if (n in attribut) and (e in attribut) and (u not in attribut):
                        na = attribut.copy()
                        na.remove(e)
                        a_supp = []
                        for noeud in na:
                            if is_equi(graph, x, y, noeud):
                                a_supp.append(noeud)
                        for a in a_supp:
                            na.remove(a)
                        na.append(u)
                        a_supp = []
                        for noeud in na:
                            chemins = nx.all_shortest_paths(graph, u, noeud)
                            one = False
                            for chemin in chemins:
                                one = one or set(chemin).issubset(na)
                            if not one:
                                a_supp.append(noeud)
                        for a in a_supp:
                            na.remove(a)
                        if na not in new_attr:
                            add = True
                            a_supp = []
                            if new_attr == []:
                                add = True
                            else:
                                for a in new_attr:
                                    if set(a).issubset(na):
                                        add = False
                                    elif set(na).issubset(a):
                                        a_supp.append(a)
                            if add:
                                new_attr.append(na)
                            for att in a_supp:
                                new_attr.remove(att)
    return new_attr

def equidistant(graph, x, y):
    equi = []
    for node in list(graph.nodes()):
        if (nx.shortest_path_length(graph, x, node) == 1) and (nx.shortest_path_length(graph, y, node) == 1):
            equi.append(node)
    return equi

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


def equal(list1, list2):
    if len(list1) == len(list2):
        equal = True
        for a in list1:
            find = False
            for b in list2:
                find = find or (set(a) == set(b))
            equal = equal and find
        return equal
    return False

from Generation_convexes_attributs.Successeurs.find_convexes import find_attributs

equality = True

while equality:
    deux_arbres_list = deux_arbres(20)
    attributs = [[[0, 1], [0, 2], [1, 2]]]
    for i in range(1, len(deux_arbres_list)):
        t1 = time.time()
        old_attributs = attributs[i - 1]
        old_graph = deux_arbres_list[i - 1]
        u = i + 2
        [x, y] = nx.neighbors(deux_arbres_list[i], u)
        attributs_w_u = find_attributs_from_attributs(old_graph, old_attributs, x, y, u)
        equi = equidistant(deux_arbres_list[i], x, y)
        attributs_w_u.append(list(old_graph.nodes()))
        na = find_new_attr(u, equi, deux_arbres_list[i].nodes(), attributs_w_u, x, y, deux_arbres_list[i])
        if na != None:
            new_attributs = attributs_w_u + na
        else:
            new_attributs = attributs_w_u
        attributs.append(new_attributs)
        t2 = time.time()
        real_attr = find_attributs(deux_arbres_list[i])[1]
        t3 = time.time()
        print(i)
        print(deux_arbres_list[i].edges())
        print(new_attributs)
        print(real_attr)
        print(equal(new_attributs, real_attr), t2-t1, t3-t2)
        equality = equality and equal(new_attributs, real_attr)



#print(find_new_attr(16, equi, objets, attributs))

# deux_ar = nx.Graph()
# deux_ar.add_edges_from([(0, 1), (0, 2), (0, 7), (1, 2), (1, 3), (1, 4), (1, 5), (1, 8), (2, 3), (2, 7), (3, 4), (3, 8), (4, 5), (4, 6), (5, 6)])
# old_attr = [[0, 6, 1, 4, 5], [0, 7], [3, 6, 4], [3, 7, 2], [5, 6], [5, 7, 1, 0, 2], [6, 7, 4, 1, 0, 5, 2, 3], [6, 8, 4, 1, 5, 3], [7, 8, 0, 1, 2, 3], [0, 2, 7], [0, 6, 1, 4, 5, 8, 3, 2], [2, 6, 1, 4, 3, 5, 8], [4, 5, 6], [4, 7, 1, 0, 2, 3, 8], [5, 7, 1, 0, 2, 8, 3, 4]]
# na = find_new_attr(8, [2, 4, 8], deux_ar.nodes(), old_attr, 1, 3, deux_ar)
#
# print(na)

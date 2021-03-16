import networkx as nx
import random
#import matplotlib.pyplot as plt
#import pandas as pd

def deux_arbres(n):
    graph = nx.Graph()
    graph.add_edges_from([(0, 1), (0, 2), (1, 2)])
    for i in range(3, n):
        edge = random.choice(list(graph.edges()))
        graph.add_edges_from([(edge[0], i), (edge[1],i)])
    return graph


def deux_arbres_const(graph, x, y, u):
    graph.add_edges_from([(x, u), (y, u), (x, y)])
    return graph


def deux_arbre_deconst(arbre):
    noeuds = list(arbre.nodes())
    edges = list(arbre.edges())
    if len(noeuds) == 3:
        if (((noeuds[0], noeuds[1]) in edges or (noeuds[1], noeuds[0]) in edges) and ((noeuds[0], noeuds[2]) in edges or (noeuds[2], noeuds[0]) in edges) and ((noeuds[2], noeuds[1]) in edges or (noeuds[1], noeuds[2]) in edges)):
            return [[noeuds[0], (noeuds[1], noeuds[2])]]
    else:
        for noeud in noeuds:
            if arbre.degree(noeud) == 2:
                voisins = [n for n in arbre.neighbors(noeud)]
                if (voisins[0], voisins[1]) in edges or (voisins[1], voisins[0]) in edges:
                    arbre.remove_node(noeud)
                    return [[noeud, (voisins[0], voisins[1])]] + deux_arbre_deconst(arbre)
    return None


def equidistant(graph, x, y):
    equi = []
    for node in list(graph.nodes()):
        if nx.shortest_path_length(graph, x, node) == nx.shortest_path_length(graph, y, node):
            equi.append(node)
    return equi

def successeurs(convexe, convexes):
    successeurs = []
    for conv in convexes:
        if set(convexe).issubset(conv) and set(convexe) != set(conv):
            if successeurs == [] :
                successeurs.append(conv)
            else:
                succ = True
                for successeur in successeurs:
                    if set(conv).issubset(successeur):
                        succ = True
                        successeurs.remove(successeur)
                    elif set(successeur).issubset(conv):
                        succ = succ and False
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


def one_successeur_rec(graph, convexe, old_convexes, x, y, equi, succ):
    list_successeurs = successeurs(convexe, old_convexes)
    #print(list_successeurs)
    if x in convexe:
        noeud = y
    if y in convexe:
        noeud = x
    if set(list_successeurs[0]) == set(graph.nodes()):
        existe_plus_petit = False
        for s in succ:
            existe_plus_petit = existe_plus_petit or set(s).issubset(graph.nodes())
        if not existe_plus_petit:
            succ.append(list(graph.nodes()))
    else:
        for successeur in list_successeurs:
            equidist = False
            for node in equi:
                equidist = equidist or (node in successeur)
            #print("coucou", equidist, successeur, noeud)
            if not equidist or (equidist and noeud in successeur):
                #print("ouiiiiiiiiii", succ)
                existe_plus_petit = False
                a_supp = []
                for s in succ:
                    existe_plus_petit = existe_plus_petit or set(s).issubset(successeur)
                    #print(existe_plus_petit, s, 'plus petit que', successeur)
                    if set(successeur).issubset(s):
                        a_supp.append(s)
                for s in a_supp:
                    succ.remove(s)
                if not existe_plus_petit and successeur not in succ:
                    #print("coucou")
                    succ.append(successeur)
            elif noeud in successeur:
                existe_plus_petit = False
                a_supp=[]
                for s in succ:
                    existe_plus_petit = existe_plus_petit or set(s).issubset(successeur)
                    #print(existe_plus_petit, s, 'plus petit que', successeur)
                    if set(successeur).issubset(s):
                        a_supp.append(s)
                for s in a_supp:
                    succ.remove(s)
                if not existe_plus_petit and successeur not in succ:
                    succ.append(successeur)
            else:
                succ2 = one_successeur_rec(graph, successeur, old_convexes, x, y, equi, [])
                for s2 in succ2:
                    existe_plus_petit = False
                    a_supp1 = []
                    for s1 in succ:
                        #print("s1", s1)
                        existe_plus_petit = existe_plus_petit or (set(s1).issubset(s2) and not set(s1) == set(s2))
                        if set(s2).issubset(s1):
                            a_supp1.append(s1)
                    for s in a_supp1:
                        succ.remove(s)
                    #print(existe_plus_petit)
                    if not existe_plus_petit and successeur not in succ:
                        succ.append(s2)
    #print("a", succ)
    return succ


def one_successeur(graph, convexe, old_convexes, x, y):
    succ = one_successeur_rec(graph, convexe, old_convexes, x, y, equidistant(graph, x, y), [])
    #print("successeurs", convexe, succ)
    return succ


def find_attributs_from_convexes(old_graph, old_attributs, old_convexes, x, y, i):
    attributs = []
    equi = equidistant(old_graph, x, y)
    for convexe in old_convexes:
        if set(convexe) != set(old_graph.nodes()):
            equidist = False
            j = 0
            if (x in convexe and y not in convexe) or (x not in convexe and y in convexe):
                while not equidist and j < len(convexe):
                    if convexe[j] in equi:
                        equidist = True
                    j = j + 1
                #print("wesh", convexe, equidist, x, y, i)
                if not equidist and convexe != [] and not(list_in_list(convexe, old_attributs)) and len(one_successeur(old_graph, convexe, old_convexes, x, y)) == 1:
                    attributs.append(convexe + [i])
    return attributs


def new_convexes(graph, old_convexes, x, y, u):
    new = old_convexes.copy()
    for convexe in old_convexes:
        if x in convexe and y in convexe:
            new.append(convexe + [u])
        elif (x in convexe or y in convexe):
            equi = equidistant(graph, x, y)
            equidist = False
            j = 0
            while not equidist and j < len(convexe):
                if convexe[j] in equi:
                    equidist = True
                j = j + 1
            if not equidist:
                new.append(convexe + [u])
    return new


def deux_arbres_to_attributs(graph):
    #print(graph.edges())
    deconst = deux_arbre_deconst(graph.copy())
    [u, (x, y)] = deconst.pop()
    arbre = deux_arbres_const(nx.Graph(), x, y, u)
    attributs = [[x, y], [u, x], [u, y]]
    convexes = [[], [x], [y], [u], [x, y], [u, x], [u, y], [x, y, u]]
    for i in range(len(deconst)):
        [u, (x, y)] = deconst.pop()
        attributs = find_attributs_from_attributs(arbre, attributs, x, y, u) + [list(arbre.nodes())] + find_attributs_from_convexes(arbre, attributs, convexes, x, y, u)
        convexes = new_convexes(arbre, convexes, x, y, u) + [[u]]
        arbre = deux_arbres_const(arbre, x, y, u)
        # print(attributs)
        # print(arbre.edges())
    return arbre.edges(), attributs, convexes


def attributs_to_contexte(objets, attributs):
    contexte = []
    for i in range(len(objets)):
        contexte.append([0] * len(attributs))
    attributs = list(map(lambda subg: ''.join(map(str, subg)), attributs))
    for objet in objets:
        for attribut in attributs:
            if str(objet) in attribut:
                contexte[objets.index(objet)][attributs.index(attribut)] = 1
            else:
                contexte[objets.index(objet)][attributs.index(attribut)] = 0
    return objets, attributs, contexte


# def display_contexte(objets, attributs, contexte):
#     fig, ax = plt.subplots()
#     # hide axes
#     fig.patch.set_visible(False)
#     ax.axis('off')
#     ax.axis('tight')
#
#     df = pd.DataFrame(contexte, columns=attributs)
#     ax.table(cellText=df.values, colLabels=df.columns, loc='center', rowLabels=objets)
#     fig.tight_layout()
#     plt.show()


# arbre = deux_arbres(6)
# attributs = deux_arbres_to_attributs(arbre)[1]
# print(attributs)
# objets, attributs, contexte = attributs_to_contexte(list(arbre.nodes()), attributs)
# print(contexte)
# display_contexte(objets, attributs, contexte)

# arbre = nx.Graph()
# arbre.add_edges_from([(0, 1), (0, 2), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8), (2, 3), (2, 5), (2, 7), (3, 4), (3, 6), (7, 8)])
# print(deux_arbres_to_attributs(arbre.copy()))
#
#
# from k_arbres import attributs_subset
# print(attributs_subset(arbre.copy())[1])


# Soit le contexte de l'arbre T + u, tentons de revenir au contexte de l'arbre T

import numpy as np
import networkx as nx

# contexte = np.array([[1, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0],
#                      [1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0],
#                      [0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0],
#                      [0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 1, 0],
#                      [1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 1, 1, 1],
#                      [0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0],
#                      [0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 1]])

# contexte = np.array([[1, 1, 0, 0, 0, 1, 1, 1, 1, 0],
#                      [0, 0, 0, 1, 1, 1, 1, 1, 1, 0],
#                      [1, 0, 1, 1, 0, 0, 1, 1, 1, 0],
#                      [0, 1, 0, 0, 1, 1, 0, 1, 1, 1],
#                      [0, 0, 1, 1, 1, 0, 1, 0, 1, 0],
#                      [1, 1, 0, 0, 0, 1, 0, 1, 0, 1]])

contexte = np.array([[0, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1],
                     [0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1],
                     [0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0],
                     [0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0],
                     [1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0],
                     [0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1],
                     [1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0]])

def is_deux_arbre(arbre):
    noeuds = list(arbre.nodes())
    edges = list(arbre.edges())
    if len(noeuds) == 3:
        if (((noeuds[0], noeuds[1]) in edges or (noeuds[1], noeuds[0]) in edges) and ((noeuds[0], noeuds[2]) in edges or (noeuds[2], noeuds[0]) in edges) and ((noeuds[2], noeuds[1]) in edges or (noeuds[1], noeuds[2]) in edges)):
            return True
    else:
        for noeud in noeuds:
            if arbre.degree(noeud) == 2:
                voisins = [n for n in arbre.neighbors(noeud)]
                if (voisins[0], voisins[1]) in edges or (voisins[1], voisins[0]) in edges:
                    arbre.remove_node(noeud)
                    return is_deux_arbre(arbre)
    return False



def find_u(contexte, objets):
    find_n = False
    objet = None
    j = 0
    while not find_n:
        colonne = contexte[:, j]
        if np.count_nonzero(colonne == 0) == 1:
            objet = np.where(colonne == 0)
            find_n = True
        j = j + 1
    if find_n:
        return True, j-1, objets[objet[0][0]]
    return False, None


def is_include(colonne1, colonne2):
    include = True
    for i in range(len(colonne1)):
        if (colonne1[i] == 1 and colonne2[i] == 0):
            include = False
    return include


def array_onecase(array, u):
    return np.concatenate((array[:u], array[u+1:]))


def find_new_attributs(contexte, u):
    new_attributs = []
    for i in range(len(contexte[0])):
        successeurs = []
        for j in range(len(contexte[0])):
            coli = contexte[:, i]
            colj = contexte[:, j]
            if coli[u] == 1 and i != j and is_include(array_onecase(coli, u), array_onecase(colj, u)):
                successeur = True
                a_supp = []
                # for succ in successeurs:
                #     if is_include(array_onecase(succ, u), array_onecase(colj, u)):
                #         successeur = False
                #     if is_include(array_onecase(colj, u), array_onecase(succ, u)):
                #         a_supp.append(succ)
                # for succ in a_supp:
                #     successeurs.remove(succ)
                if successeur:
                    successeurs.append(colj)
        if len(successeurs) > 2 or (len(contexte) == 4 and len(successeurs) == 2):
            new_attributs.append(i)
    contexte = np.delete(contexte, new_attributs, axis=1)
    return contexte


def contexteT_utocontexteT(contexte, objets):
    find, j, u = find_u(contexte, objets)
    if not find:
        print("Ce n'est pas un deux arbre")
        return None
    else:
        new_contexte = np.delete(contexte, j, axis=1)
        new_contexte = find_new_attributs(new_contexte, objets.index(u))
        new_contexte = np.delete(new_contexte, objets.index(u), axis=0)
        objets.remove(u)
    return new_contexte, u, objets


def find_couple(n, u, objets):
    list = []
    indice = objets.index(u)
    for i in range(n):
        for j in range(i+1, n):
            if i != indice and j != indice:
                list.append([objets[i], objets[j]])
    return list

def contexte_to_attribut(list, objets):
    attribut = []
    for i in range(len(list)):
        if list[i] == 1:
            attribut.append(objets[i])
    return attribut


def interliste(liste1, liste2):
    liste = []
    for a in liste1:
        for b in liste2:
            if set(a) == set(b):
                liste.append(a)
    return liste

def find_x_y(contexte, u, objets):
    couples = find_couple(len(contexte), u, objets)
    attribut3 = []
    for j in range(len(contexte[objets.index(u)])):
        attribut = contexte_to_attribut(contexte[:, j], objets)
        print(couples, attribut)
        if len(attribut) == 3 and u in attribut:
            attributbis = attribut.copy()
            del attributbis[attributbis.index(u)]
            attribut3.append(attributbis)
        if contexte[objets.index(u)][j] == 0:
            if np.count_nonzero(contexte[:, j]) != len(contexte) - 1:
                a_supp = []
                for couple in couples:
                    if set(couple).issubset(attribut):
                        a_supp.append(couple)
                for couple in a_supp:
                    couples.remove(couple)
        else:
            a_supp = []
            for couple in couples:
                if not couple[0] in attribut and not couple[1] in attribut:
                    a_supp.append(couple)
            for couple in a_supp:
                couples.remove(couple)
    if len(interliste(couples, attribut3)) > 0:
        return interliste(couples, attribut3)
    return couples


# contexteT, u, new_objets = contexteT_utocontexteT(contexte, [0, 1, 2, 3, 4, 5, 6])
# print(contexteT, u)
# print(find_x_y(contexte, u, [0, 1, 2, 3, 4, 5, 6]))
#
# contexteT2, u, new_objets2 = contexteT_utocontexteT(contexteT, new_objets.copy())
# print(contexteT2, u)
# print(find_x_y(contexteT, u, new_objets))
#
# contexteT3, u, new_objets3 = contexteT_utocontexteT(contexteT2, new_objets2.copy())
# print(contexteT3, u)
# print(find_x_y(contexteT2, u, new_objets2))
#
# contexteT4, u, new_objets4 = contexteT_utocontexteT(contexteT3, new_objets3.copy())
# print(contexteT4, u)
# print(find_x_y(contexteT3, u, new_objets3))


def contexte_to_deuxarbre(contexte, objets, arbres):
    if len(contexte) == 3:
        trees = []
        for arbre in arbres:
            arbre.add_edges_from([(objets[0], objets[1]), (objets[0], objets[2]), (objets[1], objets[2])])
            if is_deux_arbre(arbre.copy()):
                 trees.append(arbre)
        return trees
    else:
        contexteT, u, new_objets = contexteT_utocontexteT(contexte, objets.copy())
        couples = find_x_y(contexte, u, objets)
        print(couples, u)
        trees = []
        for couple in couples:
            for arbre in arbres:
                new_tree = arbre.copy()
                new_tree.add_edges_from([(u, couple[0]), (u, couple[1]), (couple[0], couple[1])])
                trees.append(new_tree)
        return contexte_to_deuxarbre(contexteT, new_objets, trees)


# new_contexte, trees = contexte_to_deuxarbre(contexte, [0, 1, 2, 3, 4, 5, 6], [nx.Graph()])
#
# for arbre in trees:
#     print(arbre.edges())

from deux_arbre_to_contexte import deux_arbres_to_attributs, attributs_to_contexte
from k_arbres import deux_arbres

#arbre = deux_arbres(7)
#edges, attributs, convexes = deux_arbres_to_attributs(arbre)
#objets, attributs, contxt = attributs_to_contexte(list(arbre.nodes()), attributs)

arbres = contexte_to_deuxarbre(contexte, list(range(7)), [nx.Graph()])

print(contexte)

for arbre in arbres:
    print("coucou", arbre.edges())


import numpy as np
import networkx as nx

contexte = np.array([[1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0],
                     [1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0],
                     [1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
                     [1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
                     [1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0],
                     [1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
                     [1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0],
                     [1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1],
                     [1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0],
                     [0, 1, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
                     [1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0]])


def check_taille(contexte):
    return 2 * (len(contexte) - 1) == len(contexte[0])



def check_parity(contexte):
    check = True
    for ligne in contexte:
        check = check and np.count_nonzero(ligne == 0) == np.count_nonzero(ligne == 1)
    return check

def find_two_columns(contexte):
    find_one = False
    find_n = False
    objet = None
    i = 0
    while not find_one:
        colonne = contexte[:, i]
        if np.count_nonzero(colonne == 1) == 1:
            objet = np.where(colonne == 1)
            find_one = True
        i = i+1
    j = 0
    while not find_n and find_one:
        colonne = contexte[:, j]
        if np.count_nonzero(colonne == 0) == 1:
            if colonne[objet] == 0 :
                find_n = True
        j = j + 1
    if find_one and find_n:
        return True, i-1, j-1, objet
    return False, None, None, None

def find_pere(fils, contexte):
    ligne_fils = contexte[fils]
    for i in range(len(contexte)):
        if i != fils and np.array_equal(ligne_fils, contexte[i]):
            return i


def contexte_to_arbre_rec(contexte, arbre, objets):
    if not (check_taille(contexte) and check_parity(contexte)):
        print("Ce n'est pas un arbre")
    else:
        check, i, j, objet = find_two_columns(contexte)
        objet = list(objet)[0][0]
        if check:
            if len(contexte) == 2:
                arbre.add_edge(objets[0], objets[1])
                return arbre
            new_contexte = np.delete(contexte, [i, j], axis=1)
            pere = find_pere(objet, new_contexte)
            arbre.add_edge(objets[objet], objets[pere])
            new_contexte = np.delete(new_contexte, objet, axis=0)
            new_objets = np.delete(objets, objet, axis=0)
            return contexte_to_arbre_rec(new_contexte, arbre, new_objets)
        else:
            print("Ce n'est pas un arbre")


def contexte_to_arbre(contexte):
    arbre = nx.Graph()
    objets = np.arange(len(contexte))
    arbre.add_nodes_from(objets)
    return contexte_to_arbre_rec(contexte, arbre, objets)




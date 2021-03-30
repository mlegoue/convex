import numpy as np
from grille import trace_grille


contexte = np.array([[1, 1, 1, 0, 0, 0, 1, 1, 0, 0],
                     [1, 1, 1, 0, 0, 0, 0, 1, 0, 1],
                     [1, 1, 1, 0, 0, 0, 0, 0, 1, 1],
                     [0, 1, 1, 0, 0, 1, 1, 1, 0, 0],
                     [0, 1, 1, 0, 0, 1, 0, 1, 0, 1],
                     [0, 1, 1, 0, 0, 1, 0, 0, 1, 1],
                     [0, 0, 1, 0, 1, 1, 1, 1, 0, 0],
                     [0, 0, 1, 0, 1, 1, 0, 1, 0, 1],
                     [0, 0, 1, 0, 1, 1, 0, 0, 1, 1],
                     [0, 0, 0, 1, 1, 1, 1, 1, 0, 0],
                     [0, 0, 0, 1, 1, 1, 0, 1, 0, 1],
                     [0, 0, 0, 1, 1, 1, 0, 0, 1, 1]])


def check_taille(contexte, n, m):
    return 2 * (m + n - 2) == len(contexte[0])

def check_parity(contexte):
    check = True
    for ligne in contexte:
        check = check and np.count_nonzero(ligne == 0) == np.count_nonzero(ligne == 1)
    return check


def find_col(contexte):
    min = float('+inf')
    for i in range(len(contexte[0])):
        n = np.count_nonzero(contexte[:, i] == 1)
        if n < min:
            min = n
    return min

def find_m(contexte, n):
    m = float('+inf')
    for i in range(len(contexte[0])):
        a = np.count_nonzero(contexte[:, i] == 1)
        if a%n != 0 and a < m:
            m = a
    if m == float('+inf'):
        dict = {}
        for i in range(len(contexte[0])):
            a = np.count_nonzero(contexte[:, i] == 1)
            dict[a] = dict[a] + 1
        for c in dict:
            if dict[c] == 4 and c < m:
                m = c
    return m

def check_size(contexte, n, m):
    check = True
    for i in range(len(contexte[0])):
        a = np.count_nonzero(contexte[:, i] == 1)
        check = check and (a%n == 0 or a%m == 0)
    return check


def is_include(colonne1, contexte, k):
    include = True
    for j in range(len(contexte[0])):
        incl = True
        for i in range(len(colonne1)):
            if (i!=j and colonne1[i] == 1 and contexte[i, j] == 0):
                incl = False
        include = include or incl
    return include


def compl(contexte):
    comp = True
    for i in range(len(contexte[0])):
        a = np.count_nonzero(contexte[:, i] == 1)
        complementaire = False
        for j in range(len(contexte[0])):
            if i != j:
                c = True
                for k in range(len(contexte)):
                    c = c and (contexte[k, j] + contexte[k, i] == 1)
                complementaire = complementaire or c
        comp = complementaire and comp
    return comp


def contexte_to_grid(contexte):
    n = find_col(contexte)
    m = find_m(contexte, n)
    if check_taille(contexte, n, m) and check_size(contexte, n, m) and compl(contexte):
        all_include = True
        for i in range(len(contexte[0])):
            if np.count_nonzero(contexte[:, i] == 1) != (m-1)*n or np.count_nonzero(contexte[:, i] == 1) != (n-1)*m:
                all_include = all_include and is_include(contexte[:, i], contexte, i)
        return trace_grille(n, m)

print(contexte_to_grid(contexte))


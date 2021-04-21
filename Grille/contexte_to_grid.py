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


def find_n(contexte):
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
        if a % n != 0 and a < m:
            m = a
    if m == float('+inf'):
        dict = {}
        for i in range(len(contexte[0])):
            a = np.count_nonzero(contexte[:, i] == 1)
            if a not in dict:
                dict[a] = 0
            dict[a] = dict[a] + 1
        for c in dict:
            if dict[c] == 4 and c < m:
                m = c
    return m


#
# def check_size(contexte, n, m):
#     check = True
#     for i in range(len(contexte[0])):
#         a = np.count_nonzero(contexte[:, i] == 1)
#         check = check and (a%n == 0 or a%m == 0)
#     return check
#
#
# def is_include(colonne1, colonne2):
#     include = True
#     for i in range(len(colonne1)):
#         if (colonne1[i] == 1 and colonne2[i] == 0):
#             include = False
#     return include
#
# def is_include_part(colonne1, colonne2):
#     include = False
#     for i in range(len(colonne1)):
#         if (colonne1[i] == 1 and colonne2[i] == 1):
#             include = True
#     return include
#
# def is_include_kn(n, m, colonne1, colonne2, contexte):
#     ok = True
#     inclusion_rec = False
#     is_in = []
#     for j in range(contexte[0]):
#         if colonne1 != contexte[:, j] and is_include(colonne1, contexte[:, j]):
#             is_in.append(contexte[:,j])
#     inclusion = np.zeros((m-1,), dtype=int)
#     inclusion[0] = 1
#     is_in.sort(key=len)
#     for attribut in is_in:
#         if np.count_nonzero(attribut == 1) % n == 0:
#             if np.count_nonzero(attribut == 1) // n <= m-1 and np.count_nonzero(attribut == 1) // n > m:
#                 inclusion[np.count_nonzero(attribut == 1) // n] += 1
#                 if is_include(colonne2, attribut):
#                     inclusion[np.count_nonzero(attribut == 1) // n] = 1000
#             else:
#                 ok = False
#         else:
#             ok = False
#     for i in inclusion:
#         if inclusion[i] != 1:
#             ok = False
#     if ok:
#         inclusion_rec = True
#         for i in range(len(is_in) - 1):
#             if not is_include(is_in[i], is_in[i+1]):
#                 inclusion_rec = False
#     return inclusion_rec
#
#
# def compl(contexte):
#     comp = True
#     for i in range(len(contexte[0])):
#         a = np.count_nonzero(contexte[:, i] == 1)
#         complementaire = False
#         for j in range(len(contexte[0])):
#             if i != j:
#                 c = True
#                 for k in range(len(contexte)):
#                     c = c and (contexte[k, j] + contexte[k, i] == 1)
#                 complementaire = complementaire or c
#         comp = complementaire and comp
#     return comp
#
#
# def contexte_to_grid(contexte):
#     n = find_col(contexte)
#     m = find_m(contexte, n)
#     if check_taille(contexte, n, m) and check_size(contexte, n, m) and compl(contexte) and n!=0:
#         all_include = True
#         n_list = []
#         m_list = []
#         for i in range(len(contexte[0])):
#             if np.count_nonzero(contexte[:, i] == 1) == n :
#                 if n_list == []:
#                     n_list.append(contexte[:, i])
#                 else:
#                     if not is_include_part(n_list[0],contexte[:, i]):
#                         n_list.append(contexte[:, i])
#             if m%n != 0:
#                 if np.count_nonzero(contexte[:, i] == 1) == m :
#                     if n_list == []:
#                         n_list.append(contexte[:, i])
#                     else:
#                         if not is_include_part(n_list[0],contexte[:, i]):
#                             n_list.append(contexte[:, i])
#         return trace_grille(n, m)
#
#

def find_col(contexte, n):
    col = None
    i = 0
    while col is None and i < len(contexte[0]):
        a = np.count_nonzero(contexte[:, i] == 1)
        if a == n:
            col = i
        i += 1
    return col

def find_G(contexte, i):
    g = None
    for j in range(len(contexte[0])):
        if i != j:
            c = True
            for k in range(len(contexte)):
                c = c and (contexte[k, j] + contexte[k, i] == 1)
            if c:
                g = j
    return g


def contexte_to_grid_rec(contexte):
    n = find_n(contexte)
    m = find_m(contexte, n)
    i = find_col(contexte, n)
    if len(contexte) == 2 and len(contexte[0]) == 2:
        return np.array_equal(contexte, np.array([[0, 1], [1, 0]])) or np.array_equal(contexte, np.array([[1, 0], [0, 1]]))
    if check_parity(contexte) and check_taille(contexte, n, m) and i is not None:
        g = find_G(contexte, i)
        u = []
        for k in range(len(contexte)):
            if contexte[k, i] == 1:
                u.append(k)
        new_contexte = np.delete(contexte, [i, g], axis=1)
        new_contexte = np.delete(new_contexte, u, axis=0)
        return contexte_to_grid_rec(new_contexte)
    else:
        return False


def contexte_to_grid(contexte):
    n = find_n(contexte)
    m = find_m(contexte, n)
    if contexte_to_grid_rec(contexte):
        return True, n, m
    return False, None, None


print(contexte_to_grid(contexte))


import networkx as nx
import numpy as np
import scipy.special
import itertools

graph = nx.hypercube_graph(3)


def fn(n, source, en_cours, tout):
    if (n == 0):
        if (len(en_cours) > 0):
            tout.append(en_cours)
        return
    for j in range(0, len(source)):
        fn(n - 1, source[j + 1:], en_cours + [source[j]], tout)
    return tout

def find_sg(fixe, n):
    mots_n = itertools.product('01', repeat=n)
    m = len(fixe)
    mots_m = itertools.product('01', repeat=m)
    convexes = {}
    mots_fixes = []
    for mot in mots_m:
        mots_fixes.append(mot)
    for mot in mots_n:
        for mot2 in mots_fixes:
            is_convexe = True
            for i in range(m):
                is_convexe = is_convexe and mot[fixe[i]] == mot2[i]
            if is_convexe:
                if mot2 not in convexes.keys():
                    convexes[mot2] = [mot]
                else:
                    convexes[mot2].append(mot)
    c = []
    for l in convexes:
        c.append(convexes[l])
    return c



def hypercubeToConvexes(graph):
    convexes = [[], list(graph.nodes())]
    dim = np.log2(graph.number_of_nodes())
    for i in range(1, int(dim) + 1):
        fixes = fn(i, np.arange(0, int(dim)), [], [])
        for fixe in fixes:
            c = []
            nb = scipy.special.binom(int(dim), len(fixe))
            convexes = [*convexes, *find_sg(fixe, int(dim))]
    return convexes

def hypercubeToContexte(graph):
    attributs = []
    dim = np.log2(graph.number_of_nodes())
    fixes = fn(1, np.arange(0, int(dim)), [], [])
    for fixe in fixes:
        attributs = [*attributs, *find_sg(fixe, int(dim))]
    objets = []
    for attribut in attributs:
        for objet in attribut:
            if objet not in objets:
                objets.append(objet)
    contexte = []
    for i in range(len(objets)):
        contexte.append([0] * len(attributs))
    for j in range(len(attributs)):
        for i in range(len(objets)):
            if objets[i] in attributs[j]:
                contexte[i][j] = 1
            else:
                contexte[i][j] = 0
    return objets, attributs, contexte



#print(hypercubeToContexte(graph))

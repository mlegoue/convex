import networkx as nx
import numpy as np


contexte = np.array([
     [1, 1, 1, 1, 0, 0, 1, 1],
     [1, 1, 0, 0, 1, 1, 1, 1],
     [0, 0, 1, 1, 1, 1, 1, 1],
     [1, 0, 1, 0, 1, 0, 1, 0],
     [0, 1, 0, 1, 0, 1, 0, 1]
])

def find_u(contexte, objets):
    for j in range(contexte.shape[1]):
        colonne = contexte[:, j]
        if np.count_nonzero(colonne == 0) == 1:
            u = np.where(colonne == 0)[0][0]
            return j, objets[u]
    return None, None

def is_include(colonne1, colonne2):
    include = True
    for i in range(len(colonne1)):
        if (colonne1[i] == 1 and colonne2[i] == 0):
            include = False
    return include

def arrow(c):
    contexte = np.empty([c.shape[0], c.shape[1]], dtype=str)
    for i in range(contexte.shape[0]):
        for j in range(contexte.shape[1]):
            if c[i, j] == 0:
                inc = False
                for k in range(contexte.shape[1]):
                    if k != j:
                        if c[i, k] == 0:
                            inc = inc or is_include(c[:, j], c[:, k])
                if inc:
                    contexte[i, j] = "m"
                else:
                    contexte[i, j] = "M"
            else:
                contexte[i, j] = "X"
    return contexte


def reduce(cwa):
    new_att = []
    for i in range(cwa.shape[1]):
        if not "M" in cwa[:, i]:
            new_att.append(i)
    return new_att


# Génére toutes les parties de a
def parties(a):
    def fn(n, source, en_cours, tout):
        if (n == 0):
            if (len(en_cours) > 0):
                tout.append(en_cours)
            return
        for j in range(0, len(source)):
            fn(n - 1, source[j + 1:], en_cours + [source[j]], tout)
        return
    tout = []
    for i in range(len(a)):
        fn(i, a, [], tout)
    tout.append(a)
    return tout

# Génére toutes les parties de taille 2 à k
def parties_kel(a, k):
    def fn(n, source, en_cours, tout):
        if (n == 0):
            if (len(en_cours) > 0):
                tout.append(en_cours)
            return
        for j in range(0, len(source)):
            fn(n - 1, source[j + 1:], en_cours + [source[j]], tout)
        return
    tout = []
    for i in range(2, k+1):
        fn(i, a, [], tout)
    if k == len(a):
        tout.append(a)
    return tout


def generate_neig(graph):
    nb = nx.graph_clique_number(graph)
    parties = parties_kel(list(graph.nodes()), nb)
    return parties


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


def find_concept_a(a, objets, attributs):
    intention = find_intention(attributs, a)
    extension = find_extension(objets, intention)
    return extension


def contexte_to_attribut(contexte, objets):
    attributs = []
    for j in range(contexte.shape[1]):
        attribut = []
        for i in range(contexte.shape[0]):
            if contexte[i, j] == 1:
                attribut.append(objets[i])
        attributs.append(attribut)
    return attributs


def factorielle(n):
    if n == 0:
        return 1
    else:
        F = 1
        for k in range(2,n+1):
            F = F * k
        return F


## equidistant à au moins 2 noeuds
def equidistant2(noeuds, graph):
    equidi = []
    for n in list(graph.nodes()):
        dist = []
        if n not in noeuds:
            for i in range(0, len(noeuds)):
                dist.append(nx.shortest_path_length(graph, noeuds[i], n))
            for d in dist:
                if dist.count(d) >= 2 and n not in equidi:
                    equidi.append(n)
    return equidi


def equidistant(noeuds, graph):
    equidi = []
    for n in list(graph.nodes()):
        equi = True
        l = nx.shortest_path_length(graph, noeuds[0], n)
        for i in range(1, len(noeuds)):
            equi = equi and (nx.shortest_path_length(graph, noeuds[i], n) == l)
        if equi:
            equidi.append(n)
    return equidi


def find_neig(u, objets, old_contexte, contexte, old_graph, old_objets):
    attributs = contexte_to_attribut(contexte, objets)
    old_attributs = contexte_to_attribut(old_contexte, old_objets)
    parties = generate_neig(old_graph)
    nb_edges = factorielle(old_graph.number_of_nodes())/(2 * factorielle(old_graph.number_of_nodes() - 2))
    edges = parties[:int(nb_edges)]
    no_edges = []
    for edge in edges:
        if not set(edge) == set(find_extension(objets, find_intention(old_attributs, edge))):
            no_edges.append(edge)
            parties.remove(edge)
    a_supp = []
    for partie in parties:
        for no_edge in no_edges:
            if set(no_edge).issubset(partie) and partie not in a_supp:
                a_supp.append(partie)
    for a in a_supp:
        parties.remove(a)
    for attribut in attributs:
        a_supp = []
        for partie in parties:
            set1 = set(attribut)
            set2 = set(partie)
            intersection = list(set1 & set2)
            if len(intersection) == len(partie):
                if u not in attribut and partie not in a_supp:
                    a_supp.append(partie)
                    print("oui1", partie, attribut)
            elif len(intersection) == 0:
                if u in attribut and partie not in a_supp:
                    a_supp.append(partie)
                    print("oui2", partie)
            equi = equidistant(partie, old_graph)
            setequi = set(equi)
            setatt = set(attribut)
            if u in attribut and len(setequi & setatt) >= 1 and partie not in a_supp and len(setatt & set(partie)) < len(partie):
                a_supp.append(partie)
                print("oui3", partie)
        for a in a_supp:
            parties.remove(a)
    return parties


def generate_tri(context, objets):
    graph = nx.Graph()
    for i in range(3):
        arete = []
        for j in range(3):
            if context[j][i] == 1:
                arete.append(objets[j])
        if len(arete) == 2:
            graph.add_edge(arete[0], arete[1])
        else:
            return None
    return graph


def is_cordal_fun(context, objets, equis, all_equi, u, voisins):
    attributs = contexte_to_attribut(context, objets)
    is_cordal = True
    setv = set(voisins)
    sete = set(equis)
    setae = set(all_equi)
    for attribut in attributs:
        seta = set(attribut)
        no_neig_and_not_u = (len(seta & setv) == 0) and (u not in attribut)
        all_neig_and_u = (len(setv & seta) == len(setv)) and (u in attribut)
        no_equi_and_neig_and_u = (len(setae & seta) == 0) and (len(setv & seta) > 0) and (u in attribut)
        equi_and_neig_and_not_u = (len(sete & seta) > 0) and (len(setv & seta) > 0) and (u not in attribut)
        is_cordal = is_cordal and (no_neig_and_not_u or all_neig_and_u or no_equi_and_neig_and_u or equi_and_neig_and_not_u)
    return is_cordal


def context_to_cordal(context, objets):
    j, u = find_u(context, objets)
    new_context = np.delete(context, j, axis=1)
    new_context_w_u = np.delete(new_context, objets.index(u), axis=0)
    liste = reduce(arrow(new_context_w_u))
    new_context_clar = np.delete(new_context_w_u, liste, axis=1)
    new_objets = objets.copy()
    new_objets.remove(u)
    if new_context_clar.shape == (3, 3):
        cordal = generate_tri(new_context_clar, new_objets)
        is_cordal = (cordal != None)
    else:
        is_cordal, cordal = context_to_cordal(new_context_clar, new_objets)
    voisins = find_neig(u, objets, new_context_clar, new_context, cordal, new_objets)[0]
    print(voisins)
    # except:
    #     is_cordal = False
    if not is_cordal:
        return False, None
    equi = equidistant2(voisins, cordal)
    all_equi = equidistant(voisins, cordal)
    is_cordal = is_cordal_fun(new_context, objets, equi, all_equi, u, voisins)
    print(is_cordal)
    if not is_cordal:
        return False, None
    for n in voisins:
        cordal.add_edge(n, u)
    return is_cordal, cordal


# deux_arbre, arbre = context_to_deux_arbre(contexte, [0, 1, 2, 3, 4])
#
# if arbre != None:
#     print(deux_arbre, arbre.edges())
# else:
#     print(deux_arbre)


#print(arrow(contexte))

#print(parties_kel([1, 2, 3, 4, 5], 3))

is_cordal, cordal = context_to_cordal(contexte, [0, 1, 2, 3, 4, 5])

print(is_cordal, "ui")
if is_cordal:
    print(cordal.edges())



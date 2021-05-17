import networkx as nx


def plus_court_chemin(graphe):
    chemin = {}
    for origin in graphe.nodes():
        chemin[origin] = {}
        for destination in graphe.nodes():
            chemin[origin][destination] = list(nx.all_shortest_paths(graphe, origin, destination))
    return chemin


def convex_step(nodes, chemins, new_nodes):
    new = []
    for s1 in new_nodes:
        for s2 in nodes:
            for chemin in chemins[s1][s2]:
                for node in chemin:
                    if node not in nodes and node not in new:
                        new.append(node)
    nodes = nodes + new
    return nodes, new


def convex_hull(chemins, nodes):
    new = nodes
    while new:
        nodes, new = convex_step(nodes, chemins, new)
    return nodes


def in_list(c, convexes):
    vu = False
    for convexe in convexes:
        if set(c) == set(convexe):
            vu = True
    return vu


def in_list_incomp(c, convexes):
    add = True
    a_supp = []
    for convexe in convexes:
        if set(c) == set(convexe):
            add = False
        elif len(c) < len(convexe):
            if set(c).issubset(convexe):
                a_supp.append(convexe)
        elif len(c) > len(convexe):
            if set(convexe).issubset(c):
                add = False
    return add, a_supp


def find_convexes(graphe):
    convexes = [[]]
    attributs = []
    non_vu = []
    chemins = plus_court_chemin(graphe)
    # On ajoute les sommets
    for node in graphe.nodes():
        non_vu.append([node])
        convexes.append([node])
    while non_vu:
        c = non_vu.pop(0)
        for u in graphe.nodes():
            if u not in c:
                candu = convex_hull(chemins, c+[u])
                if not in_list(candu, convexes):
                    convexes.append(candu)
                    non_vu.append(candu)
    return convexes

def find_attributs(graphe):
    convexes = [[]]
    attributs = []
    non_vu = []
    chemins = plus_court_chemin(graphe)
    # On ajoute les sommets
    for node in graphe.nodes():
        non_vu.append([node])
        convexes.append([node])
    while non_vu:
        c = non_vu.pop(0)
        successeurs = []
        for u in graphe.nodes():
            if u not in c:
                candu = convex_hull(chemins, c+[u])
                add, a_supp = in_list_incomp(candu, successeurs)
                for s in a_supp:
                    successeurs.remove(s)
                if add:
                    successeurs.append(candu)
                if not in_list(candu, convexes):
                    convexes.append(candu)
                    non_vu.append(candu)
        if len(successeurs) == 1:
            attributs.append(c)
    return convexes, attributs



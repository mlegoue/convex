import networkx as nx
import matplotlib.pyplot as plt
from Aleatoire.find_convexes import convex_hull, plus_court_chemin, find_attributs, in_list, in_list_incomp

# on considérera que les noeuds arrivent dans l'ordre (0 puis 1 puis 2 puis 3 ...)


def sort_by_nodes(convexes, n):
    sorted = []
    for i in range(n):
        for convexe in convexes:
            if convexe[-1] == i:
                sorted.append(convexe)
    return sorted


def successeurs(convexe, graphe, chemins):
    successeurs = []
    for u in graphe.nodes():
        if u not in convexe:
            candu = convex_hull(chemins, convexe + [u])
            add, a_supp = in_list_incomp(candu, successeurs)
            for c in a_supp:
                successeurs.remove(c)
            if add:
                successeurs.append(candu)
    return successeurs


def draw_lattice(graphe):
    chemins = plus_court_chemin(graphe)
    convexes, attributs = find_attributs(graphe)
    convexes.sort(key=lambda v: len(v))
    convexes_by_size = {}
    for convexe in convexes:
        convexe.sort()
        if len(convexe) in convexes_by_size:
            convexes_by_size[len(convexe)].append(convexe)
        else:
            convexes_by_size[len(convexe)] = [convexe]
    n = len(convexes[-1])
    convexes_graphe = nx.Graph()
    convexes_graphe.add_nodes_from(list(map(lambda convexe: ''.join(list(map(str, convexe))), convexes)))
    positions = {'': (0, 0)}
    success = successeurs([], graphe, chemins)
    for succ in success:
        convexes_graphe.add_edge('', ''.join(list(map(str, succ))))
    for i in range(1, n+1):
        convexes_by_size[i].sort(key=lambda convexe: int(''.join(list(map(str, sorted(convexe, reverse=True))))))
        for convexe in convexes_by_size[i]:
            convexe_str = ''.join(list(map(str, convexe)))
            m = len(convexes_by_size[i])//2
            positions[convexe_str] = (convexes_by_size[i].index(convexe) - m, i)
            success = successeurs(convexe, graphe, chemins)
            for succ in success:
                succ.sort()
                convexes_graphe.add_edge(convexe_str, ''.join(list(map(str, succ))))
    color_map = []
    for convexe in convexes:
        if in_list(convexe, attributs):
            color_map.append('red')
        else:
            color_map.append('blue')
    nx.draw(convexes_graphe, with_labels=True, pos=positions, node_size=100, font_size=8, node_color=color_map)
    plt.show()


G = nx.Graph()
G.add_edges_from([(0, 1), (1, 2), (0, 2), (0, 3), (2, 3), (0, 4), (3, 4), (0, 5), (2, 5), (2, 6), (3, 6), (3, 7), (4, 7), (3, 8), (7, 8)])

draw_lattice(G)
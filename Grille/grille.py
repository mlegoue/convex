import networkx as nx

grilleca = nx.Graph()

grilleca.add_edges_from([(0, 1), (1, 2), (2, 3)])
grilleca.add_edges_from([(4, 5), (5, 6), (6, 7)])
grilleca.add_edges_from([(8, 9), (9, 10), (10, 11)])
grilleca.add_edges_from([(12, 13), (13, 14), (14, 15)])
grilleca.add_edges_from([(16, 17), (17, 18), (18, 19)])

grilleca.add_edges_from([(0, 4), (4, 8), (8, 12), (12, 16)])
grilleca.add_edges_from([(1, 5), (5, 9), (9, 13), (13, 17)])
grilleca.add_edges_from([(2, 6), (6, 10), (10, 14), (14, 18)])
grilleca.add_edges_from([(3, 7), (7, 11), (11, 15), (15, 19)])

#print(attributs_subset(grilleca))

grilletri = nx.Graph()

grilletri.add_edges_from([(1, 2), (2, 3)])
grilletri.add_edges_from([(4, 5), (5, 6), (6, 7)])
grilletri.add_edges_from([(8, 9), (9, 10)])

grilletri.add_edges_from([(1, 4)])
grilletri.add_edges_from([(2, 5), (5, 8)])
grilletri.add_edges_from([(3, 6), (6, 9)])
grilletri.add_edges_from([(7, 10)])

def trace_grille(n, m):
    grid = nx.Graph()
    for i in range(n):
        for j in range(m - 1):
            grid.add_edge(i + (m-1)*j, i + (m-1)*(j+1))
    for j in range(m):
        for i in range(n-1):
            grid.add_edge(i + j*n, i + j*n + 1)
    return grid



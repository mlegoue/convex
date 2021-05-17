from Generation_convexes_attributs.Successeurs.find_convexes import find_attributs
import networkx as nx

graphe = nx.Graph()

graphe.add_edges_from([(0, 1), (1, 2), (0, 2), (1, 4), (1, 3), (4, 3)])

print(find_attributs(graphe))


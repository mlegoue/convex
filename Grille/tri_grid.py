import networkx as nx
from Generation_convexes_attributs.Successeurs.find_convexes import find_attributs

graph = nx.Graph()

graph.add_edges_from([
    (0, 1),
    (1, 2),
    (3, 4),

    (0, 3),
    (1, 3),
    (1, 4),
    (2, 4),
    (3, 5),
    (4, 5),
])

print(find_attributs(graph))
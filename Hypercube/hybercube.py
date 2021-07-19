import networkx as nx
from Generation_convexes_attributs.Successeurs.find_convexes import find_attributs

graph = nx.hypercube_graph(4)

print(graph.edges())
print(find_attributs(graph))

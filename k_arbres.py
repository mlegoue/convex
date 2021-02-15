import networkx as nx
import random

def deux_arbres(n):
    graph = nx.Graph()
    graph.add_edges_from([(0, 1), (0, 2), (1, 2)])
    for i in range(3, n):
        edge = random.choice(list(graph.edges()))
        graph.add_edges_from([(edge[0], i), (edge[1],i)])
    return graph

print(deux_arbres(5).edges())
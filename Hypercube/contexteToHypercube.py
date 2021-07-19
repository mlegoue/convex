import numpy as np
import networkx as nx

contexte = np.array([[1, 1, 1, 0, 0, 0],
                     [1, 1, 0, 0, 0, 1],
                     [1, 0, 1, 1, 0, 0],
                     [1, 0, 0, 1, 0, 1],
                     [0, 1, 1, 0, 1, 0],
                     [0, 1, 0, 0, 1, 1],
                     [0, 0, 1, 1, 1, 0],
                     [0, 0, 0, 1, 1, 1]])


def check_size(contexte):
    x = len(contexte[0])
    y = len(contexte)
    return x % 2 == 0 and y == 2**(x/2)


# def hypercube(contexte):
#     if len(contexte) == 2:
#         if contexte == np.array([[1, 0], [0, 1]]) or contexte == np.array([[0, 1], [1, 0]]):
#             return nx.hypercube_graph(1)
#     else:
#         if check_size(contexte):
#

import networkx as nx
import matplotlib.pyplot as plt

#G = nx.erdos_renyi_graph(10, 0.5)

G = nx.connected_watts_strogatz_graph(10, 4, 0)

G2 = nx.connected_watts_strogatz_graph(10, 4, 0.5)

G3 = nx.barabasi_albert_graph(10, 3)

nx.draw_circular(G, with_labels=True)

plt.show()

nx.draw_circular(G2, with_labels=True)

plt.show()

nx.draw(G3, with_labels=True)

plt.show()
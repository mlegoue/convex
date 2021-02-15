import networkx as nx
from tree_to_context import arbre_to_contexte, display_contexte
import matplotlib.pyplot as plt
from test import hierarchy_pos


#### Arbre ####

# G = nx.Graph()
#
# G.add_edge(1, 2)
# G.add_edge(2, 3)
# G.add_edge(2, 4)
# G.add_edge(1, 5)
# G.add_edge(5, 6)
#
# pos = hierarchy_pos(G, 1)
# nx.draw(G, pos=pos, with_labels=True)
# plt.show()
#
#
# objets, attributs, contexte = arbre_to_contexte(G)
# #display_contexte(objets, attributs, contexte)
#
# from tree_to_context_by_lattice import arbre_to_treillis, treillis_to_contexte
#
# objets2, attributs2, contexte2 = treillis_to_contexte(arbre_to_treillis(G))
# #display_contexte(objets2, attributs2, contexte2)

### 2-arbre ###

from tree_to_context_by_lattice import arbre_to_treillis, treillis_to_contexte
from convex import graphe_to_treillis

G = nx.Graph()

G.add_edge(1, 2)
G.add_edge(1, 3)
G.add_edge(2, 3)



print(graphe_to_treillis(G).edges())

display_contexte(*treillis_to_contexte(graphe_to_treillis(G)))




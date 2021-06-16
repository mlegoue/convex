from Aleatoire.find_convexes import find_attributs
import networkx as nx

graphe = nx.Graph()

graphe.add_edges_from([
    (0, 1),
    (1, 2),
    (0, 2),
    (0, 3),
    (1, 3),
    (2, 3),
    (0, 4),
    (1, 4),
    (2, 4)
])

attributs = find_attributs(graphe)[1]

from Arbres.tree_to_context import display_contexte

from Deux_arbres.deux_arbre_to_contexte import attributs_to_contexte

objets, attributs, contexte = attributs_to_contexte(list(graphe.nodes()), attributs)

print(contexte)

display_contexte(objets, attributs, contexte)




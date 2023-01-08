from Concept.concept import find_concept
import numpy as np
import networkx as nx

# contexte = np.array([
#      [1, 1, 1, 1, 0, 0, 1, 1],
#      [1, 1, 0, 0, 1, 1, 1, 1],
#      [0, 0, 1, 1, 1, 1, 1, 1],
#      [1, 0, 1, 0, 1, 0, 1, 0],
#      [0, 1, 0, 1, 0, 1, 0, 1]
# ])

# ligne 0 = objet 0; ligne 1 = objet 1 ...

def contexte_to_attributs(contexte):
    attributs = []
    objets = []
    for o in range (len(contexte[0])):
        objets.append(str(o))
    for i in range (len(contexte[0])):
        attribut = ''
        for j in range (len(contexte)):
            if contexte[j][i] == 1:
                attribut = attribut + str(j)
        attributs.append(attribut)
    return objets, attributs


def find_graph(contexte):
    graph = nx.Graph()
    objets, attributs = contexte_to_attributs(contexte)
    potential_edges = {}
    for objet in objets:
        for objet2 in objets:
            if objet != objet2 and int(objet) < int(objet2):
                potential_edges[objet + objet2] = [int(objet), int(objet2)]
    concept = find_concept(objets, attributs)
    for convexe in concept:
        if convexe in potential_edges.keys():
            graph.add_edge(potential_edges[convexe][0], potential_edges[convexe][1])
    return graph


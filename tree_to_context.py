import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt

def is_in_list(G, list):
    if list == []:
        return False
    for g in list:
        if (set(G.edges()) == set(g.edges())) and (set(G.nodes()) == set(g.nodes)):
            return True
    return False


def sous_graphe_un_voisin(G):
    aretes = G.edges()
    sous_graphes = []
    for arete in aretes:
        H = G.copy()
        H.remove_edge(*arete)
        components = (H.subgraph(c).copy() for c in nx.connected_components(H))
        for c in components:
            if not is_in_list(c, sous_graphes):
                sous_graphes.append(c.copy())
    return sous_graphes


def arbre_to_contexte(tree):
    if nx.is_tree(tree):
        objets = list(tree.nodes())
        attributs = list(map(lambda subg: ''.join(list(map(str, list(subg.nodes())))), sous_graphe_un_voisin(tree)))
        contexte = []
        for i in range(len(objets)):
            contexte.append([0] * len(attributs))
        for objet in objets:
            for attribut in attributs:
                if str(objet) in attribut:
                    contexte[objets.index(objet)][attributs.index(attribut)] = 1
                else:
                    contexte[objets.index(objet)][attributs.index(attribut)] = 0
        return objets, attributs, contexte
    else:
        print("Ce n'est pas un arbre !")


def display_contexte(objets, attributs, contexte):
    fig, ax = plt.subplots()
    # hide axes
    fig.patch.set_visible(False)
    ax.axis('off')
    ax.axis('tight')

    df = pd.DataFrame(contexte, columns=attributs)
    ax.table(cellText=df.values, colLabels=df.columns, loc='center', rowLabels=objets)
    fig.tight_layout()
    plt.show()


# def is_subgraph(G, H):
#     return (set(G.edges).issubset(set(H.edges)) and set(G.nodes).issubset(set(H.nodes)))
#
# def sous_graphe(G, sous_graphes = []):
#     aretes = G.edges()
#     for arete in aretes:
#         H = G.copy()
#         H.remove_edge(*arete)
#         components = (H.subgraph(c).copy() for c in nx.connected_components(H))
#         for c in components:
#             if not is_in_list(c, sous_graphes):
#                 sous_graphes.append(c.copy())
#                 if c.number_of_nodes() > 1:
#                     sous_graphe(c, sous_graphes)
#     return sous_graphes
#
#
# def subgraph_one_neighbor(G, H):
#     degree = nx.degree(H, G.nodes())
#     sum_degree = 0
#     for noeud in degree:
#         sum_degree += noeud[1]
#     return sum_degree == 2*G.number_of_edges() + 1

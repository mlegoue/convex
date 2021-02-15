import networkx as nx
import matplotlib.pyplot as plt

def is_in_list(G, list):
    if list == []:
        return False
    for g in list:
        if (set(G.edges()) == set(g.edges())) and (set(G.nodes()) == set(g.nodes)):
            return True
    return False


def is_subgraph(G, H):
    return set(G.edges).issubset(set(H.edges)) and set(G.nodes).issubset(set(H.nodes))


def sous_graphe_rec(G, sous_graphes = []):
    aretes = G.edges()
    for arete in aretes:
        H = G.copy()
        H.remove_edge(*arete)
        components = (H.subgraph(c).copy() for c in nx.connected_components(H))
        for c in components:
            if not is_in_list(c, sous_graphes):
                sous_graphes.append(c.copy())
                if c.number_of_nodes() > 1:
                    sous_graphe_rec(c, sous_graphes)
    return sous_graphes


def sous_graphe(G):
    sous_graphes = []
    sous_graphes.append(G)
    empty = nx.Graph()
    sous_graphes.append(empty)
    return sous_graphe_rec(G, sous_graphes)



def arbre_to_treillis(tree):
    subgraphs = sous_graphe(tree)

    dictionnaire_subgraphs = {}

    for subgraph in subgraphs:
        dictionnaire_subgraphs[' '.join(list(map(str, list(subgraph.nodes()))))] = subgraph

    Treillis = nx.DiGraph()

    for i in dictionnaire_subgraphs:
        for j in dictionnaire_subgraphs:
            if is_subgraph(dictionnaire_subgraphs[i], dictionnaire_subgraphs[j]) and (dictionnaire_subgraphs[i].number_of_nodes() == dictionnaire_subgraphs[j].number_of_nodes() - 1):
                Treillis.add_edge(i, j)

    return Treillis

def treillis_to_contexte(treillis):
    objets=[]
    attributs=[]
    for n in treillis.nodes():
        if treillis.in_degree(n) == 1:
            objets.append(n)
        if treillis.out_degree(n) == 1:
            attributs.append(n)
        if treillis.out_degree(n) == 0:
            noeud_final = n

    contexte = []
    for objet in objets:
        attributs_objet = [0]*len(attributs)
        print(objet, noeud_final)
        for chemin in list(nx.shortest_simple_paths(treillis, objet, noeud_final)):
            for noeud in chemin:
                if noeud not in attributs_objet and noeud in attributs:
                    attributs_objet[attributs.index(noeud)] = 1
        contexte.append(attributs_objet)

    return objets, attributs, contexte
import networkx as nx

def is_convex (S, G):
    convex = True
    for u in S.nodes():
        for v in S.nodes():
            spaths = list(nx.all_shortest_paths(G, source=u, target=v))
            for path in spaths:
                for i in range (len(path)-1):
                    if (path[i], path[i+1]) not in S.edges():
                        return False
    return True

def is_in_list(G, list):
    if list == []:
        return False
    for g in list:
        if (set(G.edges()) == set(g.edges())) and (set(G.nodes()) == set(g.nodes)):
            return True
    return False


def is_subgraph(G, H):
    return set(G.edges()).issubset(set(H.edges())) and set(G.nodes()).issubset(set(H.nodes()))


def sous_graphe_rec(G, graphe, sous_graphes = []):
    aretes = G.edges()
    for arete in aretes:
        H = G.copy()
        H.remove_edge(*arete)
        components = (H.subgraph(c).copy() for c in nx.connected_components(H))
        for c in components:
            if not is_in_list(c, sous_graphes):
                if is_convex(c, graphe):
                    sous_graphes.append(c.copy())
                if c.number_of_nodes() > 1:
                    sous_graphe_rec(c, graphe, sous_graphes)
    return sous_graphes


def sous_graphe_convex(G):
    sous_graphes = []
    sous_graphes.append(G)
    empty = nx.Graph()
    sous_graphes.append(empty)
    return sous_graphe_rec(G, G, sous_graphes)



def graphe_to_treillis(tree):
    subgraphs = sous_graphe_convex(tree)

    dictionnaire_subgraphs = {}

    for subgraph in subgraphs:
        dictionnaire_subgraphs[' '.join(list(map(str, list(subgraph.nodes()))))] = subgraph

    Treillis = nx.DiGraph()

    for i in dictionnaire_subgraphs:
        for j in dictionnaire_subgraphs:
            direct = True
            if is_subgraph(dictionnaire_subgraphs[i], dictionnaire_subgraphs[j]):
                if i == j:
                    direct = False
                else:
                    for k in dictionnaire_subgraphs:
                        if i != k and j != k and is_subgraph(dictionnaire_subgraphs[i], dictionnaire_subgraphs[k]) and is_subgraph(dictionnaire_subgraphs[k], dictionnaire_subgraphs[j]):
                            direct = False
                if direct:
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
        for chemin in list(nx.shortest_simple_paths(treillis, objet, noeud_final)):
            for noeud in chemin:
                if noeud not in attributs_objet and noeud in attributs:
                    attributs_objet[attributs.index(noeud)] = 1
        contexte.append(attributs_objet)

    return objets, attributs, contexte

import networkx as nx


def plus_court_chemin(graphe):
    distance = {}
    for origin in graphe.nodes():
        distance[origin] = {}
        for destination in graphe.nodes():
            distance[origin][destination] = nx.shortest_path_length(graphe, origin, destination)
    return distance


def find_isometrique(graph):
    distance = plus_court_chemin(graph)
    iso = []
    i, imax = 0, 2 ** len(list(graph.nodes())) - 1
    while i <= imax:
        sous_graphe = []
        j, jmax = 0, len(list(graph.nodes())) - 1
        is_iso = True
        while j <= jmax:
            if (i >> j) & 1 == 1:
                sous_graphe.append(list(graph.nodes())[j])
            j += 1
        if sous_graphe == [] or nx.is_connected(graph.subgraph(sous_graphe)):
            for origin in sous_graphe:
                for destination in sous_graphe:
                    is_iso = is_iso and (distance[origin][destination] == nx.shortest_path_length(graph.subgraph(sous_graphe), origin, destination))
            if is_iso:
                iso.append(sous_graphe)
        i = i + 1
        print(i, imax)
    return iso


graph = nx.hypercube_graph(3)
print(find_isometrique(graph))
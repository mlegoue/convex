import networkx as nx

G = nx.Graph()

G.add_edge(1, 2)
G.add_edge(1, 3)
G.add_edge(2, 3)
G.add_edge(2, 4)
G.add_edge(1, 4)
G.add_edge(3, 5)
G.add_edge(2, 5)
G.add_edge(2, 6)
G.add_edge(5, 6)
G.add_edge(5, 7)
G.add_edge(6, 7)


def roy_floyd_warshall(graph):
    distances = {}
    steps = {}
    for origin in graph.nodes():
        steps[origin] = {}
        distances[origin] = {}
        voisins_origin = [n for n in graph[origin]]
        for destination in graph.nodes():
            steps[origin][destination] = []
            distances[origin][destination] = float('inf')
            if destination in voisins_origin:
                distances[origin][destination] = 1
        distances[origin][origin] = 0
    for step in graph.nodes():
        for origin in graph.nodes():
            for destination in graph.nodes():
                print(origin, step, destination, distances[origin][step], distances[step][destination])
                if distances[origin][step] + distances[step][destination] <= distances[origin][destination]:
                    distances[origin][destination] = distances[origin][step] + distances[step][destination]
                    steps[origin][destination] += [step]
    return steps, distances

#print(roy_floyd_warshall(G))

def floyd_warshall(graph):
    n = graph.number_of_nodes()
    M = []
    chemin = {}
    for i in range(n):
        M.append([float('inf')]*n)
    for i in G.nodes():
        print(i)
        chemin[i] = {}
        for j in G.nodes():
            voisins_origin = [n for n in graph[i]]
            if i == j:
                M[i-1][j-1] = 0
                chemin[i][j] = [[i]]
            elif j in voisins_origin:
                M[i-1][j-1] = 1
                chemin[i][j] = [[i, j]]
    for k in G.nodes():
        print(k)
        for i in G.nodes():
            print(i)
            for j in G.nodes():
                print(j)
                ancien_min = M[i-1][j-1]
                if ancien_min < M[i-1][k-1] + M[k-1][j-1]:
                    chemin[i][j] = [chemin[i][k]+chemin[k][j]]
                if ancien_min == M[i-1][k-1] + M[k-1][j-1]:
                    for partie1 in chemin[i][k]:
                        for partie2 in chemin[k][j]:
                            chemin[i][j].append(partie1+partie2)
    return M, chemin

print(floyd_warshall(G))

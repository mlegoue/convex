import networkx as nx

graphe = nx.DiGraph()
graphe.add_edges_from([(1, 3), (3, 6), (6, 7), (1, 4), (4, 7), (2, 4), (2, 5)])

CC = []
A = []

visited = {}
low = {}
seq = {}
parent = {}

for node in graphe.nodes():
    visited[node] = False
    parent[node] = None
    low[node] = float('+inf')




def TD(C, F):
    print(list(C.nodes()), F)
    CC.append(list(C.nodes()))
    A = []
    for node in C:
        visited[node] = False
        parent[node] = None
        low[node] = float('inf')
        seq[node] = float('inf')
    count = 0
    for u in C:
        if visited[u] == False:
            DFS2(u, C, count, visited, seq, low, parent, A)
    Y = list((set(C.nodes()) - set(F)) - set(A))
    for s in Y:
        if list(C.successors(s)) == [] or list(C.predecessors(s)) == []:
            Cp = C.copy()
            Cp.remove_node(s)
            TD(Cp, F.copy())
            F.append(s)



def DFS(u, visited, seq, low, parent, A):
    global count
    visited[u] = True
    count += 1
    seq[u] = count
    low[u] = count
    children = 0
    for v in (list(graphe.successors(u)) + list(graphe.predecessors(u))):
        if visited[v] == False:
            children += 1
            parent[v] = u
            DFS(v, visited, seq, low, parent, A)
            low[u] = min(low[u], low[v])
            if parent[u] == None and children > 1:
                A.append(u)
            if parent[u] != None and low[v] >= seq[u]:
                A.append(u)
        elif v != parent[u]:
            low[u] = min(low[u], seq[u])

def DFS2(u, C, count, visited, seq, low, parent, A):
    visited[u] = True
    count += 1
    seq[u] = count
    low[u] = count
    children = 0
    for v in (list(C.successors(u)) + list(C.predecessors(u))):
        if visited[v] == False:
            children += 1
            parent[v] = u
            DFS2(v, C, count, visited, seq, low, parent, A)
            low[u] = min(low[u], low[v])
            if parent[u] == None and children > 1:
                A.append(u)
            if parent[u] != None and low[v] >= seq[u]:
                A.append(u)
        elif v != parent[u]:
            low[u] = min(low[u], seq[v])

TD(graphe, [])

print(seq, low, parent)
print(CC)
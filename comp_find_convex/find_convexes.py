import networkx as nx
import time
import matplotlib.pyplot as plt
import csv

def plus_court_chemin(graphe):
    chemin = {}
    for origin in graphe.nodes():
        chemin[origin] = {}
        for destination in graphe.nodes():
            chemin[origin][destination] = list(nx.all_shortest_paths(graphe, origin, destination))
    return chemin


def convex_step(nodes, chemins, new_nodes):
    new = []
    for s1 in new_nodes:
        for s2 in nodes:
            for chemin in chemins[s1][s2]:
                for node in chemin:
                    if node not in nodes and node not in new:
                        new.append(node)
    nodes = nodes + new
    return nodes, new


def convex_hull(chemins, nodes):
    new = nodes
    while new:
        nodes, new = convex_step(nodes, chemins, new)
    return nodes


def in_list(c, convexes):
    vu = False
    for convexe in convexes:
        if set(c) == set(convexe):
            vu = True
    return vu

def in_list_incomp(c, convexes):
    add = True
    a_supp = []
    for convexe in convexes:
        if set(c) == convexe:
            add = False
        elif len(c) < len(convexe):
            if set(c).issubset(convexe):
                a_supp.append(convexe)
        elif len(c) > len(convexe):
            if set(convexe).issubset(c):
                add = False
    return add, a_supp

def find_convexes(graphe):
    convexes = [[]]
    attributs = []
    non_vu = []
    chemins = plus_court_chemin(graphe)
    # On ajoute les sommets
    for node in graphe.nodes():
        non_vu.append([node])
        convexes.append([node])
    while non_vu:
        #print(len(convexes))
        c = non_vu.pop(0)
        successeurs = []
        for u in graphe.nodes():
            if u not in c:
                candu = convex_hull(chemins, c+[u])
                add, a_supp = in_list_incomp(candu, successeurs)
                for c in a_supp:
                    successeurs.remove(c)
                if add:
                    successeurs.append(candu)
                if not in_list(candu, convexes):
                    convexes.append(candu)
                    non_vu.append(candu)
        if len(successeurs) == 1:
            attributs.append(c)
    return convexes, attributs



### Comparaison

from floyd_warshall_2 import attributs_subset

x = [*range(2, 21)]
time1 = []
time2 = []

with open('time_find_convex.csv', 'w', newline='') as csvfilefc :
    spamwriterfc = csv.writer(csvfilefc)
    with open('time_attributs_subset.csv', 'w', newline='') as csvfilecs:
        spamwritercs = csv.writer(csvfilecs)
        for n in range(2, 21):
            print(n)
            somme1 = 0
            somme2 = 0
            temps1 = []
            temps2 = []
            for i in range(500):
                G = nx.erdos_renyi_graph(n, 0.5)
                while not nx.is_connected(G):
                    G = nx.erdos_renyi_graph(n, 0.5)
                t1 = time.time()
                convexes1 = find_convexes(G)
                t2 = time.time()
                convexes2 = attributs_subset(G)
                t3 = time.time()
                somme1 += (t2 - t1)
                somme2 += (t3 - t2)
                temps1.append(t2 - t1)
                temps2.append(t3 - t2)
            spamwriterfc.writerow(temps1)
            spamwritercs.writerow(temps2)
            time1.append(somme1/500)
            time2.append(somme2/500)


with open('time_total.csv', 'w', newline='') as csvfilett :
    spamwritertt = csv.writer(csvfilett)
    spamwritertt.writerow(time1)
    spamwritertt.writerow(time2)

plt.plot(x, time1, label='new find attributs')
plt.plot(x, time2, label='old find attributs')
plt.xlabel("Nombre de noeuds")
plt.ylabel("Temps en ns")
plt.title("Comparaison de temps d'execution pour 500 essais")
plt.legend()
plt.savefig("comp_time.png")

import csv
import networkx as nx
from Aleatoire.find_convexes import find_convexes
import time
import matplotlib.pyplot as plt

x = [*range(2, 30)]
time1 = []

with open('time_new_find_convex.csv', 'w', newline='') as csvfilefc :
    spamwriterfc = csv.writer(csvfilefc)
    for n in range(2, 30):
        somme1 = 0
        somme2 = 0
        temps1 = []
        temps2 = []
        for i in range(500):
            print(n, i)
            G = nx.erdos_renyi_graph(n, 0.5)
            while not nx.is_connected(G):
                G = nx.erdos_renyi_graph(n, 0.5)
            t1 = time.time()
            convexes1 = find_convexes(G)
            t2 = time.time()
            somme1 += (t2 - t1)
            temps1.append(t2 - t1)
        spamwriterfc.writerow(temps1)
        time1.append(somme1/500)


with open('time_total.csv', 'w', newline='') as csvfilett :
    spamwritertt = csv.writer(csvfilett)
    spamwritertt.writerow(time1)


plt.plot(x, time1, label='new find convex')
plt.xlabel("Nombre de noeuds")
plt.ylabel("Temps en s")
plt.title("Temps d'execution moyen sur 500 graphes de Erdos-Renyi avec p = 0.5")
plt.legend()
plt.savefig("time_new_fc.png")
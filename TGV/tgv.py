import networkx as nx
import matplotlib.pyplot as plt

carte = nx.Graph()

f = open('./data/stops.txt','r')
start = f.readline()
arrets = {}
lines = f.readlines()
for line in lines:
    tab_arret = line.split(',')
    carte.add_node(tab_arret[1], pos=(float(tab_arret[4]), float(tab_arret[3])))
    print(line)
    arrets[tab_arret[0]] = tab_arret[1]
f.close()


f2 = open('./data/transfers.txt','r')
start = f2.readline()
lines = f2.readlines()
for line in lines:
    tab_transfert = line.split(',')
    print(tab_transfert)
    print(arrets[tab_transfert[0]], arrets[tab_transfert[1]])
    if arrets[tab_transfert[0]] != arrets[tab_transfert[1]]:
        carte.add_edge(arrets[tab_transfert[0]], arrets[tab_transfert[1]])
f2.close()

pos=nx.get_node_attributes(carte,'pos')
nx.draw(carte, with_labels=True, pos=pos)
plt.show()
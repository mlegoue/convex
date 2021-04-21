import os
import csv
import matplotlib.pyplot as plt
from scipy.stats import linregress
import math

nb_noeuds = []
nb_convexes = []
nb_attributs = []

def traitement(name):
    list_dir = os.listdir(name)
    for dir in list_dir:
        file = open(name + '/' + dir + '/attributs.csv')
        reader = csv.reader(file)
        read_nodes = file.readline()
        nodes = read_nodes.split(",")
        nb_nodes = len(nodes)
        read_edges = file.readline()
        edges = read_edges.split(",")
        nb_edges = len(edges)
        read_nb = file.readline()
        nb = read_nb.split(",")
        nbc = int(nb[0])
        nba = int(nb[1])
        nb_noeuds.append(nb_nodes)
        nb_convexes.append(nbc)
        nb_attributs.append(nba)


traitement("Barabasi_Albert")

traitement("Erdos_Renyi")

traitement("Watts_Strogatz")

plt.figure()
plt.subplot(121)
plt.plot(nb_noeuds, nb_convexes, '+', label="convexes")

plt.figure()
plt.subplot(121)
plt.plot(nb_noeuds, nb_attributs, '+', label="attributs")

ln_attributs = list(map(math.log, nb_attributs))
plt.subplot(122)
plt.plot(nb_noeuds, ln_attributs, '+', label="ln attributs")
a, b, r, p_value, std_err = linregress(nb_noeuds, ln_attributs)
print(a, b, r)
plt.plot(  # droite de regression
    [1, 12],  # valeurs de x
    [a * 1 + b, a * 12 + b],  # valeurs de y
    "r-",  # couleur rouge avec un trait continu
    label="regression")  # legende
plt.xlabel("Nombre de noeuds")  # nom de l'axe x
plt.legend()  # la legende

plt.show()
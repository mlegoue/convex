import csv
import matplotlib.pyplot as plt
import math


times_find = {}
times_subset = {}
total= {}

with open('attributs_res_20_2/time_find_convex.csv', 'r') as file:
    reader = csv.reader(file)
    nb_nodes = 2
    for row in reader:
        mapped_row = list(map(float, row))
        times_find[nb_nodes] = mapped_row
        nb_nodes += 1

with open('attributs_res_20_2/time_attributs_subset.csv', 'r') as file:
    reader = csv.reader(file)
    nb_nodes = 2
    for row in reader:
        mapped_row = list(map(float, row))
        times_subset[nb_nodes] = mapped_row
        nb_nodes += 1

with open('attributs_res_20_2/time_total.csv', 'r') as file:
    reader = csv.reader(file)
    i = 0
    for row in reader:
        mapped_row = list(map(float, row))
        total[i] = mapped_row
        i += 1

def trace_pts_find(x, times):
    plt.plot([x]*100, times[x], '+', color='b')

def trace_pts_subset(x, times):
    plt.plot([x]*100, times[x], '+', color='g')

plt.figure()

# for i in range(2, 21):
#     trace_pts_find(i, times_find)
#     trace_pts_subset(i, times_subset)

plt.plot([*range(2, 21)], total[0], 'g', label="new find attributes")
plt.plot([*range(2, 21)], total[1], 'r', label="old find attributes")
plt.title("Comparaison du temps d'execution moyen sur 100 graphes de Erdos-Renyi avec p = 0.5")
plt.xlabel("Nombre de noeuds")
plt.ylabel("Temps d'execution en s")
#plt.xlim([1, 13])
#plt.ylim([0, total[1][11]])
plt.xticks([*range(2, 21)])
plt.legend()
plt.show()

plt.figure()




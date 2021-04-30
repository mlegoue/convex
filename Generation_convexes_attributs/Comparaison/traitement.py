import csv
import matplotlib.pyplot as plt
import math


times_find = {}
times_subset = {}
total= {}

with open('res_20/time_find_convex.csv', 'r') as file:
    reader = csv.reader(file)
    nb_nodes = 2
    for row in reader:
        mapped_row = list(map(float, row))
        times_find[nb_nodes] = mapped_row
        nb_nodes += 1

with open('res_20/time_convex_subset.csv', 'r') as file:
    reader = csv.reader(file)
    nb_nodes = 2
    for row in reader:
        mapped_row = list(map(float, row))
        times_subset[nb_nodes] = mapped_row
        nb_nodes += 1

with open('res_20/time_total.csv', 'r') as file:
    reader = csv.reader(file)
    i = 0
    for row in reader:
        mapped_row = list(map(float, row))
        total[i] = mapped_row
        i += 1

def trace_pts_find(x, times):
    plt.plot([x]*500, times[x], '+', color='b')

def trace_pts_subset(x, times):
    plt.plot([x]*500, times[x], '+', color='g')

plt.figure()

# for i in range(2, 21):
#     trace_pts_find(i, times_find)
#     trace_pts_subset(i, times_subset)

plt.plot([*range(2, 21)], total[0], 'g', label="new find convex")
plt.plot([*range(2, 21)], total[1], 'r', label="old find convex")
plt.title("Comparaison du temps d'execution moyen sur 500 graphes de Erdos-Renyi avec p = 0.5")
plt.xlabel("Nombre de noeuds")
plt.ylabel("Temps d'execution en s")
plt.xlim([2, 12])
plt.ylim([0, total[1][10]])
plt.xticks([*range(2, 13)])
plt.legend()
plt.show()

plt.figure()




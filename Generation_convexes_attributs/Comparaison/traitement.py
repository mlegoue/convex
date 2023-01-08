import csv
import matplotlib.pyplot as plt
import math
from scipy.stats import linregress
import numpy as np

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

def regression_exp(y,title):
    plt.figure()
    a_min, b_min, r_min, p_value_min, std_err_min = linregress(np.arange(2, 21), np.log(np.array(y)))
    plt.plot(np.arange(2, 21), np.array(y), label="Temps d'exécution")
    print(b_min)
    plt.plot(np.arange(2, 21), np.exp(b_min + a_min * np.arange(2, 21)), label="$y = e^{" + str(round(b_min, 2)) + '+' + str(round(a_min, 2)) + 'x} - r = ' + str(
                 round(r_min, 3)) + "$")
    coefs = np.polyfit(np.arange(2, 21), np.array(y), 2)
    R2 = ((coefs[0] * np.arange(2, 21) ** 2 + coefs[1] * np.arange(2, 21) + coefs[2] - np.array(y).mean()) ** 2).sum() / ((np.array(y) - np.array(y).mean()) ** 2).sum()
    plt.plot(np.arange(2, 21), coefs[0] * np.arange(2, 21) ** 2 + coefs[1] * np.arange(2, 21) + coefs[2], label="$y = " + str(round(coefs[0], 2)) + 'x^2 + ' + str(round(coefs[1], 2)) + 'x + ' + str(
                 round(coefs[2], 2)) + ' - r = ' + str(round(np.sqrt(R2), 3)) + '$')
    plt.title(title)
    plt.legend()


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

regression_exp(total[1], "Algorithme naïf")
regression_exp(total[0], "Amélioration de l'algorithme")

plt.show()





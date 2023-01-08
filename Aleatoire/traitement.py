import json
import csv
import matplotlib.pyplot as plt
from scipy.stats import linregress
import os
import numpy as np
from scipy import interpolate
from statistics import *

def traitement(name, y):
    list_dir = os.listdir(name)
    coords = []
    for dir in list_dir:
        list_dir2 = os.listdir(name + '/' + dir)
        for dir2 in list_dir2:
            print(dir, dir2)
            try:
                with open(name + '/' + dir + '/' + dir2 + '/data.txt') as json_file:
                    data = json.load(json_file)
                coord = (data["nb_nodes"], data[y])
                coords.append(coord)
            except:
                print("oups", dir, dir2)
    return coords


def traitement_nodes(name, x, y):
    list_dir = os.listdir(name)
    coords = []
    for dir in list_dir:
        list_dir2 = os.listdir(name + '/' + dir)
        for dir2 in list_dir2:
            print(dir, dir2)
            with open(name + '/' + dir + '/' + dir2 + '/data.txt') as json_file:
                data = json.load(json_file)
            for n in data[x]:
                coord = (data[x][n], data[y][n])
                coords.append(coord)
    return coords


def traitement_nb_nodes_minmoymaxvar(name, n, y):
    list_dir = os.listdir(name)
    l = []
    for dir in list_dir:
        if dir.startswith('n' + str(n)):
            list_dir2 = os.listdir(name + '/' + dir)
            for dir2 in list_dir2:
                with open(name + '/' + dir + '/' + dir2 + '/data.txt') as json_file:
                    data = json.load(json_file)
                if data["nb_nodes"] == n:
                    l.append(data[y])
    return min(l), mean(l), max(l), variance(l)


def traitement_par_nb_nodes(name, y, nb_max):
    coords = []
    for n in range(3, nb_max + 1):
        coords.append(traitement_nb_nodes_minmoymaxvar(name, n, y))
    return coords


def traitement_nb_nodes(name, n, y):
    list_dir = os.listdir(name)
    l = []
    for dir in list_dir:
        if dir.startswith('n' + str(n)):
            list_dir2 = os.listdir(name + '/' + dir)
            for dir2 in list_dir2:
                with open(name + '/' + dir + '/' + dir2 + '/data.txt') as json_file:
                    data = json.load(json_file)
                if data["nb_nodes"] == n:
                    l.append(data[y])
    return l


def traitement_par_nb_nodes_list(list, y, nb_max):
    coords = []
    for n in range(3, nb_max + 1):
        l = []
        mini = []
        moy = []
        maxi = []
        var = []
        for name in list:
            try:
                coord = traitement_nb_nodes_minmoymaxvar(name, n, y)
                mini.append(coord[0])
                moy.append(coord[1])
                maxi.append(coord[2])
                var.append(coord[3])
            except:
                print("oups", name, n)
        coords.append((min(mini), mean(moy), max(maxi), variance(var)))
    return coords


def traitement_diam(name):
    list_dir = os.listdir(name)
    l = []
    for dir in list_dir:
        list_dir2 = os.listdir(name + '/' + dir)
        for dir2 in list_dir2:
            with open(name + '/' + dir + '/' + dir2 + '/data.txt') as json_file:
                data = json.load(json_file)
            l.append((data["nb_nodes"], data["diameter"], data["nb_attributs"]))
    return l


def traitement_dens(name):
    list_dir = os.listdir(name)
    l = []
    for dir in list_dir:
        list_dir2 = os.listdir(name + '/' + dir)
        for dir2 in list_dir2:
            print(dir, dir2)
            with open(name + '/' + dir + '/' + dir2 + '/data.txt') as json_file:
                data = json.load(json_file)
            l.append((data["nb_nodes"], data["density"], data["nb_attributs"]))
    return l


# plt.plot(np.arange(3, 18), np.array(l1[1]), label="Barabasi_Albert")
# plt.plot(np.arange(3, 21), np.array(l2[1]), label="Erdos_Renyi")
# plt.plot([3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17], l[1])
# plt.legend()
# plt.show()


def regression_exp(y, n, title):
    a_min, b_min, r_min, p_value_min, std_err_min = linregress(np.arange(3, n + 1), np.log(np.array(y[0])))
    a_max, b_max, r_max, p_value_max, std_err_max = linregress(np.arange(3, n + 1), np.log(np.array(y[1])))
    plt.plot(np.arange(3, n + 1), np.log(np.array(y[0])), label="Minimum")
    plt.plot(np.arange(3, n + 1), a_min * np.arange(3, n + 1) + b_min, label="Regression exponentielle minimum")
    plt.plot(np.arange(3, n + 1), np.log(np.array(y[1])), label="Maximum")
    plt.plot(np.arange(3, n + 1), a_max * np.arange(3, n + 1) + b_max, label="Regression exponentielle maximum")
    plt.title(title)
    plt.legend()


def regression_poly_et_exp(y, n, title):
    plt.figure()

    a_min, b_min, r_min, p_value_min, std_err_min = linregress(np.arange(3, n + 1), np.log(np.array(y[0])))
    a_moy, b_moy, r_moy, p_value_moy, std_err_moy = linregress(np.arange(3, n + 1), np.log(np.array(y[1])))
    a_max, b_max, r_max, p_value_max, std_err_max = linregress(np.arange(3, n + 1), np.log(np.array(y[2])))

    plt.subplot(221)
    plt.plot(np.arange(3, n + 1), np.array(y[0]), '+', label="Minimum")
    plt.plot(np.arange(3, n + 1), np.exp(b_min + a_min * np.arange(3, n + 1)),
             label="$y = " + str(round(np.exp(b_min), 2)) + 'e^{' + str(round(a_min, 2)) + 'x} - r = ' + str(
                 round(r_min, 3)) + '$')
    coefs = np.polyfit(np.arange(3, n + 1), np.array(y[0]), 2)
    R2 = ((coefs[0] * np.arange(3, n + 1) ** 2 + coefs[1] * np.arange(3, n + 1) + coefs[2] - np.array(
        y[0]).mean()) ** 2).sum() / ((np.array(y[0]) - np.array(y[0]).mean()) ** 2).sum()
    plt.plot(np.arange(3, n + 1), coefs[0] * np.arange(3, n + 1) ** 2 + coefs[1] * np.arange(3, n + 1) + coefs[2],
             label="$y = " + str(round(coefs[0], 2)) + 'x^2 + ' + str(round(coefs[1], 2)) + 'x + ' + str(
                 round(coefs[2], 2)) + ' - r = ' + str(round(np.sqrt(R2), 3)) + '$')
    plt.title(title + ' - Minimum')
    plt.legend()
    plt.xlim([2, n + 1])
    plt.xticks(np.arange(3, n + 1))
    plt.xlabel("Nombre de noeuds")
    plt.ylabel("Nombre d'attributs minimal")

    plt.subplot(222)
    plt.plot(np.arange(3, n + 1), np.array(y[1]), '+', label="Moyenne")
    plt.plot(np.arange(3, n + 1), np.exp(b_moy + a_moy * np.arange(3, n + 1)),
             label="$y = " + str(round(np.exp(b_moy), 2)) + 'e^{' + str(round(a_moy, 2)) + 'x} - r = ' + str(
                 round(r_moy, 3)) + '$')
    coefs = np.polyfit(np.arange(3, n + 1), np.array(y[1]), 2)
    R2 = ((coefs[0] * np.arange(3, n + 1) ** 2 + coefs[1] * np.arange(3, n + 1) + coefs[2] - np.array(
        y[1]).mean()) ** 2).sum() / ((np.array(y[1]) - np.array(y[1]).mean()) ** 2).sum()
    plt.plot(np.arange(3, n + 1), coefs[0] * np.arange(3, n + 1) ** 2 + coefs[1] * np.arange(3, n + 1) + coefs[2],
             label="$y = " + str(round(coefs[0], 2)) + 'x^2 + ' + str(round(coefs[1], 2)) + 'x + ' + str(
                 round(coefs[2], 2)) + ' - r = ' + str(round(np.sqrt(R2), 3)) + '$')
    plt.title(title + ' - Moyenne')
    plt.legend()
    plt.xlim([2, n + 1])
    plt.xticks(np.arange(3, n + 1))
    plt.xlabel("Nombre de noeuds")
    plt.ylabel("Nombre d'attributs moyen")

    plt.subplot(223)
    plt.plot(np.arange(3, n + 1), np.array(y[2]), '+', label="Maximum")
    plt.plot(np.arange(3, n + 1, 0.1), np.exp(b_max + a_max * np.arange(3, n + 1, 0.1)),
             label="$y = " + str(round(np.exp(b_max), 2)) + 'e^{' + str(round(a_max, 2)) + 'x} - r = ' + str(
                 round(r_max, 3)) + '$')
    coefs = np.polyfit(np.arange(3, n + 1), np.array(y[2]), 2)
    R2 = ((coefs[0] * np.arange(3, n + 1) ** 2 + coefs[1] * np.arange(3, n + 1) + coefs[2] - np.array(
        y[2]).mean()) ** 2).sum() / ((np.array(y[2]) - np.array(y[2]).mean()) ** 2).sum()
    plt.plot(np.arange(3, n + 1, 0.1),
             coefs[0] * np.arange(3, n + 1, 0.1) ** 2 + coefs[1] * np.arange(3, n + 1, 0.1) + coefs[2],
             label="$y = " + str(round(coefs[0], 2)) + 'x^2 + ' + str(round(coefs[1], 2)) + 'x + ' + str(
                 round(coefs[2], 2)) + ' - r = ' + str(round(np.sqrt(R2), 3)) + '$')
    plt.title(title + ' - Maximum')
    plt.legend()
    plt.xlim([2, n + 1])
    plt.xticks(np.arange(3, n + 1))
    plt.xlabel("Nombre de noeuds")
    plt.ylabel("Nombre d'attributs maximal")

    plt.subplot(224)
    plt.plot(np.arange(3, n + 1), np.array(y[3]), '+', label="Variance")
    plt.title(title + ' - Variance')
    plt.legend()
    plt.xlim([2, n + 1])
    plt.xticks(np.arange(3, n + 1))
    plt.xlabel("Nombre de noeuds")
    plt.ylabel("Variance")


# ### Barabasi-Albert : Maximum, Minimum, Moyenne, Variance et Nuage de points ###
#
# data_ba = traitement("Barabasi_Albert", "nb_attributs")
# l1 = [*zip(*data_ba)]
# plt.figure()
# plt.plot(np.array(l1[0]), np.array(l1[1]), '+')
# plt.title("Nombre d'attributs en fonction du nombre de sommets - Barabasi-Albert")
# plt.xlim([2, 17])
# plt.xticks(np.arange(3, 17))
# plt.xlabel("Nombre de noeuds")
# plt.ylabel("Nombre d'attributs")
#
# data_ba = traitement_par_nb_nodes("Barabasi_Albert", "nb_attributs", 17)
# l1 = [*zip(*data_ba)]
# regression_poly_et_exp(l1, 17, "Barabasi-Albert")
#
#
# ### Erdos-Renyi : Maximum, Minimum, Moyenne, Variance et Nuage de points ###
#
# data_er = traitement("Erdos_Renyi", "nb_attributs")
# l2 = [*zip(*data_er)]
# plt.figure()
# plt.plot(np.array(l2[0]), np.array(l2[1]), '+')
# plt.title("Nombre d'attributs en fonction du nombre de sommets - Erdos-Renyi")
# plt.xlim([2, 22])
# plt.xticks(np.arange(3, 22))
# plt.xlabel("Nombre de noeuds")
# plt.ylabel("Nombre d'attributs")
#
#
# data_er = traitement_par_nb_nodes("Erdos_Renyi", "nb_attributs", 21)
# l2 = [*zip(*data_er)]
# regression_poly_et_exp(l2, 21, "Erdos-Renyi")
#
#
# ### Watts-Strogatz : Maximum, Minimum, Moyenne, Variance et Nuage de points ###
#
#
# data_ws = traitement("Watts_Strogatz", "nb_attributs")
# l3 = [*zip(*data_ws)]
# plt.figure()
# plt.plot(np.array(l3[0]), np.array(l3[1]), '+')
# plt.title("Nombre d'attributs en fonction du nombre de sommets - Watts-Strogatz")
# plt.xlim([2, 16])
# plt.xticks(np.arange(3, 16))
# plt.xlabel("Nombre de noeuds")
# plt.ylabel("Nombre d'attributs")
#
# data_ws = traitement_par_nb_nodes("Watts_Strogatz", "nb_attributs", 15)
# l3 = [*zip(*data_ws)]
# regression_poly_et_exp(l3, 15, "Watts-Strogatz")

data_all = traitement_par_nb_nodes_list(["Erdos_Renyi", "Watts_Strogatz", "Barabasi_Albert"], "nb_attributs", 21)
l3 = [*zip(*data_all)]
regression_poly_et_exp(l3, 21, "Tous")
plt.figure()
plt.plot(np.array(l3[0]), np.array(l3[1]), '+')
plt.title("Nombre d'attributs en fonction du nombre de sommets")
plt.xlim([2, 22])
plt.xticks(np.arange(3, 21))
plt.xlabel("Nombre de noeuds")
plt.ylabel("Nombre d'attributs")

#
# data_dens_ba = traitement_dens("Watts_Strogatz")
# l = [*zip(*data_dens_ba)]
#
# colors = []
#
# n_col = {
#     3: "black",
#     4: "gray",
#     5: "brown",
#     6: "red",
#     7: "salmon",
#     8: "orange",
#     9: "yellow",
#     10: "greenyellow",
#     11: "limegreen",
#     12: "lime",
#     13: "turquoise",
#     14: "cyan",
#     15: "deepskyblue",
#     16: "blue",
#     17: "indigo",
#     18: "purple",
#     19: "fuchsia",
#     20: "hotpink",
#     21: "pink",
# }
#
# for n in l[0]:
#     colors.append(n_col[n])
#
# for i in range(len(l[0])):
#     plt.plot(l[2][i], l[1][i], '+', color=colors[i])
# plt.title("Densité en fonction du nombre d'attributs")
# plt.ylabel("Densité")
# plt.xlabel("Nombre d'attributs")
#
# plt.figure()
# data_diam_ba = traitement_diam("Watts_Strogatz")
# l = [*zip(*data_diam_ba)]
#
# colors = []
#
#
# for n in l[0]:
#     colors.append(n_col[n])
#
# for i in range(len(l[0])):
#     plt.plot(l[2][i], l[1][i], '+', color=colors[i])
# plt.title("Diamètre en fonction du nombre d'attributs")
# plt.ylabel("Diamètre")
# plt.xlabel("Nombre d'attributs")

# plt.figure()
# plt.plot(np.arange(3, 18, 0.01), y)
# plt.plot(np.arange(3, 18), np.array(l1[1]), '+')

# data_all = traitement_par_nb_nodes_list(["Barabasi_Albert", "Erdos_Renyi", "Watts_Strogatz"], "nb_attributs", 20)
# l_all = [*zip(*data_all)]
#
# plt.figure()
# plt.plot(np.arange(3, 21), np.array(l_all[0]), label="Minimum")
# plt.plot(np.arange(3, 21), np.array(l_all[1]), label="Maximum")
# data = traitement("Barabasi_Albert", "nb_attributs") + traitement("Erdos_Renyi", "nb_attributs") + traitement("Watts_Strogatz", "nb_attributs")
#
# plt.plot(*zip(*data), '+')

## Pour déterminer le nombre de points à chaque coordonnée


## Poucentage à chaque coordonnées

# nb_graphe = {}
# for n in range(3, 21):
#     somme = 0
#     for a in range(l_all[0][n - 3], l_all[1][n - 3] + 1):
#         nb = data.count((n, a))
#         somme += nb
#     nb_graphe[n] = somme
#
# for n in range(3, 21):
#     for a in range(l_all[0][n-3], l_all[1][n-3]+1):
#         nb = (100*data.count((n, a)))/nb_graphe[n]
#         if nb > 0:
#             if nb < 1:
#                 color = "cyan"
#             elif nb < 2:
#                 color = "turquoise"
#             elif nb < 3:
#                 color = "lime"
#             elif nb < 4:
#                 color = "orange"
#             elif nb < 5:
#                 color = "yellow"
#             else:
#                 color="red"
#             occu[(n, a)] = color
#
# plt.figure()
# for coords in occu:
#     plt.plot(coords[0], coords[1], '+', color=occu[coords])


# nb_graphe = {}
# for n in range(3, 21):
#     somme = 0
#     for a in range(l_all[0][n - 3], l_all[1][n - 3] + 1):
#         nb = data.count((n, a))
#         somme += nb
#     nb_graphe[n] = somme
#
# occu = {}
# for n in range(3, 21):
#     occu[n] = {}
#     for a in range(l_all[0][n - 3], l_all[1][n - 3] + 1):
#         nb = data.count((n,a))
#         occu[n][a] = nb
#
# sort_occu = {}
#
# total = {}
#
# for n in range(3, 21):
#     sort_occu_n = sorted(occu[n].items(), key=lambda x: x[1], reverse=True)
#     sort_occu[n] = sort_occu_n
#     total[n] = len(sort_occu_n)
#
# colors = {}
# for n in sort_occu:
#     tot = total[n]
#     part = tot/6
#     i = 1
#     for a in sort_occu[n]:
#         print(i, part, tot)
#         if i < part or i == 1:
#             color = "red"
#         elif i < 2*part or i == 2:
#             color = "orange"
#         elif i < 3*part or i == 3:
#             color = "yellow"
#         elif i < 4*part or  i == 4:
#             color = "lime"
#         elif i < 5*part or i == 5:
#             color = "turquoise"
#         else:
#             color = "cyan"
#         colors[(n, a[0])] = color
#         i += 1
#
#
# plt.figure()
# for coords in colors:
#     print(coords)
#     plt.plot(coords[0], coords[1], '+', color=colors[coords])


# data = traitement_nodes("Barabasi_Albert", "plus_petit_attribut", "closness_centrality")
#
# plt.plot(*zip(*data), '+')
# plt.show()

plt.show()

from deux_arbre_to_contexte import deux_arbres_to_attributs
from k_arbres import deux_arbres, attributs_subset
import time
import matplotlib.pyplot as plt

n = 20
m = 500


def is_equal(liste1, liste2):
    equal = (len(liste1) == len(liste2))
    if equal:
        is_in = [False]*len(liste1)
        for a in liste1:
            for b in liste2:
                if set(a) == set(b):
                    is_in[liste1.index(a)] = True
        for c in is_in:
            equal = equal and c
    return equal


time1 = []
time2 = []
for i in range(3, n):
    moy1 = 0
    moy2 = 0
    for j in range(m):
        print(i, j)
        arbre = deux_arbres(i)
        t1 = time.time_ns()
        attributs = deux_arbres_to_attributs(arbre.copy())[1]
        t2 = time.time_ns()
        real_attributs = attributs_subset(arbre.copy())[1]
        t3 = time.time_ns()
        print(is_equal(attributs, real_attributs))
        moy1 =+ t2 - t1
        moy2 =+ t3 - t2
    time1.append(moy1/m)
    time2.append(moy2/m)

plt.plot(list(range(3, n)), time1, label="Héritage")
plt.plot(list(range(3, n)), time2, label="Algo générique")
plt.title("Moyenne du temps d'execution")
plt.xlabel('Taille du deux arbre')
plt.ylabel("Temps d'execution en ns")
plt.legend()
plt.savefig("n" + str(n) + "m" + str(m) + ".png", dpi=300)

import csv
with open('time1n' + str(n) + 'm' + str(m) +'.csv', 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile)
    for t1 in time1:
        spamwriter.writerow([t1])

with open('time2n'+ str(n) + 'm' + str(m) +'.csv', 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile)
    for t2 in time2:
        spamwriter.writerow([t2])
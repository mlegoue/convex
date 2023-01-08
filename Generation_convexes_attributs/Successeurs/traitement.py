import matplotlib.pyplot as plt
from scipy.stats import linregress
import numpy as np
import csv


def regression_exp(y, y_full):
    plt.figure()
    a_min, b_min, r_min, p_value_min, std_err_min = linregress(np.arange(10, 30), np.log(np.array(y)))
    plt.plot(np.arange(2, 30), np.array(y_full), label="Temps d'exécution de l'algorithme successeur")
    print(b_min)
    plt.plot(np.arange(10, 30), np.exp(b_min + a_min * np.arange(10, 30)), label="$y = e^{" + str(round(b_min, 2)) + '+' + str(round(a_min, 2)) + 'x} - r = ' + str(
                 round(r_min, 3)) + "$")
    coefs = np.polyfit(np.arange(10, 30), np.array(y), 2)
    R2 = ((coefs[0] * np.arange(10, 30) ** 2 + coefs[1] * np.arange(10, 30) + coefs[2] - np.array(y).mean()) ** 2).sum() / ((np.array(y) - np.array(y).mean()) ** 2).sum()
    plt.plot(np.arange(10, 30), coefs[0] * np.arange(10, 30) ** 2 + coefs[1] * np.arange(10, 30) + coefs[2], label="$y = " + str(round(coefs[0], 2)) + 'x^2 + ' + str(round(coefs[1], 2)) + 'x + ' + str(
                 round(coefs[2], 2)) + ' - r = ' + str(round(np.sqrt(R2), 3)) + '$')
    plt.title("Temps d'exécution moyen sur 500 graphes d'Erdos-Renyi avec p = 0.5")
    plt.xlabel("Nombre de noeuds")
    plt.ylabel("Temps en secondes")
    plt.legend()


total = []

with open('res_30/time_total.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        mapped_row = list(map(float, row))
        total = mapped_row

regression_exp(total[8:], total)
plt.show()
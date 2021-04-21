import json
import csv
import matplotlib.pyplot as plt
from scipy.stats import linregress
import os

class_attributs = []
class_ccentrality = []
class_attributs_incomp = []
class_petit_attribut = []
class_bcentrality = []
class_ecentrality = []
class_dcentrality = []
pourc_attributs = []
ccentrality = []
bcentrality = []
ecentrality = []
dcentrality = []
pourc_attributs_incomp = []
petits_attributs = []


def classement(dict1):
    last_node = None
    place = 1
    places = []
    for node in dict1:
        if last_node == None:
            places.append(place)
            last_node = node
        else:
            if not dict1[node] == dict1[last_node]:
                place += 1
            places.append(place)
            last_node = node
    return places


def trace_graphe(x, name_x, y, name_y):
    plt.figure()
    plt.plot(x, y, '+', label="donnees")
    a, b, r, p_value, std_err = linregress(x, y)

    print(name_x, name_y, a, b, r)

    # plt.plot(  # droite de regression
    #     [1, 10],  # valeurs de x
    #     [a * 1 + b, a * 10 + b],  # valeurs de y
    #     "r-",  # couleur rouge avec un trait continu
    #     label="regression")  # legende
    plt.xlabel(name_x)  # nom de l'axe x
    plt.ylabel(name_y)  # nom de l'axe y
    plt.legend()  # la legende

def traitement(name):
    list_dir = os.listdir(name)
    for dir in list_dir:
        file = open(name + '/' + dir + '/attributs.csv')
        reader = csv.reader(file)
        read_nodes = file.readline()
        nodes = read_nodes.split(",")
        nodes[-1] = nodes[-1][:-1]
        nb_attributs = len(list(reader)) - 2
        with open(name + '/' + dir + '/data.txt') as json_file:
            data = json.load(json_file)
        place_attributs = classement(data["nb_attributs"])
        place_ccentralitys = classement(data["closness_centrality"])
        place_attributs_incomp = classement(data["nb_attributs_incomparables"])
        place_petit_attribut = classement(data["plus_petit_attribut"])
        place_bcentrality = classement(data["betweeness_centrality"])
        place_ecentrality = classement(data["eigenvector_centrality"])
        place_dcentrality = classement(data["degree_centrality"])
        for node in nodes:
            class_attributs.append(place_attributs[list(data["nb_attributs"]).index(str(node))])
            class_ccentrality.append(place_ccentralitys[list(data["closness_centrality"]).index(str(node))])
            class_attributs_incomp.append(place_attributs_incomp[list(data["nb_attributs_incomparables"]).index(str(node))])
            class_petit_attribut.append(place_petit_attribut[list(data["plus_petit_attribut"]).index(str(node))])
            class_bcentrality.append(place_bcentrality[list(data["betweeness_centrality"]).index(str(node))])
            class_ecentrality.append(place_ecentrality[list(data["eigenvector_centrality"]).index(str(node))])
            class_dcentrality.append(place_dcentrality[list(data["degree_centrality"]).index(str(node))])
            pourc_attributs.append(data["nb_attributs"][node]/nb_attributs)
            ccentrality.append(data["closness_centrality"][node])
            bcentrality.append(data["betweeness_centrality"][node])
            ecentrality.append(data["eigenvector_centrality"][node])
            dcentrality.append(data["degree_centrality"][node])
            pourc_attributs_incomp.append(data["nb_attributs_incomparables"][node]/nb_attributs)
            petits_attributs.append(data["plus_petit_attribut"][node])


traitement("Barabasi_Albert")

traitement("Erdos_Renyi")

traitement("Watts_Strogatz")



# trace_graphe(class_attributs, "Classement du nombre d'attributs", class_ccentrality, "Classement de la closness centrality")
# trace_graphe(class_attributs_incomp, "Classement du nombre d'attributs incomparables", class_ccentrality, "Classement de la closness centrality")
# trace_graphe(class_attributs, "Classement du nombre d'attributs", class_bcentrality, "Classement de la betweeness centrality")
# trace_graphe(class_attributs_incomp, "Classement du nombre d'attributs incomparbales", class_bcentrality, "Classement de la betweeness centrality")
# trace_graphe(class_attributs, "Classement du nombre d'attributs", class_ecentrality, "Classement de la eigenvector centrality")
# trace_graphe(class_attributs_incomp, "Classement du nombre d'attributs incomparables", class_ecentrality, "Classement de la eigenvector centrality")
# trace_graphe(class_attributs, "Classement du nombre d'attributs", class_dcentrality, "Classement de la degree centrality")
# trace_graphe(class_attributs_incomp, "Classement du nombre d'attributs incomparables", class_dcentrality, "Classement de la degree centrality")

trace_graphe(pourc_attributs, "Pourcentage d'attributs", ccentrality, "Closness centrality")
trace_graphe(pourc_attributs, "Pourcentage d'attributs", bcentrality, "Betweeness centrality")
trace_graphe(pourc_attributs, "Pourcentage d'attributs", ecentrality, "Eigenvector centrality")
trace_graphe(pourc_attributs, "Pourcentage d'attributs", dcentrality, "Degree centrality")

trace_graphe(pourc_attributs_incomp, "Pourcentage attributs incomparables", ccentrality, "Closness centrality")
trace_graphe(pourc_attributs_incomp, "Pourcentage attributs incomparables", bcentrality, "Betweeness centrality")
trace_graphe(pourc_attributs_incomp, "Pourcentage attributs incomparables", ecentrality, "Eigenvector centrality")
trace_graphe(pourc_attributs_incomp, "Pourcentage attributs incomparables", dcentrality, "Degree centrality")

trace_graphe(petits_attributs, "Plus petit attribut", ccentrality, "Closness centrality")
trace_graphe(petits_attributs, "Plus petit attribut", bcentrality, "Betweeness centrality")
trace_graphe(petits_attributs, "Plus petit attribut", ecentrality, "Eigenvector centrality")
trace_graphe(petits_attributs, "Plus petit attribut", dcentrality, "Degree centrality")

trace_graphe(class_petit_attribut, "Classement du plus petit attribut", class_ccentrality, "Classement de la closness centrality")
trace_graphe(class_petit_attribut, "Classement du plus petit attribut", class_bcentrality, "Classement de la betweeness centrality")
trace_graphe(class_petit_attribut, "Classement du plus petit attribut", class_ecentrality, "Classement de la eigenvector centrality")
trace_graphe(class_petit_attribut, "Classement du plus petit attribut", class_dcentrality, "Classement de la degree centrality")

plt.show()

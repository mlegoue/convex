from find_convexes import find_attributs
import networkx as nx
import csv
import os
import json


if not os.path.exists("Barabasi_Albert"):
    os.makedirs("Barabasi_Albert")

for n in range(3, 25):
    for m in range(1, n):
        if not os.path.exists("Barabasi_Albert/n" + str(n) + "m" + str(m)):
            os.makedirs("Barabasi_Albert/n" + str(n) + "m" + str(m))
        for i in range(100):
            if not os.path.exists("Barabasi_Albert/n" + str(n) + "m" + str(m) + '/nb' + str(i)):
                os.makedirs("Barabasi_Albert/n" + str(n) + "m" + str(m)+ '/nb' + str(i))
            G = nx.barabasi_albert_graph(n, m)
            while not nx.is_connected(G):
                G = nx.extended_barabasi_albert_graph(n, m)
            print(n, m, i)
            convexes, attributs = find_attributs(G)
            with open("Barabasi_Albert/n" + str(n) + "m" + str(m) + '/nb' + str(i) + '/attributs.csv', 'w', newline='') as csvfile:
                spamwriter = csv.writer(csvfile)
                spamwriter.writerow(list(G.nodes()))
                spamwriter.writerow(list(G.edges()))
                spamwriter.writerow(["Nombre de convexes", len(convexes)])
                spamwriter.writerow(["Nombre d'attributs", len(attributs)])
                spamwriter.writerow(["Attributs :"])
                for attribut in attributs:
                    spamwriter.writerow(attribut)

            ## Nombre d'attributs et de convexes

            nbatt = len(attributs)
            nbconv = len(convexes)

            ### Nombre d'attributs par noeud ###

            nb_attributs = {}

            for node in G.nodes():
                nb_attributs[node] = 0
                for attribut in attributs:
                    if node in attribut:
                        nb_attributs[node] += 1

            sorted_nb_attributs = {k: v for k, v in sorted(nb_attributs.items(), key=lambda item: item[1], reverse=True)}

            ### Nombre de plus petits attributs incomparables ###

            nb_attributs_incomp = {}

            for node in list(G.nodes()):
                attributsNode = []
                for attribut in attributs:
                    if node in attribut:
                        attributsNode.append(attribut)
                attributsNode.sort(key=lambda v: len(v))
                attributsincomp = []
                for attribut in attributsNode:
                    incomp = True
                    for attributincomp in attributsincomp:
                        if set(attributincomp).issubset(attribut):
                            incomp = False
                    if incomp:
                        attributsincomp.append(attribut)
                nb_attributs_incomp[node] = len(attributsincomp)

            sorted_nb_attributs_incomp = {k: v for k, v in sorted(nb_attributs_incomp.items(), key=lambda item: item[1],reverse=True)}

            ### Plus petit attribut et plus grand attribut ###

            petit_attribut = {}
            grand_attribut = {}

            for node in G.nodes():
                attributsNode = []
                for attribut in attributs:
                    if node in attribut:
                        attributsNode.append(attribut)
                attributsNode.sort(key=lambda v: len(v))
                petit_attribut[node] = len(attributsNode[0])
                grand_attribut[node] = len(attributsNode[-1])

            sorted_petit_attribut = {k: v for k, v in sorted(petit_attribut.items(), key=lambda item: item[1], reverse=True)}
            sorted_grand_attribut = {k: v for k, v in sorted(grand_attribut.items(), key=lambda item: item[1], reverse=True)}

            ### Closness centrality ###

            ccentrality = {}

            for node in G.nodes():
                ccentrality[node] = nx.closeness_centrality(G, node)

            sorted_ccentrality = {k: v for k, v in sorted(ccentrality.items(), key=lambda item: item[1], reverse=True)}

            ### Betweeness centrality ###

            bcentrality = nx.betweenness_centrality(G)

            sorted_bcentrality = {k: v for k, v in sorted(bcentrality.items(), key=lambda item: item[1], reverse=True)}

            ### Eigenvector centrality ###

            ecentrality = nx.eigenvector_centrality(G, max_iter=500)

            sorted_ecentrality = {k: v for k, v in sorted(ecentrality.items(), key=lambda item: item[1], reverse=True)}

            ### Degree centrality ###

            dcentrality = nx.degree_centrality(G)

            sorted_dcentrality = {k: v for k, v in sorted(dcentrality.items(), key=lambda item: item[1], reverse=True)}

            data = {}
            data['nb_nodes'] = n
            data['nb_attributs'] = nbatt
            data['nb_convexes'] = nbconv
            data['nb_attributs_par_n'] = sorted_nb_attributs
            data['nb_attributs_incomparables'] = sorted_nb_attributs_incomp
            data['plus_petit_attribut'] = sorted_petit_attribut
            data['plus_grand_attribut'] = sorted_grand_attribut
            data['closness_centrality'] = sorted_ccentrality
            data['betweeness_centrality'] = sorted_bcentrality
            data['eigenvector_centrality'] = sorted_ecentrality
            data['degree_centrality'] = sorted_dcentrality

            with open("Barabasi_Albert/n" + str(n) + "m" + str(m) + '/nb' + str(i) + '/data.txt', 'w') as outfile:
                json.dump(data, outfile)



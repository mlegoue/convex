from find_convexes import find_convexes
import networkx as nx
import csv
import os
import json


if not os.path.exists("Watts_Strogatz"):
    os.makedirs("Watts_Strogatz")

for n in range(18, 21):
    for m in range(2, n):
        for p in range(1, 10):
            if not os.path.exists("Watts_Strogatz/n" + str(n) + "m" + str(m) + "p" + str(p/10)):
                os.makedirs("Watts_Strogatz/n" + str(n) + "m" + str(m) + "p" + str(p/10))
            G = nx.connected_watts_strogatz_graph(n, m, p/10)
            print(n, m, p/10)
            convexe, attributs = find_convexes(G)
            with open("Watts_Strogatz/n" + str(n) + "m" + str(m) + "p" + str(p/10) + '/attributs.csv', 'w', newline='') as csvfile:
                spamwriter = csv.writer(csvfile)
                spamwriter.writerow(list(G.nodes()))
                spamwriter.writerow(list(G.edges()))
                spamwriter.writerow([len(convexe), len(attributs)])
                for attribut in attributs:
                    spamwriter.writerow(attribut)

            ### Nombre d'attributs ###

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

            sorted_nb_attributs_incomp = {k: v for k, v in sorted(nb_attributs_incomp.items(), key=lambda item: item[1], reverse=True)}

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
            data['nb_attributs'] = sorted_nb_attributs
            data['nb_attributs_incomparables'] = sorted_nb_attributs_incomp
            data['plus_petit_attribut'] = sorted_petit_attribut
            data['plus_grand_attribut'] = sorted_grand_attribut
            data['closness_centrality'] = sorted_ccentrality
            data['betweeness_centrality'] = sorted_bcentrality
            data['eigenvector_centrality'] = sorted_ecentrality
            data['degree_centrality'] = sorted_dcentrality

            with open("Watts_Strogatz/n" + str(n) + "m" + str(m) + "p" + str(p/10) + '/data.txt', 'w') as outfile:
                json.dump(data, outfile)



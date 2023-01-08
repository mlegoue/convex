import os
import json
import csv
import networkx as nx

graph = "Barabasi_Albert"

list_dir = os.listdir(graph)
l = []
for dir in list_dir:
        list_dir2 = os.listdir(graph + '/' + dir)
        for dir2 in list_dir2:
            with open(graph + '/' + dir + '/' + dir2 + '/attributs.csv', newline='') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=',')
                i = 0
                for row in spamreader:
                    if i == 1:
                        edges = row
                    i += 1
            edges_crop = []
            for edge in edges:
                edge_crop = edge[1:-1]
                res = tuple(map(int, edge_crop.split(', ')))
                edges_crop.append(res)
            G = nx.Graph()
            G.add_edges_from(edges_crop)
            with open(graph + '/' + dir + '/' + dir2 + '/data.txt') as json_file:
                data = json.load(json_file)
            if "diameter" not in data:
                data["diameter"] = nx.diameter(G)
                data["density"] = nx.density(G)
                with open(graph + '/' + dir + '/' + dir2 + '/data.txt', 'w') as outfile:
                    json.dump(data, outfile)
            print(dir, dir2)
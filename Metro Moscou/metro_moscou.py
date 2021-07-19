from Generation_convexes_attributs.Successeurs.find_convexes import find_attributs
import json
import networkx as nx
import matplotlib.pyplot as plt

metro_moscou = nx.Graph()
positions = {}

colors = {
    "1": "red",
    "2": "green",
    "3": "blue",
    "4": "powderblue",
    "5": "brown",
    "6": "orange",
    "7": "purple",
    "8": "yellow",
    "9": "grey",
    "10": "lime",
    "11": "turquoise",
    "12": "pink",
    "M1": "indigo"
}

with open('metro_moscou.json', "r") as f:
    metro = json.load(f)

for n in range(len(metro)):
    arret = metro[n]
    if n > 0:
        if metro[n]["line"] == metro[n-1]["line"]:
            metro_moscou.add_edge(metro[n]["name"], metro[n-1]["name"], color=colors[metro[n]["line"]])
    positions[arret["name"]] = (arret["longitude"], arret["latitude"])

couleurs = [metro_moscou[u][v]['color'] for u, v in metro_moscou.edges()]

plt.figure()
nx.draw(metro_moscou, with_labels=True, pos=positions, edge_color=couleurs, node_size=100, font_size=8)
plt.show()

print("coucou")
convexes, attributs = find_attributs(metro_moscou)

print("coucou")
print(convexes)
print("============")
print(attributs)



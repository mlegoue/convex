import networkx as nx
import matplotlib.pyplot as plt

G = nx.DiGraph()

G.add_edge(("vide", None), ("Chien", "mammifère"))
G.add_edge(("vide", None), ("Grenouille", None))
G.add_edge(("vide", None), ("Haricots", "Deux feuilles par graine"))
G.add_edge(("vide", None), ("Roseau", None))
G.add_edge(("Chien", "mammifère"), ("None 1", None))
G.add_edge(("Grenouille", None), ("None 1", None))
G.add_edge(("Grenouille", None), ("Brème", None))
G.add_edge(("Grenouille", None), ("None 2", None))
G.add_edge(("Haricots", "Deux feuilles par graine"), ("None 3", None))
G.add_edge(("Roseau", None), ("None 2", None))
G.add_edge(("Roseau", None), ("Maïs", None))
G.add_edge(("Roseau", None), ("Spike-weed", None))
G.add_edge(("None 1", None), (None, "A des membres"))
G.add_edge(("None 1", None), (None, "Vit sur terre"))
G.add_edge(("Brème", None), (None, "A des membres"))
G.add_edge(("Brème", None), ("Sangsue", None))
G.add_edge(("Maïs", None), ("None 3", None))
G.add_edge(("Maïs", None), (None, "Une feuille par graine"))
G.add_edge(("Spike-weed", None), (None, "Vit dans l'eau"))
G.add_edge(("Spike-weed", None), (None, "Une feuille par graine"))
G.add_edge((None, "A des membres"), (None, "Peut bouger"))
G.add_edge(("Sangsue", None), (None, "Peut bouger"))
G.add_edge(("Sangsue", None), (None, "Vit dans l'eau"))
G.add_edge(("None 2", None), (None, "Vit sur terre"))
G.add_edge(("None 2", None), (None, "Vit dans l'eau"))
G.add_edge(("None 3", None), (None, "Vit sur terre"))
G.add_edge(("None 3", None), (None, "A besoin de chlorophyle"))
G.add_edge((None, "Une feuille par graine"), (None, "A besoin de chlorophyle"))
G.add_edge((None, "Peut bouger"), (None, "A besoin d'eau pour vivre"))
G.add_edge((None, "Vit sur terre"), (None, "A besoin d'eau pour vivre"))
G.add_edge((None, "Vit dans l'eau"), (None, "A besoin d'eau pour vivre"))
G.add_edge((None, "A besoin de chlorophyle"), (None, "A besoin d'eau pour vivre"))

objets = []
attributs = []

noeud_final = None

for n in G.nodes():
    if (G.in_degree(n) == 1):
        objets.append(n[0])
    if (G.out_degree(n) == 1):
        attributs.append(n[1])
    if (G.out_degree(n) == 0):
        noeud_final = n



# options = {
#      'node_color': 'pink',
#      'node_size': 10000,
#  }
#
# nx.draw_spectral(G, with_labels=True, font_weight='bold', **options)
# plt.show()

noeuds = list(G.nodes)
dictionnaire = {}

for objet in objets:
    noeud_objet = None
    attributs_objet = []
    for noeud in noeuds:
        if noeud[0] == objet:
            noeud_objet = noeud
    for chemin in list(nx.shortest_simple_paths(G, noeud_objet, noeud_final)):
        for noeud in chemin:
            if noeud[1] not in attributs_objet and noeud[1] != None:
                attributs_objet.append(noeud[1])
    dictionnaire[objet] = attributs_objet


print(dictionnaire)

table = []

for i in range(8):
    table.append([0]*8)

for objet in objets:
    for attribut in attributs:
        if attribut in dictionnaire[objet]:
            table[objets.index(objet)][attributs.index(attribut)] = 1
        else:
            table[objets.index(objet)][attributs.index(attribut)] = 0

print (attributs)
for i in table:
    print(objets[table.index(i)], i)
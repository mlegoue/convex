import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt

def grid_to_contexte(grid):
    coins = []
    bords = []
    attributs = []
    for node in grid.nodes():
        if grid.degree[node] == 2:
            coins.append(node)
        elif grid.degree[node] == 3:
            bords.append(node)
    bords_grid = []
    for i in range(len(coins)):
        for j in range(i + 1, len(coins)):
            bord = nx.shortest_path(grid, source=coins[i], target=coins[j])
            if set(bord[1:-1]).issubset(bords):
                bords_grid.append(bord)
    for i in range(len(bords_grid)):
        b = []
        attribut = bords_grid[i]
        for j in range(len(bords_grid)):
            if i!=j:
                if bords_grid[i][0] == bords_grid[j][0]:
                    b.append((bords_grid[j], 0))
                elif bords_grid[i][-1] == bords_grid[j][-1]:
                    bords_grid[j].reverse()
                    b.append((bords_grid[j], -1))
                elif bords_grid[i][0] == bords_grid[j][-1]:
                    bords_grid[j].reverse()
                    b.append((bords_grid[j], 0))
                elif bords_grid[i][-1] == bords_grid[j][0]:
                    b.append((bords_grid[j], -1))
        attributs.append(attribut)
        if b != []:
            for i in range(1, len(b[0][0]) - 1):
                attribut = attribut + nx.shortest_path(grid, source=b[0][0][i], target=b[1][0][i])
                attributs.append(attribut)
    contexte = []
    objets = list(grid.nodes())
    for i in range(len(objets)):
        contexte.append([0] * len(attributs))
    for objet in objets:
        for attribut in attributs:
            if objet in attribut:
                contexte[objets.index(objet)][attributs.index(attribut)] = 1
            else:
                contexte[objets.index(objet)][attributs.index(attribut)] = 0
    return attributs, contexte



def display_contexte(objets, attributs, contexte):
    attributs_str = list(map(lambda attribut: ''.join(list(map(str, list(attribut)))), attributs))
    fig, ax = plt.subplots()
    # hide axes
    fig.patch.set_visible(False)
    ax.axis('off')
    ax.axis('tight')

    df = pd.DataFrame(contexte, columns=attributs_str)
    ax.table(cellText=df.values, colLabels=df.columns, loc='center', rowLabels=objets)
    fig.tight_layout()
    plt.show()



# grilleca = nx.Graph()
#
# grilleca.add_edges_from([(0, 1), (1, 2)])
# grilleca.add_edges_from([(3, 4), (4, 5)])
# grilleca.add_edges_from([(6, 7), (7, 8)])
#
# grilleca.add_edges_from([(0, 3), (3, 6)])
# grilleca.add_edges_from([(1, 4), (4, 7)])
# grilleca.add_edges_from([(2, 5), (5, 8)])
#
# attributs, contexte = grid_to_contexte(grilleca)
#
# display_contexte(list(grilleca.nodes()), attributs, contexte)


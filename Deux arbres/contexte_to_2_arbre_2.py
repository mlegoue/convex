import numpy as np
import networkx as nx

contexte = np.array([[1, 1, 0, 1, 0, 0, 1, 0],
                     [1, 0, 1, 1, 1, 0, 1, 0],
                     [0, 1, 1, 1, 0, 1, 1, 0],
                     [0, 0, 1, 0, 1, 1, 1, 1],
                     [1, 0, 1, 0, 1, 0, 1, 1]])

arbre0 = nx.Graph()
arbre0.add_edge(1, 2)
arbre0.add_edge(1, 3)
arbre0.add_edge(2, 3)

arbre0.edges[1, 2]['labels'] = 3
arbre0.edges[1, 3]['labels'] = 2
arbre0.edges[2, 3]['labels'] = 1

arbre3 = nx.Graph()
arbre3.add_edge(1, 2)
arbre3.add_edge(0, 1)
arbre3.add_edge(0, 2)

arbre3.edges[1, 2]['labels'] = 0
arbre3.edges[0, 1]['labels'] = 2
arbre3.edges[0, 2]['labels'] = 1


def find_u(contexte, objets):
    for j in range(contexte.shape[1]):
        colonne = contexte[:, j]
        if np.count_nonzero(colonne == 0) == 1:
            u = np.where(colonne == 0)[0][0]
            return j, objets[u]
    return None, None


# Fonction qui génére les couples de sommets ne contenant pas u

def find_couple(u, objets):
    list = []
    indice = objets.index(u)
    for i in range(len(objets)):
        for j in range(i+1, len(objets)):
            if i != indice and j != indice:
                list.append([objets[i], objets[j]])
    return list


# Fonction qui à partir de la colonne d'un contexte renvoie l'attribut

def contexte_to_attribut(contexte, objets):
    attributs = []
    for j in range(contexte.shape[1]):
        attribut = []
        for i in range(contexte.shape[0]):
            if contexte[i, j] == 1:
                attribut.append(objets[i])
        attributs.append(attribut)
    return attributs


def couples_in_attribut(couples, attribut):
    c_in = []
    c_not = []
    for couple in couples:
        if (couple[0] in attribut) and (couple[1] in attribut):
            c_in.append(couple)
        if (couple[0] not in attribut) and (couple[1] not in attribut):
            c_not.append(couple)
    return c_in, c_not

def not_in_any_attributs(couples, attributs):
    c_not = []
    in_attr = False
    for couple in couples:
        for attribut in attributs:
            if couple[0] in attribut or couple[1] in attribut:
                in_attr = True
        if not in_attr:
            c_not.append(couple)
    return c_not


# Fonction qui trouve x et y

def find_x_y(contexte, u, objets):
    couples = find_couple(u, objets)
    index_u = objets.index(u)
    attributs = contexte_to_attribut(contexte, objets)
    not_in_any = not_in_any_attributs(couples, attributs)
    for couple in not_in_any:
        couples.remove(couple)
    for i in range(contexte.shape[0]):
        in_attr, not_in_attr = couples_in_attribut(couples, attributs[i])
        if contexte[index_u][i] == 0:
            for couple in in_attr:
                couples.remove(couple)
        else:
            for couple in not_in_attr:
                couples.remove(couple)
    return couples

def powerset(seq):
    """
    Returns all the subsets of this set. This is a generator.
    """
    if len(seq) <= 1:
        yield seq
        yield []
    else:
        for item in powerset(seq[1:]):
            yield [seq[0]]+item
            yield item

def clarify_context(context):
    listes = powerset([i for i in range(context.shape[1])])
    to_clarify = []
    for liste in listes:
        for n in range(context.shape[1]):
            if n not in liste:
                res = [1 for _ in range(context.shape[0])]
                for i in liste:
                    for j in range(context.shape[0]):
                        res[j] = res[j] and context[j, i]
                if (res == context[:, n]).all():
                    to_clarify.append(n)
    return to_clarify

def generate_tri(context, objets):
    graph = nx.Graph()
    for i in range(3):
        arete = []
        equi = None
        for j in range(3):
            if context[j][i] == 1:
                arete.append(objets[j])
            else:
                equi = objets[j]
        if len(arete) == 2 and equi:
            graph.add_edge(arete[0], arete[1])
            graph.edges[arete[0], arete[1]]['labels'] = [equi]
        else:
            return None
    return graph




def is_deux_arbre(context, objets, equis, u, x, y):
    index_u = objets.index(u)
    index_x = objets.index(x)
    index_y = objets.index(y)
    deux_arbre = True
    for j in range(context.shape[1]):
        col = context[:, j]
        for equi in equis:
            index_e = objets.index(equi)
            equi_and_x_and_y_and_u = (col[index_e] == 1) and (col[index_u] == 1) and (col[index_x] == 1) and (col[index_y] == 1)
            equi_and_x_or_y_and_not_u = (col[index_e] == 1) and (col[index_u] == 0) and ((col[index_x] == 1) ^ (col[index_y] == 1))
            x_and_y_and_u = (col[index_e] == 0) and (col[index_u] == 1) and ((col[index_x] == 1) or (col[index_y] == 1))
            equi_and_not_x_and_not_y_and_not_u = (col[index_e] == 1) and (col[index_u] == 0) and (col[index_x] == 0) and (col[index_y] == 0)
            deux_arbre = deux_arbre and (equi_and_x_and_y_and_u or equi_and_x_or_y_and_not_u or x_and_y_and_u or equi_and_not_x_and_not_y_and_not_u)
    return deux_arbre


def change_label(graph, x, y, u):
    len_u = nx.shortest_path_length(graph, u)
    len_x = nx.shortest_path_length(graph, x)
    len_y = nx.shortest_path_length(graph, y)
    graph.edges[x, u]['labels'] = []
    graph.edges[y, u]['labels'] = []
    for edge in graph.edges():
        if len_u[edge[0]] == len_u[edge[1]]:
            graph.edges[edge[0], edge[1]]['labels'].append(u)
    for node in graph.nodes():
        if len_x[node] == len_u[node]:
            graph.edges[x, u]['labels'].append(node)
        elif len_y[node] == len_u[node]:
            graph.edges[y, u]['labels'].append(node)


def context_to_deux_arbre(context, objets):
    try:
        j, u = find_u(context, objets)
        new_context = np.delete(context, j, axis=1)
        x, y = find_x_y(new_context, u, objets)[0]
        new_context_w_u = np.delete(new_context, objets.index(u), axis=0)
        liste = clarify_context(new_context_w_u)
        new_context_clar = np.delete(new_context_w_u, liste, axis=1)
        new_objets = objets.copy()
        new_objets.remove(u)
        if new_context_clar.shape == (3, 3):
            arbre = generate_tri(new_context_clar, new_objets)
            deux_arbre = (arbre != None)
        else:
            deux_arbre, arbre = context_to_deux_arbre(new_context_clar, new_objets)
    except:
        deux_arbre = False
    if not deux_arbre:
        return False, None
    equix_y = arbre.edges[x, y]['labels']
    deux_arbre = is_deux_arbre(new_context, objets, equix_y, u, x, y)
    if not deux_arbre:
        return False, None
    arbre.add_edges_from([(x, u), (y, u)])
    change_label(arbre, x, y, u)
    return deux_arbre, arbre


deux_arbre, arbre = context_to_deux_arbre(contexte, [0, 1, 2, 3, 4])

if arbre != None:
    print(deux_arbre, arbre.edges())
else:
    print(deux_arbre)
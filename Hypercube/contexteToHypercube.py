import numpy as np
import networkx as nx
import itertools

contexte = np.array([[1, 0, 1, 0, 1, 0],
                     [1, 0, 1, 0, 0, 1],
                     [1, 0, 0, 1, 1, 0],
                     [1, 0, 0, 1, 0, 1],
                     [0, 1, 1, 0, 1, 0],
                     [0, 1, 1, 0, 0, 1],
                     [0, 1, 0, 1, 1, 0],
                     [0, 1, 0, 1, 0, 1]])


def fn(n, source, en_cours, tout):
    if (n == 0):
        if (len(en_cours) > 0):
            tout.append(en_cours)
        return
    for j in range(0, len(source)):
        fn(n - 1, source[j + 1:], en_cours + [source[j]], tout)
    return tout


def check_parity(contexte):
    check = True
    for ligne in contexte:
        check = check and np.count_nonzero(ligne == 0) == np.count_nonzero(ligne == 1)
    return check

def check_size(contexte):
    x = len(contexte[0])
    y = len(contexte)
    return x % 2 == 0 and y == 2**(x/2)


def same_table(table1, table2):
    comp = np.array(table1) == np.array(table2)
    return comp.all()


def sub_table(h, w, table):
    nptable = np.array(table)
    for i in range(len(table[0]) - w + 1):
        sub_table1 = nptable[0:h, i:i+w]
        sub_table2 = nptable[h:, i:i+w]
        if check_parity(sub_table1) and check_parity(sub_table2) and same_table(sub_table1, sub_table2):
            return sub_table1, sub_table2
    return None, None


def find_subtables(table, h, w):
    # objets = list(itertools.permutations(tuple(list(np.arange(len(table))))))
    # attributs = list(itertools.permutations(tuple(list(np.arange(len(table[0]))))))
    obj = np.arange(len(table))
    i, imax = 0, 2**len(obj)-1
    while i <= imax:
        objet = []
        j, jmax = 0, len(obj)-1
        if (i >> j) & 1 == 1:
            objet.append(obj[j])
        j += 1
        att = np.arange(len(table[0]))
        m, mmax = 0, 2**len(att)-1
        while m <= mmax:
            attribut = []
            n, nmax = 0, len(att) - 1
            if (m >> n) & 1 == 1:
                attribut.append(att[n])
            n += 1
            tableCopy = []
            for ligne in table:
                tableCopy.append(list(ligne.copy()))
            for i in objet:
                ligne = len(attribut)*[0]
                for j in attribut:
                    ligne[j] = table[i][j]
                tableCopy[i] = ligne.copy()
            table1, table2 = sub_table(h, w, tableCopy)
            if type(table1) == np.ndarray:
                return table1, table2
    return None, None





def contexte_to_hypercube(contexte):
    if len(contexte) == 2:
        comp1 = contexte == np.array([[1, 0], [0, 1]])
        comp2 = contexte == np.array([[0, 1], [1, 0]])
        if comp1.all() or comp2.all():
            hyper = nx.Graph()
            hyper.add_edge("0", "1")
            return hyper
        else:
            return None
    else:
        if check_size(contexte) and check_parity(contexte):
            table1, table2 = find_subtables(contexte, 2**(int(len(contexte[0])/2 - 1)),  int(len(contexte[0])-2))
            if type(table1) == np.ndarray:
                hyper = contexte_to_hypercube(table1)
                if hyper == None:
                    print("Ce n'est pas un hypercube !")
                    return None
                else:
                    nodes = hyper.nodes()
                    edges = hyper.edges()
                    new_hyper = nx.Graph()
                    for node in nodes:
                        new_hyper.add_nodes_from(["0" + node, "1" + node])
                        new_hyper.add_edge("0" + node, "1" + node)
                    for edge in edges:
                        new_hyper.add_edge("0" + edge[0], "0" + edge[1])
                        new_hyper.add_edge("1" + edge[0], "1" + edge[1])
                    return new_hyper
            else:
                return None
        else:
            return None


# hyper = hypercube(contexte)
# print(hyper.edges())

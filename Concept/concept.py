# objets = [0, 1, 2, 3, 4]
# attributs = [[0, 2], [4, 3], [0, 2, 4, 1], [0, 2, 3, 1], [0, 4, 1, 3], [2, 4, 1, 3]]

objets = [0, 1, 2, 3]
attributs = [[0, 1], [1, 2], [0, 3], [2, 3], [0, 1, 2], [0, 2, 3]]

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

def find_intention(attributs, extension):
    intention = []
    for attribut in attributs:
        if set(extension).issubset(attribut):
            intention.append(attribut)
    return intention

def find_extension(objets, intention):
    extension = []
    for objet in objets:
        in_attribut = True
        for attribut in intention:
            if objet not in attribut:
                in_attribut = False
        if in_attribut:
            extension.append(objet)
    return extension

def find_concept(objets, attributs):
    subsets = powerset(objets)
    concept = {}
    for subset in subsets:
        intention = find_intention(attributs, subset)
        extension = find_extension(objets, intention)
        print(subset, extension)
        if set(subset) == set(extension):
            concept[''.join(list(map(str, subset)))] = intention
    return concept

print(find_concept(objets, attributs))
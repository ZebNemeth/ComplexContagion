# Aart van Bochove, May 2020

'Defining the functions for the name labeling.'
def labelNode(conenr, levelnr, nodenr):
   return str(int(conenr)) + "_" + str(int(levelnr)) + "_" + str(int(nodenr))

def getConenr(node):
    indexEnd = node.find("_")
    conenr = ""
    for i in range(indexEnd):
        conenr += node[i]
    return int(conenr)

def getLevelnr(node):
    indexBegin = node.find("_")
    indexEnd = node.rfind("_")
    levelnr = ""
    for i in range(indexBegin+1,indexEnd):
         levelnr += node[i]
    return int(levelnr)

def getNodenr(node):
    indexBegin = node.rfind("_")
    nodenr = ""
    for i in range(indexBegin+1, len(node)):
        nodenr += node[i]
    return int(nodenr)

def getNodes(Graph, **conditions):
    specificCone = False
    specificLevel = False
    specificNode = False
    for argument in conditions:
        if argument == "conenr":
            specificCone = True
            Conenr = conditions[argument]
        elif argument == "levelnr":
            specificLevel = True
            Levelnr = conditions[argument]
        elif argument == "nodenr":
            specificNode = True
            Nodenr = conditions[argument]    
    nodelist = list(Graph.nodes)
    irrelevantNodes = []
    for counter, node in enumerate(nodelist):
        if specificCone:
            if getConenr(node) != Conenr:
                irrelevantNodes.append(node)
                continue
        if specificLevel:
            if getLevelnr(node) != Levelnr:
                irrelevantNodes.append(node)
                continue
        if specificNode:
            if getNodenr(node) != Nodenr:
                irrelevantNodes.append(node)
                continue
    for counter, node in enumerate(irrelevantNodes):
        nodelist.remove(node)
    return nodelist

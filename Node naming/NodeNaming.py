'As a string. The label of node 3 in level 2 in cone 1 is "1_2_3"'
def labelNode(conenr, levelnr, nodenr):
    return(str(str(conenr) + "_" + str(levelnr) + "_" + str(nodenr)))
    
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

'As a node attribute. Node 3 in level 2 in cone 1 is has attributes: node = 1, level = 2, cone = 3'
def labelNode(labels, conenr, levelnr, nodenr): #here 'labels' is a 3D array which translates from the given numbers to the label of the node
    return(labels[conenr][levelnr][nodenr])
    
def getConenr(node):
    return(G.node[node]['conenr'])
    
def getLevelnr(node):
    return(G.node[node]['levelnr'])
        
def getNodenr(node):
    return(G.node[node]['nodenr'])

#getNodes(Graph, **conditions) is defined in the exact same way as before
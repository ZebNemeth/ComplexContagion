import networkx as nx
import matplotlib.pyplot as plt
import math
import numpy as np

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

'Setting up the variables for the model'
nCones = 3 #The number of cones (communities)
nLevels = 3 #The number of levels per cone

#The number of nodes per level. Example: with n levels this creates [n,n*nInferiors,(n*nInferiors)*nInferiors, ..., n*(nInferiors**n)]
nNodes = np.array(nLevels)
nInferiors = 4
for i in range(1,nLevels): nNodes = np.append(nNodes,np.max(nNodes)*nInferiors)
print nNodes
nRingNeighbors = (np.arange(nLevels)+1)*2 #Number of neighbors per node in the ring. Example with 3 levels: [2,4,6]


'Graph is defined'
G = nx.Graph()


'Cones are created'
for level in reversed(range(nLevels)): #Building it level by level, from the lowest level to the highest

    'The seperate rings are build'
    #Making the 'blueprint' of the Watts-Strogatz ring for this level:
    ringlevel = nx.watts_strogatz_graph(nNodes[level],nRingNeighbors[level],0)
    #Implementing this blueprint for every cone
    for cone in range(nCones):
        mapping = {}
        for node in range(nNodes[level]):
            mapping.update({node:labelNode(cone,level,node)}) #Making a map for relabeling the node names as conenr_levelnr_nodenr
        ring = nx.relabel_nodes(ringlevel,mapping) #Applying map on ring for this cone - this relabels the node names

        G.add_nodes_from(ring) #Adding the nodes from the ring to the graph
        G.add_edges_from(ring.edges()) #Adding the edges from the ring to the graph
        
        'The connections between rings are created. The connections are created from the higher level to the lower level'
        if level != nLevels-1: #The lowest level can't create any connections up, so this level is skipped
            #The nodes of the level below are split into groups. This is the size of each group
            groupsize = nNodes[level+1]/nNodes[level]
            
            for nodeInLowerLevel in range(nNodes[level+1]): #This loop goes over every node in the lower level
                nodeInThisLevel = math.ceil((nodeInLowerLevel+1)/groupsize) #This is the nodenumber of the node in the current level.
                G.add_edge(labelNode(cone,level,nodeInThisLevel),labelNode(cone,level+1,nodeInLowerLevel)) #Edges are added between the different levels

'Optional interconal edges are created'
bInterEdge = True  # Wanna do this?
bManual = False     # See ~9 lines down what to do
friendliness = .90 # Fraction of nodes that are assigned a friend in another cone
friendlyLevel = nLevels # Only lowest ranking nodes are friendly to othercone low-levels

goodFriend = .9
mediumFriend = .8
badFriend = -.5

interEdges = []
print friendlyLevel

if bManual: # For manually adding a list of interconal edges
   interEdges = [
      ('0_2_1','1_2_1', goodFriend),
      ('2_2_1','0_2_4', badFriend),
      ]
   G.add_weighted_edges_from(interEdges)

else:          # We assign, to each lowest-level node, if friendly enough, a friend in another cone
   for cone in range(nCones):
      for node in range(nNodes[friendlyLevel-1]): 
         if ( np.random.random() <= friendliness ):
            edgeToAdd = (labelNode(cone, friendlyLevel-1, node), labelNode( (cone + int(np.random.random()*nCones))%nCones, friendlyLevel-1, (node + int(np.random.random()*nNodes[friendlyLevel-1]))%nNodes[friendlyLevel-1]), # From current node to some other node not outside range
                     goodFriend)   # And the weight
            otherWayEdgeToAdd = (edgeToAdd[1],edgeToAdd[0],edgeToAdd[2])
            G.add_weighted_edges_from([edgeToAdd, otherWayEdgeToAdd])



'Graph is drawn'
nx.draw(G, node_size=10, edge_color='grey')
plt.show()

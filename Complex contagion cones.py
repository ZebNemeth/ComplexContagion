import networkx as nx
import matplotlib.pyplot as plt
import math
import numpy as np

'Defining the function for the name labeling.'
def labelNode(conenr, levelnr, nodenr):
    return(str(str(conenr) + "_" + str(levelnr) + "_" + str(nodenr)))
    
'Setting up the variables for the model'
nCones = 8 #The number of cones (communities)
nLevels = 4 #The number of levels per cone

#The number of nodes per level. Example: with 3 levels this creates [4,32,256]
nNodes = np.array(4)
for i in range(1,nLevels): nNodes = np.append(nNodes,np.max(nNodes)*8)

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
                nodeInThisLevel = math.ceil((nodeInLowerLevel+1)/groupsize)-1 #This is the nodenumber of the node in the current level.
                G.add_edge(labelNode(cone,level,nodeInThisLevel),labelNode(cone,level+1,nodeInLowerLevel)) #Edges are added between the different levels
                
'Graph is drawn'
#nx.draw(G, node_size=10, edge_color='grey')
#plt.show()

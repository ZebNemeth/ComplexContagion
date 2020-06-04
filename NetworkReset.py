# Aart van Bochove, June 2020

import networkx as nx
import math
import numpy as np

from NodeLabeling import labelNode, getConenr, getLevelnr, getNodenr, getNodes

def resetNetwork(G, nCones = 1, nLevels = 4, nNodes = np.arange(1,5), nInferiors = 2, nRingNeighbors = (np.arange(4))*2, weightUp = 0.3, weightDown = 0.8):
    
    nx.set_node_attributes(G, 0, name='conv_lev')
    for level in reversed(range(nLevels)): #Resetting the edges level by level, from the lowest level to the highest
        for cone in range(nCones):
            'The weights of the connections between rings are changed.'
            if level != nLevels-1: #The lowest level can't create any connections up, so this level is skipped
                #The nodes of the level below are split into groups. This is the size of each group
                groupsize = nNodes[level+1]/nNodes[level]

                for nodeInLowerLevel in range(nNodes[level+1]): #This loop goes over every node in the lower level
                    nodeInThisLevel = math.ceil((nodeInLowerLevel+1)/groupsize)-1 #This is the nodenumber of the node in the current level.
                    G[labelNode(cone,level,nodeInThisLevel)][labelNode(cone,level+1,nodeInLowerLevel)][0]['weight'] = weightDown #Weight of edge sup to inf
                    G[labelNode(cone,level+1,nodeInLowerLevel)][labelNode(cone,level,nodeInThisLevel)][0]['weight'] = weightUp #Weight of edge inf to sup
    return G
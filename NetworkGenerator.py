# Aart van Bochove, May 2020

import networkx as nx
import matplotlib.pyplot as plt
import math
import numpy as np

from NodeLabeling import labelNode, getConenr, getLevelnr, getNodenr, getNodes
import CSPComplexContagionConfig as var

def conalGraphGenerator( nCones = 1, nLevels = 4, nNodes = np.arange(1,5), nInferiors = 2, nRingNeighbors = (np.arange(4))*2 ):

    'Graph is defined'
    G = nx.MultiGraph()


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
            G.add_edges_from(ring.edges(), weight = var.weightNeutral ) #Adding the edges from the ring to the graph and giving them the same-level weights

            G = G.to_directed() #Turn Multi Graph into directed, only the intra-ring nodes get duplicated, not the one between rings

            'The connections between rings are created. The connections are created from the higher level to the lower level'
            if level != nLevels-1: #The lowest level can't create any connections up, so this level is skipped
                #The nodes of the level below are split into groups. This is the size of each group
                groupsize = nNodes[level+1]/nNodes[level]

                for nodeInLowerLevel in range(nNodes[level+1]): #This loop goes over every node in the lower level
                    nodeInThisLevel = math.ceil((nodeInLowerLevel+1)/groupsize)-1 #This is the nodenumber of the node in the current level.
                    G.add_edge(labelNode(cone,level,nodeInThisLevel),labelNode(cone,level+1,nodeInLowerLevel), weight = var.weightDown)   # Edge sup to inf, weight accordingly
                    G.add_edge(labelNode(cone,level+1,nodeInLowerLevel),labelNode(cone,level,nodeInThisLevel), weight = var.weightUp) # Edge inf to sup, weight accordingly
    return G
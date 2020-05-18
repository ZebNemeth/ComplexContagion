import networkx as nx
import random
import matplotlib.pyplot as plt
import math
import numpy as np

#First setting up the variables for the model
nCones = 8 #The number of cones (communities)
nLevels = 4 #The number of levels per cone
nNodes = np.array(4) #The number of nodes per level. For now only the highest level
for i in range(1,nLevels): nNodes = np.append(nNodes,np.max(nNodes)*8) #Number of nodes set for other levels
nUpperNeighbors = np.arange(nLevels) #Number of upper neighbors per node in the ring. Different per level
nRingNeighbors = (nUpperNeighbors+1)*2 #Number of neighbors in the ring. Different per level

#Graph is made
G = nx.Graph()

#Setting up the cones
for level in range(nLevels): #Building it level by level, from the highest level to the lowest
    ringlevel = nx.watts_strogatz_graph(nNodes[level],nRingNeighbors[level],0) #Making the Watts-Strogatz ring for this level
    for cone in range(nCones): #Building this ring for every cone
        mapping = {}
        for node in range(nNodes[level]):
            mapping.update({node:str(str(cone) + "_" + str(level) + "_" + str(node))}) #Making a map for relabeling the nodes as conenr_levelnr_nodenr
        ring = nx.relabel_nodes(ringlevel,mapping) #Applying map on ring for this cone
        G.add_nodes_from(ring) #Adding the nodes from the ring to the graph
        G.add_edges_from(ring.edges()) #Adding the edges from the ring to the graph
        if level != 0: #For making connections with level above
            nGroups = nNodes[level-1] #Nodes are split into groups - this is the number of groups
            groupsize = nNodes[level]/nGroups #Number of nodes per group
            connectedNodes = [] #Array which will be filled with nodes to connect to
            for group in range(nGroups):
                connectedNodes.append(random.sample(range(0,nNodes[level-1]),nUpperNeighbors[level])) #For every group, nUpperNeighbors[level] nodes will be randomly selected from te level above.
            for node in range(nNodes[level]):
                group = math.ceil((node+1)/groupsize)-1 #The group this node belongs to
                for upperNeighbor in range(0,nUpperNeighbors[level]):
                    G.add_edge(str(str(cone) + "_" + str(level-1) + "_" + str(connectedNodes[group][upperNeighbor])),str(str(cone) + "_" + str(level) + "_" + str(node))) #Edges are added between the different levels

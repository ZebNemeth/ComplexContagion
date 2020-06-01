# Zeb Nemeth, May 2020


import networkx as nx
import matplotlib.pyplot as plt
import math
import numpy as np

'Cone variables'
nCones = 1 #The number of cones (communities)
nLevels = 4 #The number of levels per cone


nNodes = np.array(4) #The number of nodes in the highest level
nInferiors = 2
for i in range(1,nLevels): 
    nNodes = np.append(nNodes,np.max(nNodes)*nInferiors) # Example: with 3 levels of 2 inferiors this creates [3,6,12]

#Number of neighbors per node in the ring. Example with 3 levels: [2,4,6]
nRingNeighbors = (np.arange(nLevels)+1)*2


weightNeutral = .5   # Weights on the same ring
weightUp = .3        # Weight from inferior to superior
weightDown = .8      # Weight from your boss and the world on your shoulders



'Variables for interconal edge creation'
friendliness = .2
friendQuality = .9
friendQualityBackwards = .9 # Who knows how balanced the friendship is...
friendLevel = nLevels # Set to nLevels for lowest level
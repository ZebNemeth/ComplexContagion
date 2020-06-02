'''
Aart van Bochove
Grigorios Kyrpizidis
Luja Kockritz
Zeb Nemeth

https://github.com/ZebNemeth/ComplexContagion

'''

import networkx as nx
import matplotlib.pyplot as plt
import math
import numpy as np

from NodeLabeling import labelNode, getConenr, getLevelnr, getNodenr, getNodes
from InterconalEdges import interconalEdges
from NetworkGenerator import conalGraphGenerator

import CSPComplexContagionConfig as var


'Generate Cones'
G = conalGraphGenerator(var.nCones, var.nLevels, var.nNodes, var.nInferiors, var.nRingNeighbors)


'Add interconal edges'
G.add_weighted_edges_from( interconalEdges( var.friendliness, var.friendLevel, var.friendQuality) )

'Graph is drawn'
nx.draw(G, node_size=10, edge_color='grey')
plt.show()
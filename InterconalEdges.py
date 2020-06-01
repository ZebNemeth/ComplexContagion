# Zeb Nemeth


import networkx as nx
import matplotlib.pyplot as plt
import math
import numpy as np
import random

import CSPComplexContagionConfig as var
from NodeLabeling import labelNode, getConenr, getLevelnr, getNodenr, getNodes

nCones = var.nCones
nNodes = var.nNodes


'Optional interconal edges are created'
def interconalEdges( friendliness=.15, friendlyLevel=1, friendQuality=.9):

    friendlyPercent = int(friendliness*100)
    interEdges = []

    if nCones == 1:
        print( 'Single cone, no interconal edges possible')
        return interEdges


    print ('Interconal two-way edges of weight %d occur %d percent of the time, at level #%d of the network' %(friendQuality, friendlyPercent, friendlyLevel) )

          # We assign, to each lowest-level node, if friendly enough, a random friend in random other cone
    for cone in range(nCones):
        otherCones = []
        for i in range(nCones):
            otherCones.append(i)
        otherCones.remove(cone)
        for node in range(nNodes[friendlyLevel-1]): 
            if ( np.random.random() <= friendliness ):
                edgeToAdd = ( 
                    (
                        labelNode( # From this node
                            cone, 
                            friendlyLevel-1,
                            node
                        ),
                        labelNode( # To this node
                            random.choice(otherCones),
                            friendlyLevel-1,
                            (node + int(np.random.random()*nNodes[friendlyLevel-1])%nNodes[friendlyLevel-1])
                        ),
                        friendQuality # With weight
                    )
                )

                interEdges.append( edgeToAdd )
                interEdges.append( (edgeToAdd[1],edgeToAdd[0],var.friendQualityBackwards) ) # Just switch the To and From and give weight so friendship is bidirectional

    return interEdges
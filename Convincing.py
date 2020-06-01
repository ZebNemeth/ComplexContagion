# -*- coding: utf-8 -*-
"""
Created on Mon May 18 09:15:56 2020

@author: luja
"""
import random as random
import sys

from past.builtins import execfile
execfile('Complex contagion cones.py')  

#conv = ['convinced', 'time t', 'r'] #list with values for convinced nodes, timestep and r. - to be set up later if needed
t = 0         #timesteps
tmax = 5     #maximum amount of timesteps
r = 2       #number of neibors that need to be convinced to convince a node
nr_convinced = 3 # number of initally convinced nodes
nr_convinced_neighbors = 2 # numer of neighbors of initially convinced node, that are already convinced
level_start = 1 # level in which to seed 

'choosing initially convinced nodes and their convinced neighbors'
nodes = list(G.nodes) # unique IDs of the nodes
convinced = []
convinced = random.sample(list(G.nodes()),nr_convinced)
for i in range(0, nr_convinced):
    convinced.extend(random.sample(list(G[convinced[i]]),nr_convinced_neighbors))
seeding = len(convinced) 

'check if seeding has worked and otherwise stop code execution'
if seeding == (nr_convinced+nr_convinced*nr_convinced_neighbors):
    print('Seeding complete')
    print('Initially conviced nodes: '+ str(seeding))
else:
    print('Seeding error')
    sys.exit()
         
conv_next = []          #the nodes to be convinced in 1 timestep
#'looping n times to get multiple values of N - only relevant for running the code multiple times'
#for n in range(0, 5):

stop = False
conv_time = [0] * tmax

'looping for tmax timesteps'
for t in range (0,tmax):
    for node in nodes:
        if node in convinced:
            continue
        neighbors = list(G[node])
        if bool(set(neighbors) & set(convinced)) == False:
            continue
        if len(list(set(neighbors) & set(convinced))) >= r:
            conv_next.append(node)
    #print(conv_next)
    convinced.extend(x for x in conv_next if x not in convinced)
    print('At timestep ' + str(t) + ', ' + str(len(conv_next)) + ' were convinced')
    conv_time[t]=len(conv_next)
    convinced.sort()
    if stop:
        break
    conv_next.clear()
    if len(convinced)==len(nodes):
        break                #if all nodes are convinced, stop process
print('Time is up')
print('In total ' + str(len(convinced)) + ' nodes were conviced')
if sum(conv_time)==len(convinced):
    print('All convinced nodes were recorded')
else:
    print('Some nodes got lost')
 
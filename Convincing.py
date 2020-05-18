# -*- coding: utf-8 -*-
"""
Created on Mon May 18 09:15:56 2020

@author: luja
"""

#conv = ['convinced', 'time t', 'r'] #list with values for convinced nodes, timestep and r. - to be set up later if needed
t = 0         #timesteps
tmax = 5     #maximum amount of timesteps
r = 2       #number of neibors that need to be convinced to convince a node
nr_convinced = 3 # number of initally convinced nodes
nr_convinced_neighbors = 2 # numer of neighbors of initially convinced node, that are already convinced
level_start = 1 # level in which to seed 

# choosing initially convinced nodes and their convinced neighbors
nodes = list(G.nodes) # unique IDs of the nodes
convinced = []
convinced.append(random.sample(range(0,nNodes[level_start]),nr_convinced))
for i in range(0,nr_convinced):
    convinced.append(random.sample(range(0,G.neighbors[convinced[i]]),nr_convinced_neighbors)
      
#infection = False        
conv_next = []          #the nodes to be convinced in 1 timestep
#looping n times to get multiple values of N - only relevant for running the code multiple times
#for n in range(0, 5):
t=0
#looping for tmax timesteps
while t < tmax:
    for node in nodes:
        neighbors = list(G.neighbors(node))
        if node in convinced:
            continue
        if bool(set(neighbors) & set(convinced)) == False:
            continue
        if len(list(set(neighbors) & set(convinced)) >= r
               conv_next.append(node)
    infected.extend(x for x in infected_next if x not in infected)
    conv_next.clear()
    convinced.sort()
    t = t+1
    if len(convinced)==len(nodes):
        t = tmax                #if all nodes are convinced, stop process

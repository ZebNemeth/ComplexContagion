# -*- coding: utf-8 -*-
"""
Created on Mon May 18 09:15:56 2020

@author: luja
"""
import random as random
import sys
import os
import networkx as nx
os.chdir(r"C:\Users\luja\Documents\GSS\Complex_Systems_Project\ComplexContagion-master")
print(os.getcwd())

from platform import python_version
print(python_version())

from past.builtins import execfile
execfile('Cones_weighted.py')  

#conv = ['convinced', 'time t', 'r'] #list with values for convinced nodes, timestep and r. - to be set up later if needed
t = 0         #timesteps
tmax = 5     #maximum amount of timesteps
r = 2       #number of neibors that need to be convinced to convince a node
nr_convinced = 3 # number of initally convinced nodes
nr_convinced_neighbors = 2 # numer of neighbors of initially convinced node, that are already convinced
nr_to_convince = 2 # number of neighbors a node convinces in one timestep
level_start = 1 # level in which to seed

nx.set_node_attributes(G, 0, name='conv_lev') 
# access attribute as G.node['0_0_0']['conv_lev']

'choosing initially convinced nodes and their convinced neighbors'
nodes = list(G.nodes) # unique IDs of the nodes
convinced = []
convinced = random.sample(list(G.nodes()),nr_convinced)
for i in range(0, nr_convinced):
    convinced.extend(random.sample(list(G[convinced[i]]),nr_convinced_neighbors))
seeding = len(convinced) 

for node in convinced:
    G.node[node]['conv_lev']=1
    

'check if seeding has worked and otherwise stop code execution'
if seeding == (nr_convinced+nr_convinced*nr_convinced_neighbors):
    print('Seeding complete')
    print('Initially convinced nodes: '+ str(seeding))
    convinced.sort()
    print(convinced)
else:
    print('Seeding error')
    sys.exit()
         
conv_next = []          #the nodes to be convinced in 1 timestep
#cum_inf = 

#'looping n times to get multiple values of N - only relevant for running the code multiple times'
#for n in range(0, 5):

stop = False
conv_time = [0] * (1+tmax)
conv_time[0]=seeding

'looping for tmax timesteps'
for t in range (0,tmax):
    for node in convinced:
        neighbors = list(G[node])
        for i in neighbors:
            if i in convinced:
                neighbors.remove(i)
        if len(neighbors)>nr_to_convince:
            chosen=random.sample(neighbors,nr_to_convince)
            for j in chosen:
                G.node[j]['conv_lev']+=nx.dijkstra_path_length(G, node, j, 'weight')
                conv_next.append(j)
        elif len(neighbors)>0:
            chosen = random.choice(neighbors)
            G.node[chosen]['conv_lev']+=nx.dijkstra_path_length(G, node, chosen, 'weight')
            conv_next.append(chosen)
        else:
            continue
            
    #print(conv_next)
    convinced.extend(x for x in conv_next if x not in convinced)
    print('At timestep ' + str(t) + ', ' + str(len(conv_next)) + ' were convinced')
    conv_time[t+1]=len(conv_next)
    convinced.sort()
    if stop:
        break
    conv_next.clear()
    if len(convinced)==len(nodes):
        break                #if all nodes are convinced, stop process
print('Time is up')
print('In total ' + str(len(convinced)) + ' nodes were conviced')
if sum(conv_time)==(len(convinced)):
    print('All convinced nodes were recorded')
else:
    print('Some nodes got lost')
consensus=(len(convinced)/len(nodes))*100
print(str(consensus) +'% were convinced')
 
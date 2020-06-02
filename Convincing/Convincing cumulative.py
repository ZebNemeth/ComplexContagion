# -*- coding: utf-8 -*-
"""
Created on Mon May 18 09:15:56 2020
@author: luja
"""
import random as random
import sys
import os
import networkx as nx
os.chdir(r"C:\Users\aartv\Documents\Natuur- en sterrenkunde\CSP\ComplexContagion-ParadigmContagion")
print(os.getcwd())

from platform import python_version
print(python_version())

from past.builtins import execfile
execfile('CSPComplexContagionMain.py')  

#conv = ['convinced', 'time t', 'r'] #list with values for convinced nodes, timestep and r. - to be set up later if needed
t = 0         #timesteps
tmax = 5     #maximum amount of timesteps
r = 2       #number of neibors that need to be convinced to convince a node
convincing_threshold = 1 #treshold
draining = 0.1 #Draining per timestep
nr_convinced = 3 # number of initally convinced nodes
nr_convinced_neighbors = 2 # numer of neighbors of initially convinced node, that are already convinced
nr_to_convince = 2 # number of neighbors a node convinces in one timestep
level_start = 1 # level in which to seed

nodes = list(G.nodes()) # unique IDs of the nodes

seedingTry = 1 #How many times seeded
while True:
    if seedingTry == 5:
        print('Seeding failed too often, procedure stopped')
        sys.exit()

    nx.set_node_attributes(G, 0, name='conv_lev') 
    # access attribute as G.node['0_0_0']['conv_lev']

    'choosing initially convinced nodes and their convinced neighbors'
    convinced = random.sample(getNodes(G, levelnr = level_start),nr_convinced)
    
    for i in range(0, nr_convinced):
        neighbors = list(G[convinced[i]])

        #Neighbors which cannot be convinced are excluded
        for neighbor in neighbors[:]:
            if neighbor in convinced or getLevelnr(neighbor) != level_start:
                neighbors.remove(neighbor)

        #If not enough neighbors are left for seeding
        if len(neighbors) < nr_convinced_neighbors:
            break
        
        neighborsToConvince = random.sample(neighbors,nr_convinced_neighbors)
        convinced.extend(neighborsToConvince)
    seeding = len(convinced)

    for node in convinced:
        G.node[node]['conv_lev']=1
    
    'check if seeding has worked and otherwise stop code execution'
    if seeding == (nr_convinced+nr_convinced*nr_convinced_neighbors):
        print('Seeding complete')
        print('Initially convinced nodes: '+ str(seeding))
        convinced.sort()
        print(convinced)
        break
    else:
        print('Seeding error, starting over again')
        seedingTry += 1
        continue
         
#looping n times to get multiple values of N - only relevant for running the code multiple times'
#for n in range(0, 5):

stop = False
conv_time = [0] * (1+tmax)
conv_time[0]=seeding

'looping for tmax timesteps'
for t in range (0,tmax):
    'Convinced nodes spread information'
    for node in convinced:
        neighbors = list(G[node])

        #Already convinced neighbors are excluded
        for i in neighbors[:]:
            if i in convinced:
                neighbors.remove(i)

        #Weight is added to random selection of those neighbors
        if len(neighbors)>nr_to_convince:
            chosen=random.sample(neighbors,nr_to_convince)
            for j in chosen:
                G.node[j]['conv_lev']+=G[node][j][0]['weight']
        elif len(neighbors)>0:
            chosen = random.choice(neighbors)
            G.node[chosen]['conv_lev']+=G[node][chosen][0]['weight']

    'Nodes are convinced and not convinced nodes lose some information'
    for node in nodes:
        if node in convinced:
            continue

        #Nodes are convinced
        if G.node[node]['conv_lev'] >= convincing_threshold:
            convinced.append(node)
            conv_time[t+1] += 1

        #Not convinced nodes lose some information
        else:
            G.node[node]['conv_lev'] -= draining
            if G.node[node]['conv_lev'] < 0:
                G.node[node]['conv_lev'] = 0

    print('At timestep ' + str(t) + ', ' + str(conv_time[t+1]) + ' were convinced')
    convinced.sort()
    if stop:
        break
    if len(convinced)==len(nodes):
        print('All nodes are convinced')
        break                #if all nodes are convinced, stop process
    if t == tmax-1:
        print('Time ended')
print('In total ' + str(len(convinced)) + ' nodes were conviced')
if sum(conv_time)==(len(convinced)):
    print('All convinced nodes were recorded')
else:
    print('Some nodes got lost')
consensus=(len(convinced)/len(nodes))*100
print('{:.2f} were convinced'.format(consensus))
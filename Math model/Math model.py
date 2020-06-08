import sympy
import numpy as np
import matplotlib.pyplot as plt
import sys

'''
The variables of the model
'''

'Cone variables'
nLevels = 4 #The number of levels per cone
nNodes = np.array(4) #The number of nodes in the highest level
nInferiors = 3
for i in range(1,nLevels): 
    nNodes = np.append(nNodes,np.max(nNodes)*nInferiors) # Example: with 3 levels of 2 inferiors this creates [4,8,16]

#Number of neighbors per node in the ring. Example with 3 levels: [2,4,6]
nRingNeighbors = (np.arange(nLevels)+1)*2

'Number of entries determines number of runs'
weightNeutral = 0.3  # Weights on the same ring
weightUp = 0.05       # Weight from inferior to superior
weightDown = 0.55     # Weight from your boss and the world on your shoulders

'seeding varinables'
ini_convinced = 1   # number of initally convinced nodes
ini_convinced_neighbors = 2 # number of neighbors of initially convinced node, that are already convinced
level_start = 0 # level in which to seed

'convincing variables'
to_convince = 2 # number of neighbors a node convinces in one timestep
draining = 0.1 #Draining per timestep
convincing_threshold = 1


'''
Calculating some extra quantities
'''

nNodesSeeded = np.zeros(nLevels) #Number of nodes seeded per level
nNodesSeeded[level_start] = ini_convinced*(1+ini_convinced_neighbors)
rho0 = [] #density of seeded nodes per level
for level in range(nLevels):
    rho0.append(nNodesSeeded[level]/nNodes[level])
nNeighborsPerLevel = nRingNeighbors #Total number of neighbors per level
for level in range(nLevels):
    if level != 0: nNeighborsPerLevel[level] += 1
    if level != nLevels-1: nNeighborsPerLevel[level] += nInferiors
     
    
'''
Defining the functions given in the paper
'''

thetaArray = [[],[],[],[]]
def theta(Li,Lj,t): #Calculates theta
    #print("theta: t =",t,"Lj =",Lj,"Li =",Li)
    global thetaArray
    for i, item in enumerate(thetaArray[0]): #Checks if theta is already calculated before, if so, use that answer
        if item == Li and thetaArray[1][i] == Lj and thetaArray[2][i] == t:
            theta = thetaArray[3][i]
            return theta
        
    if t == 0: #Initial value
        theta = Psi(convincing_threshold,Li,0)*to_convince/nNeighborsPerLevel[Li]
        return theta
    
    theta = Psi(convincing_threshold,Li,t-1)*to_convince/nNeighborsPerLevel[Li] #Calculate as given in paper
    
    #Add theta to list of calculated values
    thetaArray[0].append(Li)
    thetaArray[1].append(Lj)
    thetaArray[2].append(t)
    thetaArray[3].append(theta)
    return theta

def n(Li,Lj): #Returns number of edges between level Li and a node on level Lj
    if (Li == Lj): return nRingNeighbors[Li]
    elif (Li == Lj + 1): return 1
    elif (Li == Lj - 1): return nInferiors
    else: return 0

def w(Li,Lj): #Returns weight from node on level Li to node on level Lj
    if (Li == Lj): return weightNeutral
    elif (Li == Lj + 1): return weightUp
    elif (Li == Lj - 1): return weightDown
    else: return 0

phiArray = [[],[],[],[],[]]
def phi(m,Li,Lj,t): #Calculates phi
    #print("phi: t =",t,"Lj =",Lj,"Li =",Li,"m =",m)
    global phiArray
    for i, item in enumerate(phiArray[0]): #Checks if phi is already calculated before, if so, use that answer
        if item == m and phiArray[1][i] == Li and phiArray[2][i] == Lj and phiArray[3][i] == t:
            phi = phiArray[4][i]
            return phi
        
    Comb = int(sympy.binomial(n(Li,Lj),m)) #Binomial coefficient
    termYes = theta(Li,Lj,t)**m #Second part
    termNo = (1-theta(Li,Lj,t))**(n(Li,Lj)-m) #Third part
    phi = Comb*termYes*termNo #Combine the parts as given in paper
    
    #Add phi to list of calculated values
    phiArray[0].append(m)
    phiArray[1].append(Li)
    phiArray[2].append(Lj)
    phiArray[3].append(t)
    phiArray[4].append(phi)
    return phi

PhiArray = [[],[],[],[],[]]
def Phi(M,Li,Lj,t): #Calculates Phi
    #print("Phi: t =",t,"Lj =",Lj,"Li =",Li,"M =",M)
    global PhiArray
    for i, item in enumerate(PhiArray[0]): #Checks if Phi is already calculated before, if so, use that answer
        if item == M and PhiArray[1][i] == Li and PhiArray[2][i] == Lj and PhiArray[3][i] == t:
            Phi = PhiArray[4][i]
            return Phi

    #mList contains the number of pieces of information m per time step. It starts with filling the first timesteps until M
    #in later steps always as many m is deleted as is added somewhere else, so tot total amount of m is always equal to M
    mList = np.zeros(t)
    Mleft = M
    whichM = 0
    while Mleft > 0:
        if Mleft > n(Li,Lj): mList[whichM] = n(Li,Lj)
        else: mList[whichM] = Mleft
        Mleft -= n(Li,Lj)
        whichM += 1
        if whichM >= t: return 0

    #i is an iterator which is used to track where the changes are done
    if M == 0: i = 0
    else: i = whichM - 1

    Phi = 0 #Phi is a sum of terms, so it starts with being zero

    calculating = True
    while calculating:
        sk = 1 #The term to be summed is a product, so it starts with being 1

        if max(mList) <= n(Li,Lj): #A node can not receive more pieces of information then it has neighbors
            for loopt in range(t): #Do the product
                sk *= phi(mList[loopt],Li,Lj,loopt)
            Phi += sk #Add the term to Phi

        if M == 0: break #For M = 0 there is only one possibility, all zeros, so after that the program should stop
        
        #If i is not on the end of the list yet, it brings one m one step further to the right
        if i < len(mList)-1:
            mList[i] -= 1
            i += 1
            mList[i] += 1

        else: #If i is on the end of the list

            #The iterator checkForNon0 finds the first element before i which contains a value higher then 0
            checkForNon0 = i
            nonZeroFound = False
            while not nonZeroFound:
                checkForNon0 -= 1
                if mList[checkForNon0] != 0: nonZeroFound = True
                #If there is no previous zero, mList hast the form of [0,0,...,0,M], and all relevant combinations are checked
                elif checkForNon0 == 0:
                    calculating = False
                    break
 
            #The iterator checkBeforeNon0 checks if there are non-zero elements before checkForNon0
            checkBeforeNon0 = checkForNon0
            onlyZeros = True
            while onlyZeros:
                if checkBeforeNon0 == 0: break
                checkBeforeNon0 -= 1
                if mList[checkBeforeNon0] != 0: onlyZeros = False

            mList[checkForNon0] -= 1 #The element at checkForNon0 decreases by one

            #If there are only 2 non-zero elements
            if onlyZeros:
                #If the 2 non-zero elements are not adjacent the m from the end is brought to the place after the non-zero element
                if checkForNon0 + 1 != i:
                    mList[checkForNon0+1] += mList[i] + 1
                    mList[i] = 0
                #If the 2 non-zero elements are adjacent the last one increases by one
                else:
                    mList[i] += 1
                #The iterator i goes to the last non-zero value in the list
                i = checkForNon0 + 1

            #If there are more then 2 non-zero elements, the iterator i goes to checkForNon0 + 1 and adds one there
            else:
                i = checkForNon0 + 1
                mList[i] += 1

    #Add Phi to list of calculated values
    PhiArray[0].append(M)
    PhiArray[1].append(Li)
    PhiArray[2].append(Lj)
    PhiArray[3].append(t)
    PhiArray[4].append(Phi)
    return Phi

psiArray = [[],[],[],[]]
def psi(nu,Lj,t): #Calculate psi
    #print("psi: t =",t,"Lj =",Lj,"nu =",nu)
    global psiArray
    for i, item in enumerate(psiArray[0]): #Checks if Phi is already calculated before, if so, use that answer
        if item == nu and psiArray[1][i] == Lj and psiArray[2][i] == t:
            psi = psiArray[3][i]
            return psi
        
    if nu == 0: #There is no possibility to find less then 0 information
        psi = 0
        return psi

    #If Lj is the lowest or highest level, only 2 levels have to be checked, otherwise 3
    if Lj == 0: minLevel = 0
    else: minLevel = Lj-1
    if Lj == nLevels-1: maxLevel = Lj
    else: maxLevel = Lj+1
    
    #MList contains the number of pieces of information M per level. It starts with filling the first level until it has
    #so many M that M*w <= nu and (M+1)*w > nu.
    MList = np.zeros(maxLevel-minLevel+1)
    MList[0] = int(nu/w(minLevel,Lj))
    if nu/w(minLevel,Lj) == int(nu/w(minLevel,Lj)) and int(nu/w(minLevel,Lj)) != 0: MList[0] -= 1
    i = 0 #i is an iterator which is used to track where the changes are done
    
    psi = 0 #phi is a sum of terms, so it starts with being zero
    
    calculating = True
    while calculating:
        Sk = 1 #The term to be summed is a product, so it starts with being 1

        summu = 0 #The total amount of information transfered by MList
        for Li in range(minLevel,maxLevel+1):
            summu += MList[Li-minLevel]*w(Li,Lj) #The total amount of information is calculated

        #If the amount of information summu is smaller then nu
        if summu < nu:
            #This is an allowed term, so it is calculated and added to psi
            for Li in range(minLevel,maxLevel+1):
                Sk *= Phi(MList[Li-minLevel],Li,Lj,t)
            psi += Sk

            #If i is not on the end yet, it increases with one
            if i != maxLevel-minLevel: i += 1
            
            #The first non-zero element in the list is found
            for findFirstNon0 in range(maxLevel-minLevel+1):
                if MList[findFirstNon0] != 0: break

            #If the first non-zero element is not on the end, 1 is added
            if findFirstNon0 != len(MList)-1: MList[i] += 1

            #If the first non-zero element is on the end OR there is no non-zero element, 1 is subtracted...
            else:
                MList[i] -= 1

                #And if there is no non-zero element, the procedure is stopped
                if MList[i] == -1:
                    calculating = False
                    break

        #If the amount of information summu is equal or larger then nu
        else:
            #The element i is at is emptied and i goes to the left
            MList[i] = 0
            i -= 1

            #The fist non-zero element in the list is found
            for findFirstNon0 in range(maxLevel-minLevel+1):
                if MList[findFirstNon0] != 0: break

            #If the first non-zero element is i
            if findFirstNon0 == i:

                #level i loses 1 bit of information and i increases by one
                MList[i] -= 1
                i += 1

                #if level i-1 (the previous level i) is now empty:
                if MList[i-1] == 0:

                    #This part is hardcoded. It should be possible to not do this, but this is easier now
                    #Level i is filled now similar to how the first element got filled in the beginning
                    if Lj == 0:
                        MList[i] = int(nu/w(Lj+1,Lj))
                        if nu/w(Lj+1,Lj) == int(nu/w(Lj+1,Lj)) and int(nu/w(Lj+1,Lj)) != 0: MList[i] -= 1
                    elif Lj == nLevels-1:
                        MList[i] = int(nu/w(Lj,Lj))
                        if nu/w(Lj,Lj) == int(nu/w(Lj,Lj)) and int(nu/w(Lj+1,Lj)) != 0: MList[i] -= 1
                    else:
                        MList[i] = int(nu/w(Lj,maxLevel-i))
                        if nu/w(Lj,maxLevel-i) == int(nu/w(Lj,maxLevel-i)) and int(nu/w(Lj+1,Lj)) != 0: MList[i] -= 1

                #if level i-1 (the previous level i) is not empty yet, level i gets emptied
                else: MList[i] = 0

            #If the first non-zero element is not i, element i increses by one
            else: MList[i] += 1

    #Add psi to list of calculated values    
    psiArray[0].append(nu)
    psiArray[1].append(Lj)
    psiArray[2].append(t)
    psiArray[3].append(psi)
    return psi

PsiArray = [[],[],[],[]]
def Psi(nu,Lj,t): #Calculate Psi
    #print("Psi: t =",t,"Lj =",Lj,"nu =",nu)
    global PsiArray
    for i, item in enumerate(PsiArray[0]): #Checks if Psi is already calculated before, if so, use that answer
        if item == nu and PsiArray[1][i] == Lj and PsiArray[2][i] == t:
            PsiValue = PsiArray[3][i]
            return PsiValue

    #Initial value
    if t == 0:
        if nu <= convincing_threshold:
            PsiValue = rho0[Lj]
        else:
            PsiValue = 0
        return PsiValue

    #Lambda as given in paper
    Lambda = draining*(1-Psi(0,Lj,t-1))

    #Psi as given in paper
    if nu - Lambda > 0: PsiValue = 1 - psi(nu-Lambda,Lj,t)
    else: PsiValue = 1 - psi(0,Lj,t)

    #Add Psi to list of calculated values
    PsiArray[0].append(nu)
    PsiArray[1].append(Lj)
    PsiArray[2].append(t)
    PsiArray[3].append(PsiValue)
    return PsiValue

def F(Lj,t):#Calculate F
    #print("F: t =",t,"Lj =",Lj)
    F = Psi(convincing_threshold,Lj,t) #F as given in paper
    return F

def f(t): #Calculate f
    #print("f: t =",t)
    Sum = 0 #f is the sum over all levels, it starts at 0
    for level in range(nLevels):
        Sum += nNodes[level]*F(level,t) #Add F of every level times the nodes on that level
    f = 1/sum(nNodes)*Sum #f as given in paper
    return f


'''
Calculate the total fraction of convinced nodes and plot it versus time
'''

t = np.arange(20)
fraction = []
for time in t:
    fraction.append(f(time))
plt.plot(t,fraction)
plt.xlabel("Time")
plt.ylabel("Consensus")
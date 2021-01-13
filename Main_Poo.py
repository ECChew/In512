import numpy as np
import Classes_Cell_Robot_PrioHuman_4_5Trouve as cl
import matplotlib.pyplot as plt
from matplotlib import colors
GridProba = np.zeros((20,20), dtype = cl.Cell)
for i in range(20):
    for j in range(20):
        GridProba[i, j] = cl.Cell(i, j)



#### Position of Walls

for i in [6,9,12]:
    for j in range(5,8):
        GridProba[i,j].Set_Wall(GridProba)
        
for i in range(15,20):
    for j in [7,16]:
        GridProba[i,j].Set_Wall(GridProba)

for i in range(14,19):
    GridProba[i,12].Set_Wall(GridProba)
      
for i in range(2,20):
    GridProba[i,3].Set_Wall(GridProba)
    
for i in [4,9]:
    for j in range(9,14):
        GridProba[i,j].Set_Wall(GridProba)       

for j in range(10,14):
        GridProba[12,j].Set_Wall(GridProba)
        
for i in range(2,7):
        GridProba[i,19].Set_Wall(GridProba)
        
for i in range(11,16):
    GridProba[i,18].Set_Wall(GridProba)
    
for i in range(1,6):
    GridProba[i,15].Set_Wall(GridProba)


#### Position of humans and spread cancellation behind wall
x_Human = [0, 0, 2, 8, 8, 12, 19, 19, 19]
y_Human = [8, 19, 4, 11, 17, 9, 8, 14, 19]
            
cl.PosHuman(x_Human,y_Human, GridProba)


#### Save
np.save('Map.npy', GridProba)





GridBelief = np.zeros((20,20), dtype = cl.Believe)
for i in range(20):
    for j in range(20):
        GridBelief[i, j] = cl.Believe(i, j)

GridBelief[15,1].Mouvement(GridProba, GridBelief)

##Avance d'une case

GridBelief[14,1].Mouvement(GridProba, GridBelief)
GridBelief[13,1].Mouvement(GridProba, GridBelief)
GridBelief[12,1].Mouvement(GridProba, GridBelief)
GridBelief[11,1].Mouvement(GridProba, GridBelief)
GridBelief[10,1].Mouvement(GridProba, GridBelief)
GridBelief[9,1].Mouvement(GridProba, GridBelief)
GridBelief[8,1].Mouvement(GridProba, GridBelief)
GridBelief[7,1].Mouvement(GridProba, GridBelief)
GridBelief[6,1].Mouvement(GridProba, GridBelief)
GridBelief[5,1].Mouvement(GridProba, GridBelief)
GridBelief[4,1].Mouvement(GridProba, GridBelief)
GridBelief[3,1].Mouvement(GridProba, GridBelief)

##
##
GridBelief[1,1].Mouvement(GridProba, GridBelief)
#print("-------------------------------------------------\n\n\n")
GridBelief[0,2].Mouvement(GridProba, GridBelief)
##GridBelief[1,1].Mouvement(GridProba, GridBelief)
##
###
##GridBelief[0,1].Mouvement(GridProba, GridBelief)
####
####print("-------------------------------------------------\n\n\n")
GridBelief[1,5].Mouvement(GridProba, GridBelief)
#####GridBelief[4,5].Mouvement(GridProba, GridBelief)
#####print("-------------------------------------------------\n\n\n")
GridBelief[4,6].Mouvement(GridProba, GridBelief)
#########print("-------------------------------------------------\n\n\n")
GridBelief[4,7].Mouvement(GridProba, GridBelief)
GridBelief[4,8].Mouvement(GridProba, GridBelief)
########print("-!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n\n")
GridBelief[3,7].Mouvement(GridProba, GridBelief)
########print("-!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n\n")
#GridBelief[0,8].Mouvement(GridProba, GridBelief)
GridBelief[3,9].Mouvement(GridProba, GridBelief)
####print("-------------------------------------------------\n\n\n")
GridBelief[2,10].Mouvement(GridProba, GridBelief)
#######print("-------------------------------------------------\n\n\n")
GridBelief[2,11].Mouvement(GridProba, GridBelief)
#######print("-------------------------------------------------\n\n\n")
GridBelief[2,12].Mouvement(GridProba, GridBelief)
############
######print("-------------------------------------------------\n\n\n")
GridBelief[2,13].Mouvement(GridProba, GridBelief)
######print("-------------------------------------------------\n\n\n")
GridBelief[2,14].Mouvement(GridProba, GridBelief)
######print("-------------------------------------------------\n\n\n")
GridBelief[1,13].Mouvement(GridProba, GridBelief)
######print("-------------------------------------------------\n\n\n")
GridBelief[3,14].Mouvement(GridProba,GridBelief)
######print("-------------------------------------------------\n\n\n")
GridBelief[4,14].Mouvement(GridProba,GridBelief)
#GridBelief[5,13].Mouvement(GridProba, GridBelief)
#GridBelief[5,14].Mouvement(GridProba, GridBelief)
#GridBelief[5,15].Mouvement(GridProba, GridBelief)
#GridBelief[4,16].Mouvement(GridProba, GridBelief)
#GridBelief[3,16].Mouvement(GridProba, GridBelief)

#GridBelief[5,12].Mouvement(GridProba, GridBelief)
GridBelief[6,12].Mouvement(GridProba, GridBelief)

#GridBelief[5,14].Mouvement(GridProba, GridBelief)
#GridBelief[5,15].Mouvement(GridProba, GridBelief)
#GridBelief[4,16].Mouvement(GridProba, GridBelief)
#GridBelief[3,14].Mouvement(GridProba, GridBelief)
#GridBelief[2,14].Mouvement(GridProba, GridBelief)
#GridBelief[1,14].Mouvement(GridProba, GridBelief)
#GridBelief[0,14].Mouvement(GridProba, GridBelief)
#GridBelief[0,13].Mouvement(GridProba, GridBelief)


##
##
##print("-------------------------------------------------\n\n\n")
#GridBelief[6,10].Mouvement(GridProba,GridBelief)
##print("-------------------------------------------------\n\n\n")
GridBelief[8,11].ProbabilisticWay(GridProba,GridBelief)
#print("-------------------------------------------------\n\n\n")
GridBelief[8,12].Mouvement(GridProba,GridBelief)
GridBelief[8,13].Mouvement(GridProba,GridBelief)
##
####
#####print("-------------------------------------------------\n\n\n")
#####GridBelief[8,12].Mouvement(GridProba,GridBelief)
##print("-------------------------------------------------\n\n\n")
#GridBelief[7,13].Mouvement(GridProba,GridBelief)
#print("-------------------------------------------------\n\n\n")
GridBelief[7,14].Mouvement(GridProba,GridBelief)
#print("-------------------------------------------------\n\n\n")
GridBelief[8,15].Mouvement(GridProba,GridBelief)
GridBelief[8,17].Mouvement(GridProba,GridBelief)
GridBelief[10,16].Mouvement(GridProba,GridBelief)
GridBelief[5,17].Mouvement(GridProba,GridBelief)
GridBelief[11,16].Mouvement(GridProba,GridBelief)
#
#print("-------------------------------------------------\n\n\n")
GridBelief[13,15].Mouvement(GridProba,GridBelief)
#print("-------------------------------------------------\n\n\n")
GridBelief[14,14].Mouvement(GridProba,GridBelief)
#
##print("-------------------------------------------------\n\n\n")
#GridBelief[14,13].Mouvement(GridProba, GridBelief)
#GridBelief[13,14].Mouvement(GridProba, GridBelief)
#print("-------------------------------------------------\n\n\n")
GridBelief[15,14].Mouvement(GridProba,GridBelief)
##print("-------------------------------------------------\n\n\n")
#GridBelief[16,14].Mouvement(GridProba,GridBelief)
print("-------------------------------------------------\n\n\n")
#GridBelief[17,13].Mouvement(GridProba,GridBelief)
#GridBelief[17,14].Mouvement(GridProba,GridBelief)
GridBelief[19,14].Mouvement(GridProba,GridBelief)
GridBelief[18,14].Mouvement(GridProba,GridBelief)
GridBelief[19,14].Mouvement(GridProba,GridBelief)
GridBelief[18,14].Mouvement(GridProba,GridBelief)
GridBelief[19,14].getOut(GridProba,GridBelief)
GridBelief[19, 13].getOut(GridProba,GridBelief)
GridBelief[19, 12].getOut(GridProba,GridBelief)
GridBelief[19, 11].Mouvement(GridProba,GridBelief)
GridBelief[18, 11].Mouvement(GridProba,GridBelief)
"""print(GridBelief[17, 14].L)

#print("-------------------------------------------------")
#print("-------------------------------------------------")
#print("-------------------------------------------------")
#print("-------------------------------------------------")
#print("-------------------------------------------------")
#print("-------------------------------------------------")
#print("-------------------------------------------------")
#print("-------------------------------------------------")
#print("-------------------------------------------------")
#print("-------------------------------------------------")
#print("-------------------------------------------------")
#print("-------------------------------------------------")
#print("-------------------------------------------------")
#GridBelief[10,17].Mouvement(GridProba,GridBelief)
#print("-------------------------------------------------\n\n\n")
#GridBelief[10,16].Mouvement(GridProba,GridBelief)
#print("-------------------------------------------------\n\n\n")
#GridBelief[11,15].Mouvement(GridProba,GridBelief)
#print("-------------------------------------------------\n\n\n")
#GridBelief[11,14].Mouvement(GridProba,GridBelief)
#print("-------------------------------------------------\n\n\n")
#GridBelief[12,15].Mouvement(GridProba,GridBelief)
#print("-------------------------------------------------\n\n\n")
#GridBelief[13,14].Mouvement(GridProba,GridBelief)
#print("-------------------------------------------------\n\n\n")
#GridBelief[14,14].Mouvement(GridProba,GridBelief)
#print("-------------------------------------------------\n\n\n")
#GridBelief[13,13].Mouvement(GridProba,GridBelief)
#print("-------------------------------------------------\n\n\n")
#GridBelief[12,12].Mouvement(GridProba,GridBelief)
#print("-------------------------------------------------\n\n\n")
#GridBelief[10,18].Mouvement(GridProba,GridBelief)
#print("-------------------------------------------------\n\n\n")
#GridBelief[9,19].Mouvement(GridProba,GridBelief)




#GridBelief[0,0].CaseToVisit(GridBelief)
"""
#print(GridBelief[0,6].L,GridBelief[1,6].L, GridBelief[0,7].L)
peoplebelief = np.zeros(GridProba.shape, dtype=float)
wallsbelief = np.zeros(GridProba.shape, dtype=float)
wallaroundbelief = np.zeros(GridProba.shape, dtype=float)
people = np.zeros(GridProba.shape, dtype=float)
Explored = np.zeros(GridProba.shape, dtype=float)
walls = np.zeros(GridProba.shape, dtype=float)
Validwall = np.zeros(GridProba.shape, dtype=float)
Longueur = np.zeros(GridProba.shape, dtype=float)
hybrid = np.zeros(GridProba.shape, dtype=float)
AVisite = np.zeros(GridProba.shape, dtype=float)


for i in range(GridProba.shape[0]):
    for j in range(GridProba.shape[1]):
        walls[i, j] = GridProba[i, j].L[0]
        people[i, j] = GridProba[i, j].L[1]
        Explored[i, j] = GridProba[i, j].L[2]
        hybrid[i, j] = GridProba[i, j].L[1] - GridProba[i, j].L[0]
        Validwall[i,j]= GridBelief[i,j].WallValid
        Longueur[i,j]= GridBelief[i,j].Longueur
        AVisite[i,j] = GridBelief[i,j].Visit
        wallsbelief[i, j] = GridBelief[i, j].L[0]
        peoplebelief[i, j] = GridBelief[i, j].L[1]
        #wallaroundbelief[i,j] =GridBelief[i,j].L[2]

        

cmap = colors.ListedColormap(['White','Gray','Black'])
cmap2 = colors.ListedColormap(['White','Yellow', 'Orange','Red'])
plt.figure(figsize=(6,6))
plt.pcolor(walls[::-1,:],cmap=cmap,edgecolors='k', linewidths=3)
plt.figure(figsize=(6,6))
plt.pcolor(people[::-1, :],cmap=cmap2,edgecolors='k', linewidths=3)
plt.figure(figsize=(6,6))
#plt.pcolor(Longueur[::-1, :],cmap='Reds',edgecolors='k', linewidths=3)
plt.figure(figsize=(6,6))
plt.pcolor(Explored[::-1, :],cmap=cmap2,edgecolors='k', linewidths=3)
#######plt.figure(figsize=(6,6))
#######plt.pcolor(hybrid[::-1, :],cmap='Reds',edgecolors='k', linewidths=3)
#####
plt.figure(figsize=(6,6))
plt.pcolor(Validwall[::-1, :],cmap='seismic',edgecolors='k', linewidths=3)
plt.title("Walls Valid")
plt.figure(figsize=(6,6))
plt.pcolor(wallsbelief[::-1, :],cmap='seismic',edgecolors='k', linewidths=3)
plt.title("Walls belief")
plt.figure(figsize=(6,6))
plt.pcolor(peoplebelief[::-1, :],cmap='seismic',edgecolors='k', linewidths=3)
plt.title("People belief")
#
#plt.xticks(np.arange(0.5,20.5,step=1))
#plt.yticks(np.arange(0.5,20.5,step=1))
plt.show()

#print(GridProba[3,3].L)

import movementCounter
print("Movement counter", movementCounter.mvtCounter, movementCounter.mvtCounter2, movementCounter.mvtCounter3, movementCounter.mvtCounter4)
print(cl.PourcentPeopleProba(GridProba))















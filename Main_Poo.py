import numpy as np
import Classes_Cell_Robot_PrioHuman_2 as cl
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

#### Initial position of the robot
GridProba[15,1].Set_Robot(GridProba)


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
GridBelief[2,1].Mouvement(GridProba, GridBelief)
GridBelief[1,1].Mouvement(GridProba, GridBelief)
GridBelief[0,1].Mouvement(GridProba, GridBelief)
GridBelief[0,2].Mouvement(GridProba, GridBelief)
GridBelief[1,3].Mouvement(GridProba, GridBelief)
GridBelief[1,2].Mouvement(GridProba, GridBelief)
GridBelief[0,3].Mouvement(GridProba, GridBelief)
GridBelief[1,4].Mouvement(GridProba, GridBelief)
GridBelief[1,6].Mouvement(GridProba, GridBelief)
GridBelief[0,7].Mouvement(GridProba, GridBelief)
GridBelief[0,9].Mouvement(GridProba, GridBelief)
GridBelief[0,10].Mouvement(GridProba, GridBelief)
GridBelief[1,9].Mouvement(GridProba, GridBelief)
GridBelief[1,10].Mouvement(GridProba, GridBelief)
GridBelief[1,11].Mouvement(GridProba, GridBelief)
GridBelief[0,12].Mouvement(GridProba, GridBelief)
GridBelief[0,13].Mouvement(GridProba, GridBelief)
GridBelief[1,12].Mouvement(GridProba, GridBelief)
GridBelief[1,13].Mouvement(GridProba, GridBelief)
GridBelief[1,14].Mouvement(GridProba, GridBelief)
GridBelief[0,14].Mouvement(GridProba, GridBelief)
GridBelief[0,15].Mouvement(GridProba, GridBelief)
GridBelief[0,16].Mouvement(GridProba, GridBelief)
GridBelief[0,17].Mouvement(GridProba, GridBelief)
GridBelief[1,18].Mouvement(GridProba, GridBelief)
GridBelief[0,17].Mouvement(GridProba, GridBelief)
GridBelief[1,16].Mouvement(GridProba, GridBelief)
GridBelief[1,17].Mouvement(GridProba, GridBelief)
GridBelief[2,16].Mouvement(GridProba, GridBelief)
GridBelief[2,17].Mouvement(GridProba, GridBelief)
GridBelief[3,16].Mouvement(GridProba, GridBelief)
GridBelief[3,17].Mouvement(GridProba, GridBelief)
GridBelief[3,18].Mouvement(GridProba, GridBelief)
GridBelief[2,18].Mouvement(GridProba, GridBelief)
GridBelief[1,19].Mouvement(GridProba, GridBelief)



#GridBelief[3,2].Mouvement(GridProba, GridBelief)
#GridBelief[3,5].Mouvement(GridProba, GridBelief)
#GridBelief[2,6].Mouvement(GridProba, GridBelief)
#GridBelief[1,7].Mouvement(GridProba, GridBelief)
#GridBelief[1,9].Mouvement(GridProba, GridBelief)
#GridBelief[0,9].Mouvement(GridProba, GridBelief)
#GridBelief[0,10].Mouvement(GridProba, GridBelief)
#GridBelief[1,10].Mouvement(GridProba, GridBelief)
#GridBelief[1,11].Mouvement(GridProba, GridBelief)
#GridBelief[0,12].Mouvement(GridProba, GridBelief)
#GridBelief[0,13].Mouvement(GridProba, GridBelief)
#GridBelief[1,12].Mouvement(GridProba, GridBelief)
#GridBelief[1,13].Mouvement(GridProba, GridBelief)
#GridBelief[1,14].Mouvement(GridProba, GridBelief)
#GridBelief[0,14].Mouvement(GridProba, GridBelief)
#GridBelief[1,15].Mouvement(GridProba, GridBelief)





#print(GridBelief[0,6].L,GridBelief[1,6].L, GridBelief[0,7].L)
peoplebelief = np.zeros(GridProba.shape, dtype=float)
wallsbelief = np.zeros(GridProba.shape, dtype=float)
wallaroundbelief = np.zeros(GridProba.shape, dtype=float)
people = np.zeros(GridProba.shape, dtype=float)
walls = np.zeros(GridProba.shape, dtype=float)
hybrid = np.zeros(GridProba.shape, dtype=float)

for i in range(GridProba.shape[0]):
    for j in range(GridProba.shape[1]):
        walls[i, j] = GridProba[i, j].L[0]
        people[i, j] = GridProba[i, j].L[1]
        hybrid[i, j] = GridProba[i, j].L[1] - GridProba[i, j].L[0]
        wallsbelief[i, j] = GridBelief[i, j].L[0]
        peoplebelief[i, j] = GridBelief[i, j].L[1]
        wallaroundbelief[i,j] =GridBelief[i,j].L[2]

        

#cmap = colors.ListedColormap(['White','Gray','Black'])
#cmap2 = colors.ListedColormap(['White','Yellow', 'Orange','Red'])
#plt.figure(figsize=(6,6))
#plt.pcolor(walls[::-1,:],cmap=cmap,edgecolors='k', linewidths=3)
#plt.figure(figsize=(6,6))
#plt.pcolor(people[::-1, :],cmap=cmap2,edgecolors='k', linewidths=3)
#plt.figure(figsize=(6,6))
#plt.pcolor(hybrid[::-1, :],cmap='Reds',edgecolors='k', linewidths=3)
#
#plt.figure(figsize=(6,6))
#plt.pcolor(wallsbelief[::-1, :],cmap='seismic',edgecolors='k', linewidths=3)
#plt.title("Walls belief")
#plt.figure(figsize=(6,6))
#plt.pcolor(peoplebelief[::-1, :],cmap='seismic',edgecolors='k', linewidths=3)
#plt.title("People belief")
##plt.figure(figsize=(6,6))
##plt.pcolor(wallaroundbelief[::-1, :],cmap='seismic',edgecolors='k', linewidths=3)
##plt.title("WallAround belief")
#plt.xticks(np.arange(0.5,20.5,step=1))
#plt.yticks(np.arange(0.5,20.5,step=1))
#plt.show()

#print(GridProba[3,3].L)



















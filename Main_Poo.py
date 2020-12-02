import numpy as np
import Classes_Cell_Robot as cl

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
    
#### Position of humans
GridProba[2,4].Set_Human(GridProba)
GridProba[0,8].Set_Human(GridProba)
GridProba[0,19].Set_Human(GridProba)
GridProba[8,11].Set_Human(GridProba)
GridProba[8,17].Set_Human(GridProba)
GridProba[12,9].Set_Human(GridProba)
GridProba[19,8].Set_Human(GridProba)
GridProba[19,14].Set_Human(GridProba)
GridProba[19,19].Set_Human(GridProba)


#### Save
np.save



























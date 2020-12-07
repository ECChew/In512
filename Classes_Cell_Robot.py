import numpy as np


class Cell: 
    def __init__(self, xValue, yValue):
        #[Wall, Human, Explored, Position]
        self.L = [0, 0, 0, 0]
        self.x = xValue
        self.y = yValue
        
    #Spread the information of a human 2 cells around
    def Set_Human(self, Map):
        self.L = findMaxL([0, 1, 0, 0], self.L) 
        for i in range(-1,2):
            for j in range (-1,2):
                try:
                    #print("i - " ,i , "j - ", j ,Map[self.x + i, self.y + j].L)
                    Map[self.x+i, self.y+j].L = findMaxL(Map[self.x + i, self.y + j].L, [0, 0.6, 0, 0])
                except:
                    pass
                
        for i in range(-2,3):
            for j in range (-2,3):
                try:
                    Map[self.x+i, self.y+j].L = findMaxL(Map[self.x + i, self.y + j].L, [0, 0.3, 0, 0])
                except:
                    pass
    # Spread the information of a wall 1 cell around 
    def Set_Wall(self, Map):
        self.L = [1, 0, 0, 0]
        
        for i in range(-1,2):
            for j in range (-1,2):
                try:
                    Map[self.x+i, self.y+j].L = findMaxL(Map[self.x + i, self.y + j].L, [0.5, 0, 0, 0])
                except:
                    pass
                
    def Set_Robot(self, Map):
        self.L = [0, 0, 1, 1]
        Map[self.x, self.y].L = findMaxL(Map[self.x, self.y].L, self.L)
            
class Believe():
    def __init__(self, xValue, yValue):
        self.x = xValue
        self.y = yValue
        self.L = [1,1]
        
    def ConfirmBelief(self, Map):
        self.L = Map[self.x, self.y].L[:2] # Found using sensor at cell
   
    def Prediction_Wall(self, MapProba, MapBelief):
        if self.L[0] == 0:
            for i in range(-1,2):
                for j in range (-1,2):
                    try:
                        if MapProba[self.x + i, self.y + j].L[2] == 0:
                            MapBelief[self.x+i, self.y+j].L[0] *= 0
                    except: 
                        pass
        else:
            for i in range(-1,2):
                for j in range (-1,2):
                    try:
                        if MapProba[self.x + i, self.y + j].L[2] == 0:
                            MapBelief[self.x+i, self.y+j].L[0] *= 1
                    except: 
                        pass
    
    def Prediction_Human(self, MapProba, MapBelief):
        if self.L[1] == 0:
            for i in range(-2,3):
                for j in range (-2,3):
                    try:
                        if MapProba[self.x + i, self.y + j].L[1] == 0:
                            MapBelief[self.x+i, self.y+j].L[1] *= 0
                    except: 
                        pass
        elif self.L[1]==0.3:
            for i in range (-3, 2):
                for j in range (-3, 2):
                    if MapProba[self.x + i, self.y + j] == 0:
                        try:
                            if MapProba[self.x + i, self.y + j].L[1] == 0:
                                MapBelief[self.x+i, self.y+j].L[1] *= 1
                            except: 
                                pass
            for i in range(-1,2):
                for j in range (-1,2):
                    try:
                        if MapProba[self.x + i, self.y + j].L[1] == 0:
                            MapBelief[self.x+i, self.y+j].L[1] *= 0.6
                    except: 
                        pass
        elif self.L[1] == 0.6:
            for i in range(-1,2):
                for j in range (-1,2):
                    try:
                        if MapProba[self.x + i, self.y + j].L[1] == 0:
                            MapBelief[self.x+i, self.y+j].L[1] *= 1
                    except: 
                        pass
        else:
            print("Wow un humain à sauver en case ", self.x,", ", self.y)


                    
            
            
                
                
        

            
def findMaxL(L1, L2):
    maxlist = []
    for i in range(len(L1)):
        maxlist.append( max(L1[i], L2[i]) )
    return maxlist
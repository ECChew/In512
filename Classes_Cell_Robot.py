import numpy as np


class Cell: 
    def __init__(self, xValue, yValue):
        #[Wall, Human, Explored, Position]
        self.L = [0, 0, 0, 0]
        self.x = xValue
        self.y = yValue
        
    #Spread the information of a human 2 cells around
    def Set_Human(self, Map):
        self.L = [0, 1, 0, 0]
        
        for i in range(-1,2):
            for j in range (-1,2):
                try:
                    findMaxL(Map[self.x + i, self.y + j].L, [0, 0.6, 0, 0])
                except:
                    pass
                
        for i in range(-1,2):
            for j in range (-1,2):
                try:
                    findMaxL(Map[self.x + 2*i, self.y + 2*j].L, [0, 0.3, 0, 0])
                except:
                    pass
    # Spread the information of a wall 1 cell around 
    def Set_Wall(self, Map):
        self.L = [1, 0, 0, 0]
        
        for i in range(-1,2):
            for j in range (-1,2):
                try:
                    findMaxL(Map[self.x + i, self.y + j].L, [0.5, 0, 0, 0])
                except:
                    pass
            
        
class Robot():
    def __init__(self, xValue, yValue):
        # self.L = [0, 0, 0, 1]
        self.x = xValue
        self.y = yValue
    
    def Check_Human(self, Map):
        Case = Map[self.x, self.y]
        if Case.L[1] == 1:
            print("Humain trouvé et à vendre")
            
            
def findMaxL(L1, L2):
    maxlist = []
    for i in range(len(L1)):
        maxlist.append( max(L1[i], L2[i]) )
    return maxlist
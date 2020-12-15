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
        self.ListWall = []
        self.ListHuman = []
        for i in range(-1,2):
            for j in range (-1,2):
                try:
                    if Map[self.x+i, self.y+j].L[0] != 1:           #If wall no spread of human
                        
                        #print("i - " ,i , "j - ", j ,Map[self.x + i, self.y + j].L)
                        Map[self.x+i, self.y+j].L = findMaxL(Map[self.x + i, self.y + j].L, [0, 0.6, 0, 0])
                    else:
                        self.ListWall.append([self.x+i, self.y+j])
                        self.ListHuman.append([self.x, self.y])
                except:
                    pass
                
        for i in range(-2,3):
            for j in range (-2,3):
                try:
                    if Map[self.x+i, self.y+j].L[0] != 1: 
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
                
    def RemoveThroughWall(self, Map):
        try:
            for i in range(len(self.ListHuman)):
                xval = self.ListHuman[i][0] - self.ListWall[i][0]         # xval = 0, -1, 1 
                yval = self.ListHuman[i][1] - self.ListWall[i][1]         # yval = 0, -1, 1
                if (xval == 1 or xval ==-1) and yval == 0:
                    for j in range(-1,2):
                        Map[self.ListWall[i][0]-xval, self.ListWall[i][1]+j].L[1] = 0
                elif xval == 0 and (yval == 1 or yval == -1):
                    for j in range(-1,2):
                        Map[self.ListWall[i][0]+j, self.ListWall[i][1]-yval].L[1] = 0
                else:
                    Map[self.ListWall[i][0]-xval, self.ListWall[i][1]-yval].L[1] = 0
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
                    if MapProba[self.x+i, self.y+j].L[2] == 1:
                        pass
                    else:
                        try:
                            if MapProba[max(self.x + i, 0), max(self.y + j, 0)].L[2] == 0:
                                MapBelief[max(self.x + i,0), max(self.y + j, 0)].L[0] *= 0.001
                        except:
                            pass
        else:
            for i in range(-1,2):
                for j in range (-1,2):
                    if MapProba[self.x+i, self.y+j].L[2] == 1:
                        pass
                    else:
                        try:
                            if MapProba[max(self.x + i, 0), max(self.y + j, 0)].L[2] == 0:
                                MapBelief[max(self.x + i,0), max(self.y + j, 0)].L[0] *= 1
                        except:
                            pass
    
    def Prediction_Human(self, MapProba, MapBelief):

        if self.L[1] == 0:
            for i in range(-2,3):
                for j in range (-2,3):
                    #print("Human prediction", max(self.x + i, 0), max(self.y + j, 0))
                    if MapProba[self.x+i, self.y+j].L[2] == 1:
                        pass
                    else:
                        try:
                            if self.x+i >= 0 and self.y+j >= 0:
                                MapBelief[(self.x + i), (self.y + j)].L[1] *= 0.1
                        except:
                            pass
        elif self.L[1]==0.3:
            for i in range (-2, 3):
                for j in range (-2, 3):
                    if MapProba[self.x+i, self.y+j].L[2] == 1:
                        pass
                    else:
                        try:
                            if self.x + i >= 0 and self.y + j >= 0:
                                MapBelief[self.x + i, self.y + j].L[1] *= 1
                        except:
                            pass
            for i in range(-1,2):
                for j in range (-1,2):
                    if MapProba[self.x+i, self.y+j].L[2] == 1:
                        pass
                    else:
                        try:
                            if self.x+i >= 0 and self.y+j >= 0:
                                MapBelief[(self.x + i), (self.y + j)].L[1] *= 0.6
                        except:
                            pass
        elif self.L[1] == 0.6:
            for i in range(-1,2):
                for j in range (-1,2):
                    if MapProba[self.x+i, self.y+j].L[2] == 1:
                        pass
                    else:
                        try:
                            if self.x + i >= 0 and self.y + j >= 0:
                                MapBelief[(self.x + i), (self.y + j)].L[1] *= 1
                        except:
                            pass
        else:
            print("Wow un humain à sauver en case ", self.x,", ", self.y)
    
    def Aleatoire(self, MapProba, MapBelief):
        MapProba[self.x, self.y].L[2] = 1
        self.Possibility=[]
        if self.L == [0,0]:
            for i in range(-1,2):
                for j in range(-1,2):
                    try:
                        if self.x + i >= 0 and self.y + j >= 0: 
                            if MapProba[self.x+i, self.y+j].L[2]!= 1:
                                self.Possibility.append([self.x+i, self.y+j])
                    except:
                        pass
            print(self.Possibility[2])
        #MapBelief[self.Possibility[0][0],self.Possibility[0][1]].run(MapProba, MapBelief)
    
    
    def ProbabilisticWay(self, MapProba, MapBelief):
       MapProba[self.x, self.y].L[2] = 1
       self.Around = []
       self.Liste = []
       if self.L != [0,0]:
            for i in range(-1,2):
                for j in range(-1,2):
                    try:
                        if self.x + i >= 0 and self.y + j >= 0: 
                            if MapProba[self.x+i, self.y+j].L[2] != 1:
                                self.Around.append([self.x+i, self.y+j])
                                self.Liste.append(MapBelief[self.x+i, self.y+j].L)
                    except:
                        pass
            self.BestWay, self.Index = minimize(self.Liste,self.Around)
            print(self.Index)
            #print("Ratio wall/Human : ", self.BestWay,"at Position :", self.Index, "Belief : ",MapBelief[self.Index[0],self.Index[1]].L)
       #MapBelief[self.Index[0],self.Index[1]].run(MapProba, MapBelief)
        
        
    def run(self, MapProba, MapBelief):
        self.ConfirmBelief(MapProba)
        self.Prediction_Wall(MapProba, MapBelief)
        self.Prediction_Human(MapProba, MapBelief)
        self.ConfirmBelief(MapProba) # We reconfirm as the predictions will also predict on the case we are on
        
                    
    def Mouvement(self, MapProba, MapBelief):
        self.ConfirmBelief(MapProba)
        self.Prediction_Wall(MapProba, MapBelief)
        self.Prediction_Human(MapProba, MapBelief)
        self.ConfirmBelief(MapProba)
        if self.L == [0,0]:
            self.Aleatoire( MapProba, MapBelief)
        else:
            self.ProbabilisticWay( MapProba, MapBelief)
            
                
                
        

            
def findMaxL(L1, L2):
    maxlist = []
    for i in range(len(L1)):
        maxlist.append( max(L1[i], L2[i]))
    return maxlist

def minimize(LBelief,LPos): 
    #print ("LBelief ", LBelief)
    #print ("LPos ", LPos)
    Lowest = 1
    Index = 0
    for i in range(len(LBelief)):
        if LBelief[i][0]/LBelief[i][1]<Lowest:
            Lowest = LBelief[i][0]/LBelief[i][1]
            Index += 1
        
    return Lowest, LPos[Index]

    
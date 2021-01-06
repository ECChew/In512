import numpy as np
import sys
#Chaque case de la GridProba est une Cell 
class Cell: 
    def __init__(self, xValue, yValue):
        #[Wall, Human, Explored, WallAround]
        self.L = [0, 0, 0, 0]
        #Position de la cell
        self.x = xValue
        self.y = yValue
        
    #Spread the information of a human 2 cells around
    def Set_Human(self, Map):
        self.L = findMaxL_Human([0, 1, 0, 0], self.L) 
        self.ListWall = []
        self.ListHuman = []
        for i in range(-1,2):
            for j in range (-1,2):
                try:
                    if Map[self.x+i, self.y+j].L[0] != 1:           #If wall no spread of human
                        
                        #print("i - " ,i , "j - ", j ,Map[self.x + i, self.y + j].L)
                        Map[self.x+i, self.y+j].L = findMaxL_Human(Map[self.x + i, self.y + j].L, [0, 0.6, 0, 0])
                    else:
                        self.ListWall.append([self.x+i, self.y+j])
                        self.ListHuman.append([self.x, self.y])
                except:
                    pass
                
        for i in range(-2,3):
            for j in range (-2,3):
                try:
                    if Map[self.x+i, self.y+j].L[0] != 1: 
                        Map[self.x+i, self.y+j].L = findMaxL_Human(Map[self.x + i, self.y + j].L, [0, 0.3, 0, 0])
                except:
                    pass
                
    # Spread the information of a wall 1 cell around 
    def Set_Wall(self, Map):
        self.L = [1, 0, 0, 1]
        
        for i in range(-1,2):
            for j in range (-1,2):
                try:
                    Map[self.x+i, self.y+j].L = findMaxL_Wall(Map[self.x + i, self.y + j].L, [0.5, 0, 0, 0.5])
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
        self.L = [0, 0, 1, 0]
        Map[self.x, self.y].L = findMaxL_Human(Map[self.x, self.y].L, self.L)
        

#Chaque case de la GridBelief est un Believe         
class Believe():
    def __init__(self, xValue, yValue):
        #1 = Presence, 0 = absence
        #[Wall, Human]
        self.x = xValue
        self.y = yValue
        self.L = [1,1,1]
        self.HumanFound = []
        
    def ConfirmBelief(self, Map):
        self.L = Map[self.x, self.y].L[:2] # Found using sensor at cell
        self.L.append(Map[self.x, self.y].L[3])

   
    def Prediction_Wall(self, MapProba, MapBelief):
#        print("-------------------------------------------------------------------------------")
#        print ("GRIDPROBA WALL at ",self.x, self.y, " == ",self.L[0])
        if self.L[0] == 0:
            for i in range(-1,2):
                for j in range (-1,2):
                    try:
                        if MapProba[self.x+i, self.y+j].L[2] == 1:
                            pass
                        else:
                            if MapProba[max(self.x + i, 0), max(self.y + j, 0)].L[2] == 0:
                                MapBelief[max(self.x + i,0), max(self.y + j, 0)].L[0] *= 0.001
                    except:
                        pass
        elif self.L[0] == 0.5:
            for i in range(-1,2):
                for j in range (-1,2):
                    try:
                        if MapProba[self.x+i, self.y+j].L[2] == 1:
                            pass
                        else:
                            if MapProba[max(self.x + i, 0), max(self.y + j, 0)].L[2] == 0:
                                if self.x + i == 0 or self.x + i == 20 or self.y + j == 0 or self.y + j == 20:
#                                    MapBelief[max(self.x + i,0), max(self.y + j, 0)].L[0] *= 0.9
#                                else:
                                    MapBelief[max(self.x + i,0), max(self.y + j, 0)].L[0] *= 1
                    except:
                        pass
        else: 
            print("Wow le robot a mangé un mur ", self.x,", ", self.y)
            sys.exit()
    
    
    
    
    
    def Prediction_Human(self, MapProba, MapBelief):
        if self.L[1] == 0:
            for i in range(-2,3):
                for j in range (-2,3):
                    #print("Human prediction", max(self.x + i, 0), max(self.y + j, 0))
                    try:
                        if MapProba[self.x+i, self.y+j].L[2] == 1:
                            pass
                        else:
                                if self.x+i >= 0 and self.y+j >= 0 and self.x + i < 20 and self.y + j <20 :
                                    MapBelief[(self.x + i), (self.y + j)].L[1] = 0
                    except:
                        pass
        elif self.L[1]==0.3:
            for i in range (-2, 3):
                for j in range (-2, 3):
                    try:
                        if MapProba[self.x+i, self.y+j].L[2] == 1:
                            pass
                        else:
                            
                                if self.x + i >= 0 and self.y + j >= 0 and self.x + i < 20 and self.y + j <20:
                                    MapBelief[self.x + i, self.y + j].L[1] *= 1
                    except:
                        pass
            for i in range(-1,2):
                for j in range (-1,2):
                    try:
                        if MapProba[self.x+i, self.y+j].L[2] == 1:
                            pass
                        else:
                            
                                if self.x+i >= 0 and self.y+j >= 0 and self.x + i < 20 and self.y + j <20:
                                    MapBelief[(self.x + i), (self.y + j)].L[1] *= 0.6
                    except:
                        pass
        elif self.L[1] == 0.6:
            try:
                for i in range(-1,2):
                    for j in range (-1,2):
                        if MapProba[self.x+i, self.y+j].L[2] == 1:
                            pass
                        else:
                            
                                if self.x + i >= 0 and self.y + j >= 0 and self.x + i < 20 and self.y + j <20:
                                    MapBelief[(self.x + i), (self.y + j)].L[1] *= 1
            except:
                pass
        else:
            print("-----------------------------------------------")
            print("Wow un humain à sauver en case ", self.x,", ", self.y)
            print("-----------------------------------------------")
#            try:
#                for i in range(-2,3):
#                    for j in range (-2,3):
#                        MapProba[self.x+i, self.y+j].L[1]=0
#            except:
#                pass
#                    
#            for k in range(len(MapProba)):
#                for l in range(len(MapProba)):
#                    if MapProba[k,l].L[1]==1:
#                        MapProba[k,l].Set_Human(MapProba)
#                        MapProba[k,l].RemoveThroughWall(MapProba)
            #MapBelief[self.x, self.y].Move(MapProba, MapBelief)
    
    
    
    
    def Aleatoire(self, MapProba, MapBelief):
        #print("Aleatoire : Position actuelle", self.x, self.y )
        MapProba[self.x, self.y].L[2] = 1
        self.Possibility = []
        self.Around = []
        if self.L == [0,0,0]:
            for i in range(-1,2):
                for j in range(-1,2):
                    try:
                        #print(self.x + i, self.y + j)
                        if self.x + i >= 0 and self.y + j >= 0 and self.x + i < 20 and self.y + j <20: 
                            if MapProba[self.x+i, self.y+j].L[2]!= 1:
                                #print("=====",self.x + i, self.y + j)
                                self.Possibility.append([self.x+i, self.y+j])
                    except:
                        pass
               
        if len(self.Possibility) >=2:
            #print(" ---------------------------------------")
            #print(self.Possibility)
            print("Aleatoire - Case suivante : ",self.Possibility[1])
            MapBelief[self.Possibility[1][0],self.Possibility[1][1]].Move(MapProba, MapBelief)
            #print("j'ai bougé")
        else:
            for i,j in zip([-1, -1, 1, 1],[-1, 1, -1, 1]):
                try:
                    self.Around.append([self.x+i, self.y+j])
                    self.Possibility.append(MapBelief[self.x+i, self.y+j].L)
                except:
                    pass
            self.BestWay, self.NextPos = minimize(self.Possibility, self.Around)
            print("j'ai bougé en ", self.NextPos[0], self.NextPos[1])
            #MapBelief[self.NextPos[0],self.NextPos[1]].Move(MapProba, MapBelief)
    
    
    
    
    
    def HumanAround(self, MapProba, MapBelief):  #If there is a human around use this method
        MapProba[self.x, self.y].L[2] = 1
        self.Around = []
        self.Liste = []
        self.LastPos = []
        
        if self.L[1] == 0.3:
            for i,j in zip([-1, -1, 1, 1],[-1, 1, -1, 1]):
                try: 
                    if self.x + i >= 0 and self.y + j >= 0 and self.x+i < 20 and self.y + j < 20:
                        if MapProba[self.x+i, self.y+j].L[2] != 1:
                            self.Around.append([self.x+i, self.y+j])
                            self.Liste.append(MapBelief[self.x+i, self.y+j].L)
                except:
                    pass
            self.BestWay, self.NextPos = FindTheHumanAround(self.Liste, self.Around)
            print("Human Around- 0,3 - Next posi" ,self.NextPos)
            MapBelief[self.NextPos[0],self.NextPos[1]].Move(MapProba, MapBelief)
            
        if self.L[1] == 0.6:
            print("Suis-je Passer dans cette boucle : ", self.x, self.y)
            for i in range(-1,2):
                for j in range(-1,2):
                    print("i : ", i, "j : ", j)
                    try: 
                        print(self.x +i , self.y+j)
                        if self.x + i >= 0 and self.y + j >= 0 and self.x+i < 20 and self.y + j < 20:
                            if MapProba[self.x+i, self.y+j].L[2] != 1 and MapBelief[self.x+i, self.y+j].L[0] != 1:
                                MapBelief[self.x+i, self.y+j].Move(MapProba,MapBelief)
                                if MapBelief[self.x+i, self.y+j].L[1] == 1:
                                    print("----------MAIS JE SUIS LA 1-------")
                                    
                                    
                                    for k in range(-2,3):
                                        for l in range (-2,3):
                                            if self.x + i + k >= 0 and self.y + j+l >= 0 and self.x+i+k < 20 and self.y + j + l< 20:
                                                #print("k : ", k , "l : ", l)
                                                #print("a efaccer",self.x+i+k, self.y+j+l)
                                                MapProba[self.x+i+k, self.y+j+l].L[1]=0
                                    self.ConfirmBelief(MapProba)
                                    
                                    print("----------MAIS JE SUIS LA 2-------")      
                                    for k in range(len(MapProba)):
                                        for l in range(len(MapProba)):
                                            if MapProba[k,l].L[1]==1:
                                                MapProba[k,l].Set_Human(MapProba)
                                                MapProba[k,l].RemoveThroughWall(MapProba)
                                                
                                    self.Aleatoire(MapProba,MapBelief)
                                    return

                                else:
                                    #print("---------Raté c'est pas ici----------")
                                    MapBelief[self.x, self.y].Move(MapProba,MapBelief)
                                    self.LastPos = [self.x+i, self.y+j]
                                
                    except:
                        pass
            
            
    def ProbabilisticWay(self, MapProba, MapBelief):
       MapProba[self.x, self.y].L[2] = 1
       self.Around = []
       self.Liste = []
       if self.L != [0,0]:
            for i in range(-1,2):
                for j in range(-1,2):
                    try:
                        if self.x + i >= 0 and self.y + j >= 0 and self.x + i < 20 and self.y + j <20 : 
                            if MapProba[self.x+i, self.y+j].L[2] != 1:
                                
                                self.Around.append([self.x+i, self.y+j])
                                self.Liste.append(MapBelief[self.x+i, self.y+j].L)
                    except:
                        pass
            self.BestWay, self.NextPos = minimize(self.Liste,self.Around)
            print("ProbaWay - Next posi" ,self.NextPos)
            #MapBelief[self.NextPos[0],self.NextPos[1]].Move(MapProba, MapBelief)
            #print("Ratio wall/Human : ", self.BestWay,"at Position :", self.NextPos, "Belief : ",MapBelief[self.Index[0],self.Index[1]].L)
       #MapBelief[self.Index[0],self.Index[1]].run(MapProba, MapBelief)
    
    def CompteurWall(self, MapProba, MapBelief):
        nbrWall = 0
        for n in range(5):
            if self.L[2] == 0.5**n:
                for i in range(-1,2):
                    for j in range(-1,2):
                        if MapBelief[self.x+i, self.y+j].L[0] == 1:
                            nbrWall += 1
                if nbrWall == n:
                    pass
        
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
        if self.L == [0,0,0]:
            self.Aleatoire( MapProba, MapBelief)
        elif self.L[1] != 0:
            self.HumanAround(MapProba, MapBelief)
        else:
            self.ProbabilisticWay( MapProba, MapBelief)
            
    
    def Move(self, MapProba, MapBelief):
        #print("Position actuelle:", self.x , self.y)
        self.ConfirmBelief(MapProba)
        self.Prediction_Wall(MapProba, MapBelief)
        self.Prediction_Human(MapProba, MapBelief)
        self.ConfirmBelief(MapProba)
                
        

def PosHuman(x_Human, y_Human, Map):
        for x,y in zip(x_Human, y_Human):
            Map[x,y].Set_Human(Map)
            Map[x,y].RemoveThroughWall(Map)


            
def findMaxL_Human(L1, L2):
    maxlist = []
    for i in range(len(L1)):
        maxlist.append( max(L1[i], L2[i]))    
    return maxlist

def findMaxL_Wall(L1, L2):
    maxlist = []
    if L1[3] == 0:
        for i in range(len(L1)):
            maxlist.append( max(L1[i], L2[i]))
    else:
        for i in range(len(L1)-1):
            maxlist.append( max(L1[i], L2[i])) 
        maxlist.append(L1[3]*0.5)
    return maxlist

def minimize(LBelief,LPos): 
    #print("-----------------------------")
    #print ("LBelief ", LBelief)
    #print ("LPos ", LPos)
    Index = 0
    Priorite = 0
    ratio = []
    for element in range(len(LBelief)):
        ratio.append(LBelief[element][1]-LPos[element][0])
    for i in range(len(LBelief)):
        if LBelief[i][0] < 0.001:
            Priorite += 1
    #print ("Priorite = : ",Priorite)
    if Priorite <= 2:
        #print("Priorite = : ", Priorite)
        #print("Ratio :",ratio)
        Lowest = 1
        for i in range(len(LBelief)):
            if LBelief[i][0] < Lowest:
                Lowest = LBelief[i][0] 
                Index = i
        print ("---Low---", Lowest, Index, LPos[Index])
        return Lowest, LPos[Index]
    
    else:
        Index_High = 0 
        Highest = 0
        #print ("Priorite = : ", Priorite)
        for i in range(len(LBelief)):
            if LBelief[i][1] > Highest:
                Highest = LBelief[i][1]
                Index_High = i
        print ("---High---", Highest, Index_High, LPos[Index_High])
        return Highest, LPos[Index_High]


def FindTheHumanAround(LBelief, LPos):
    print("-----------------------------")
    print ("LBelief ", LBelief)
    print ("LPos ", LPos)
    NextPos = []
    Highest = 0
    Identique = LBelief[0][1]
    Compteur = 0
    for i in range(len(LBelief)):
        if Identique == LBelief[i][1]:
            Compteur += 1
    print("Compteur = ", Compteur , "len(LBelief) = ", len(LBelief))
    if Compteur == len(LBelief):
        Highest = Identique
        NextPos = LPos[len(LBelief)//2]
    else:
        for i in range(len(LBelief)):
            if LBelief[i][1] >=  Highest:
                Highest = LBelief[i][1]
                NextPos = LPos[i]
    #print("Highest", Highest, NextPos)
    return Highest, NextPos

   

    
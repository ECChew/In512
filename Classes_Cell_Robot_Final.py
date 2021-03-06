# -*- coding: utf-8 -*-
"""
Created on Sat Jan  9 03:18:02 2021

@author: franc
"""

import numpy as np
import sys
import movementCounter


# Chaque case de la GridProba est une Cell

def incrementCounter():
    movementCounter.mvtCounter += 1


def incrementHuman():
    movementCounter.humanCount += 1


def addPos(x, y):
    movementCounter.positions.append([x, y])


def savedHuman(x, y):
    movementCounter.humanPositions.append([x, y])


class Cell:
    def __init__(self, xValue, yValue):
        # [Wall, Human, Explored, WallAround]
        self.L = [0, 0, 0]
        # Position de la cell
        self.x = xValue
        self.y = yValue

    # Spread the information of a human 2 cells around
    def Set_Human(self, Map):
        self.L = findMaxL_Human([0, 1, 0], self.L)
        self.ListWall = []
        self.ListHuman = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                try:
                    if Map[self.x + i, self.y + j].L[0] != 1:  # If wall no spread of human

                        # print("i - " ,i , "j - ", j ,Map[self.x + i, self.y + j].L)
                        Map[self.x + i, self.y + j].L = findMaxL_Human(Map[self.x + i, self.y + j].L, [0, 0.6, 0])
                    else:
                        self.ListWall.append([self.x + i, self.y + j])
                        self.ListHuman.append([self.x, self.y])
                except:
                    pass

        for i in range(-2, 3):
            for j in range(-2, 3):
                try:
                    if Map[self.x + i, self.y + j].L[0] != 1:
                        Map[self.x + i, self.y + j].L = findMaxL_Human(Map[self.x + i, self.y + j].L, [0, 0.3, 0])
                except:
                    pass

    # Spread the information of a wall 1 cell around
    def Set_Wall(self, Map):
        self.L = findMaxL_Wall([1, 0, 0], self.L)

        for i in range(-1, 2):
            for j in range(-1, 2):
                try:
                    Map[self.x + i, self.y + j].L = findMaxL_Wall(Map[self.x + i, self.y + j].L, [0.5, 0, 0])
                except:
                    pass

    def RemoveThroughWall(self, Map):
        try:
            for i in range(len(self.ListHuman)):
                xval = self.ListHuman[i][0] - self.ListWall[i][0]  # xval = 0, -1, 1
                yval = self.ListHuman[i][1] - self.ListWall[i][1]  # yval = 0, -1, 1
                if (xval == 1 or xval == -1) and yval == 0:
                    for j in range(-1, 2):
                        Map[self.ListWall[i][0] - xval, self.ListWall[i][1] + j].L[1] = 0
                elif xval == 0 and (yval == 1 or yval == -1):
                    for j in range(-1, 2):
                        Map[self.ListWall[i][0] + j, self.ListWall[i][1] - yval].L[1] = 0
                else:
                    Map[self.ListWall[i][0] - xval, self.ListWall[i][1] - yval].L[1] = 0
        except:
            pass

    def Set_Robot(self, Map):
        self.L = [0, 0, 1]
        Map[self.x, self.y].L = findMaxL_Human(Map[self.x, self.y].L, self.L)


# Chaque case de la GridBelief est un Believe
class Believe():
    def __init__(self, xValue, yValue):
        # 1 = Presence, 0 = absence
        # [Wall, Human]
        self.x = xValue
        self.y = yValue
        self.L = [1, 1]
        self.HumanFound = []
        self.WallValid = 0
        self.Longueur = 1
        self.Visit = 0
        self.hitWall = 0

#Take the information of the GridProba
    def ConfirmBelief(self, Map):
        #
        self.L = Map[self.x, self.y].L[:2]  # Found using sensor at cell
        # print("Confirm : ", self.L)

#Spread or not the wall, depending on the cell it is  
    def Prediction_Wall(self, MapProba, MapBelief): 
        
        #        print("-------------------------------------------------------------------------------")
        #        print ("GRIDPROBA WALL at ",self.x, self.y, " == ",self.L[0])
        if self.L[0] == 0:
            for i in range(-1, 2):
                for j in range(-1, 2):
                    try:
                        if MapProba[self.x + i, self.y + j].L[2] == 1:
                            pass
                        else:
                            if MapProba[max(self.x + i, 0), max(self.y + j, 0)].L[2] == 0:
                                MapBelief[max(self.x + i, 0), max(self.y + j, 0)].L[0] *= 0.001
                    except:
                        pass
        elif self.L[0] == 0.5:
            for i in range(-1, 2):
                for j in range(-1, 2):
                    try:
                        if MapProba[self.x + i, self.y + j].L[2] == 1:
                            pass
                        else:
                            if MapProba[max(self.x + i, 0), max(self.y + j, 0)].L[2] == 0:
                                if self.x + i == 0 or self.x + i == 20 or self.y + j == 0 or self.y + j == 20:
                                    #                                    MapBelief[max(self.x + i,0), max(self.y + j, 0)].L[0] *= 0.9
                                    #                                else:
                                    MapBelief[max(self.x + i, 0), max(self.y + j, 0)].L[0] *= 1
                    except:
                        pass
        else:

            print("-------------------------------------------------")
            print("Wall hit ", self.x, ", ", self.y)
            print("-------------------------------------------------")


#try to find a straight wall if 3 cells safe around it
    def StraightWall(self, MapBelief):
        #print("Straight wall ", self.x, self.y)
        Walls = [[-1, 0], [1, 0], [0, -1], [0, 1]]
        for i, j in zip([-1, 1, 0, 0], [0, 0, -1, 1]):
            # print (MapBelief[self.x+i, self.y+j].L[0],i,j, self.x+i, self.y+j)
            if self.x + i >= 0 and self.y + j >= 0 and self.x + i < 20 and self.y + j < 20:
                if MapBelief[self.x + i, self.y + j].L[0] == 0.5 or MapBelief[self.x + i, self.y + j].L[0] == 0.2:
                    # print (MapBelief[self.x+i, self.y+j].L[0],i,j)
                    Walls.remove([i, j])
        #print("--- Walls", Walls)
        if len(Walls) == 1:
            #print("3 cases visite ou sure!!")
            MapBelief[self.x + Walls[0][0], self.y + Walls[0][1]].L[0] = 1
            MapBelief[self.x + 2 * Walls[0][0], self.y + 2 * Walls[0][1]].L[0] = 1
            MapBelief[self.x + Walls[0][0], self.y + Walls[0][1]].WallValid = 1
            MapBelief[self.x + 2 * Walls[0][0], self.y + 2 * Walls[0][1]].WallValid = 1

            return Walls

#Count the number of wall around the cell, between 0 and 3
    def WallAround(self, MapProba, MapBelief):
        Diag = []
        self.WallsPos = []
        for i, j in zip([-1, 1, 0, 0], [0, 0, -1, 1]):
            try:
                #                print("Wallaround, i,j ", i,j , "x+i,y+j :",self.x+i, self.y+j)
                if self.x + i >= 0 and self.y + j >= 0 and self.x + i < 20 and self.y + j < 20 and self.L[0] == 0.5:
                    #                    print("La belief wall en +i , +j",i,j,MapBelief[self.x+i,self.y+j].L[0])
                    if MapBelief[self.x + i, self.y + j].L[0] < 0.5:
                        if MapProba[self.x + i, self.y + j].L[2] == 1:
                            Diag.append([i, j])
                        else:
                            # print("Wallaround, i,j ", i,j , "x+i,y+j :",self.x+i, self.y+j)
                            MapBelief[self.x + i, self.y + j].ConfirmBelief(MapProba)
                            if MapBelief[self.x + i, self.y + j].L[0] == 0:
                                Diag.append([i, j])
            except:
                pass


        if len(Diag) == 2:

            MapBelief[self.x - Diag[0][0] - Diag[1][0], self.y - Diag[0][1] - Diag[1][1]].L[0] = 1
            MapBelief[self.x - Diag[0][0] - Diag[1][0], self.y - Diag[0][1] - Diag[1][1]].WallValid = 1
            return 0, []
        for i, j in zip([-1, 1, 0, 0], [0, 0, -1, 1]):
            # print("i - j :",i, j)
            try:
                if self.x + i >= 0 and self.y + j >= 0 and self.x + i <= 20 and self.y + j <= 20 and \
                        MapBelief[self.x + i, self.y + j].L[0] == 1:
                    self.WallsPos.append([i, j])
            except:
                pass
        return len(self.WallsPos), self.WallsPos

#Use a different method depending on the number of wall around
    def Nothing_Wall(self, MapProba, MapBelief, WallsPos):
        if len(WallsPos) == 2:
            self.DeuxMurs(MapProba, MapBelief, WallsPos)
        if len(WallsPos) == 3:
            self.TroisMurs(MapProba, MapBelief, WallsPos)
        else:
            self.UnOuZeroMur(MapProba, MapBelief, WallsPos)

#Find a wall pattern
    def ASpecificPattern(self, MapProba, MapBelief):
        Pourcent = PourcentPeople(MapBelief)
        for i, j in zip([-2, -2, 2, 2, -1, -1, 1, 1], [-1, 1, -1, 1, -2, 2, -2, 2]):
            try:
                if MapBelief[self.x + i, self.y + j].WallValid == 1:

                    if i == 2:
                        #print("Specific Pattern - la case ", self.x + 1, self.y, " est sure")
                        MapBelief[self.x + 1, self.y].L[0] = 0.2
                        MapBelief[self.x + 1, self.y - j].L[0] = 0.2
                        MapBelief[self.x + 1, self.y - 2 * j].L[0] = 0.2
                        if Pourcent < 0.5:
                            MapBelief[self.x + 1, self.y + j].run(MapProba, MapBelief)
                            MapBelief[self.x + 1, self.y].run(MapProba, MapBelief)
                            break
                    elif i == -2:
                        #print("Specific Pattern - la case ", self.x - 1, self.y, " est sure")
                        MapBelief[self.x - 1, self.y].L[0] = 0.2
                        MapBelief[self.x - 1, self.y - j].L[0] = 0.2
                        MapBelief[self.x - 1, self.y - 2 * j].L[0] = 0.2
                        if Pourcent < 0.5:
                            MapBelief[self.x - 1, self.y + j].run(MapProba, MapBelief)
                            MapBelief[self.x - 1, self.y].run(MapProba, MapBelief)

                            break
                    elif j == 2:
                        #print("Specific Pattern - la case ", self.x, self.y + 1, " est sure")
                        MapBelief[self.x, self.y + 1].L[0] = 0.2
                        MapBelief[self.x - i, self.y + 1].L[0] = 0.2
                        MapBelief[self.x - 2 * i, self.y + 1].L[0] = 0.2
                        if Pourcent < 0.5:
                            MapBelief[self.x + i, self.y + 1].run(MapProba, MapBelief)
                            MapBelief[self.x, self.y + 1].run(MapProba, MapBelief)
                            break
                    elif j == -2:
                        #print("Specific Pattern - la case ", self.x, self.y - 1, " est sure")
                        MapBelief[self.x, self.y - 1].L[0] = 0.2
                        MapBelief[self.x - i, self.y - 1].L[0] = 0.2
                        MapBelief[self.x - 2 * i, self.y - 1].L[0] = 0.2
                        if Pourcent < 0.5:
                            MapBelief[self.x + i, self.y - 1].run(MapProba, MapBelief)
                            MapBelief[self.x, self.y - 1].run(MapProba, MapBelief)
                            break
                else:  # 3 Mur aligné flemme de recursive
                    pass
            except:
                pass

#Method use if their is one/zero wall around
    def UnOuZeroMur(self, MapProba, MapBelief, WallsPos):
        if len(WallsPos) == 1:
            MapBelief[self.x + WallsPos[0][0], self.y + WallsPos[0][1]].ASpecificPattern(MapProba, MapBelief)
            if abs(WallsPos[0][1]) == 1:
                for k in [-2, -1, 0, 1, 2]:
                    try:
                        if self.x + k >= 0 and self.y + 2 * WallsPos[0][1] >= 0 and self.x + k <= 20 and self.y + 2 * \
                                WallsPos[0][1] <= 20:
                            if MapBelief[self.x + k, self.y + 2 * WallsPos[0][1]].WallValid != 1 or \
                                    MapProba[self.x + k, self.y + 2 * WallsPos[0][1]].L[2] == 0:
                                MapBelief[self.x + k, self.y + 2 * WallsPos[0][1]].L[1] = 1
                            MapBelief[self.x, self.y + WallsPos[0][1]].WallValid = 1
                            MapBelief[self.x, self.y + 2 * WallsPos[0][1]].L[0] = 0.2

                        # Si la case est explorer pas d'humains possible
                        if MapProba[self.x + k, self.y + 2 * WallsPos[0][1]].L[2] == 1:
                            MapBelief[self.x + k, self.y + 2 * WallsPos[0][1]].L[1] = 0
                            # MapBelief[self.x , self.y+WallsPos[0][1]].StraightWall(MapBelief)
                    except:
                        pass
            else:
                for k in [-2, -1, 0, 1, 2]:
                    try:
                        if self.x + 2 * WallsPos[0][0] >= 0 and self.y + k >= 0 and self.x + 2 * WallsPos[0][
                            0] <= 20 and self.y + k <= 20:
                            if MapBelief[self.x + 2 * WallsPos[0][0], self.y + k].WallValid != 1:
                                MapBelief[self.x + 2 * WallsPos[0][0], self.y + k].L[1] = 1
                            MapBelief[self.x + WallsPos[0][0], self.y].WallValid = 1
                            MapBelief[self.x + 2 * WallsPos[0][0], self.y].L[0] = 0.2
                            # MapBelief[self.x+WallsPos[0][0] , self.y].StraightWall(MapBelief)
                        if MapProba[self.x + 2 * WallsPos[0][0], self.y + k].L[2] == 1:
                            MapBelief[self.x + 2 * WallsPos[0][0], self.y + k].L[1] = 0
                    except:
                        pass
        elif WallsPos == []:
            #print("nothing is Empty")
            for i, j in zip([-1, 1, 0, 0], [0, 0, -1, 1]):
                # print("i - j :",i, j)
                if MapBelief[self.x + i, self.y + j].L[0] == 0.2:
                    #print("i - j :", i, j, self.x + i, self.y + j)
                    MapBelief[self.x + i, self.y + j].L[0] = 1
                    MapBelief[self.x + i, self.y + j].WallValid = 1
                    WallsPos.append([i, j])
                    if j == 1 or j == -1:
                        for k in [-2, -1, 0, 1, 2]:
                            MapBelief[self.x + k, self.y + 2 * j].L[1] = 1
                            MapBelief[self.x, self.y + 2 * j].L[0] = 0.2
                    else:
                        for k in [-2, -1, 0, 1, 2]:
                            MapBelief[self.x + 2 * i, self.y + k].L[1] = 1

#Method use if 2 walls around
    def DeuxMurs(self, MapProba, MapBelief, WallsPos):

        # Deux cas possible, les murs sont en diagonale => 1 mur existant , lautre est faux
        # Les murs sont sur la meme ligne/Colonne
        # Cas meme ligne/Colonne
        if [sum(x) for x in zip(WallsPos[0], WallsPos[1])] == [0, 0]:

            if WallsPos[0][0] != 0:  # LEs mur sont sur la meme colonne
                # Explore la derniere case (C'est un non mur), qui est sur la ligne

                # Si une et seulement une des deux cases est non explorer
                if (MapProba[self.x, self.y + 1].L[2] == 0 and not MapProba[self.x, self.y - 1].L[2] == 0) or (
                        not MapProba[self.x, self.y + 1].L[2] == 0 and MapProba[self.x, self.y - 1].L[2] == 0):
                    if MapProba[self.x, self.y + 1].L[2] == 0:
                        MapBelief[self.x, self.y + 1].Longueur += self.Longueur
                        if MapBelief[self.x, self.y + 1].Longueur == 3 and MapBelief[self.x, self.y + 1].L[1] == 0:
                            # MapBelief[self.x, self.y+1].run(MapProba,MapBelief)
                            MapBelief[self.x, self.y + 1].Longueur3(MapProba, MapBelief)

                        else:
                            MapBelief[self.x, self.y + 1].run(MapProba, MapBelief)

                    else:
                        MapBelief[self.x, self.y - 1].ConfirmBelief(MapProba)
                        MapBelief[self.x, self.y - 1].Longueur += self.Longueur
                        if MapBelief[self.x, self.y - 1].Longueur == 3 and MapBelief[self.x, self.y - 1].L[1] == 0:
                            MapBelief[self.x, self.y - 1].Longueur3(MapProba, MapBelief)
                        #                        elif: MapBelief[self.x, self.y-1].L[1] != 0:
                        #
                        else:
                            MapBelief[self.x, self.y - 1].Longueur3(MapProba, MapBelief)
                            hit = MapBelief[self.x, self.y - 1].Mouvement(MapProba, MapBelief)
                            if hit :
                                return

                elif MapProba[self.x, self.y + 1].L[2] == 0 and MapProba[self.x, self.y - 1].L[2] == 0:
                    if MapBelief[self.x, self.y + 1].L[0] < MapBelief[self.x, self.y - 1].L[0]:
                        MapBelief[self.x, self.y + 1].run(MapProba, MapBelief)
                    else:
                        hit = MapBelief[self.x, self.y - 1].Mouvement(MapProba, MapBelief)
                        if hit:
                            return
            else:
                if MapProba[self.x + 1, self.y].L[2] == 0:
#                    print(self.x + 1, self.y, "N'a pas ete explorer")
                    MapBelief[self.x + 1, self.y].Longueur += self.Longueur
                    if MapBelief[self.x + 1, self.y].Longueur == 3:
                        MapBelief[self.x + 1, self.y].Longueur3(MapProba, MapBelief)
                    else:
                        MapBelief[self.x + 1, self.y].run(MapProba, MapBelief)
                else:
#                    print(self.x - 1, self.y, "N'a pas ete explorer")
                    MapBelief[self.x - 1, self.y].Longueur += self.Longueur
                    if MapBelief[self.x - 1, self.y].Longueur == 3:
                        MapBelief[self.x - 1, self.y].Longueur3(MapProba, MapBelief)
                    else:
                        MapBelief[self.x - 1, self.y].run(MapProba, MapBelief)
                        # 2eme cas en diagonal
        else:
            # Si une des deux autre possibilités sont non exploré
            if (MapProba[self.x - WallsPos[0][0], self.y - WallsPos[0][1]].L[2] == 0 and not
            MapProba[self.x - WallsPos[1][0], self.y - WallsPos[1][1]].L[2] == 0) or (
                    not MapProba[self.x - WallsPos[0][0], self.y - WallsPos[0][1]].L[2] == 0 and
                    MapProba[self.x - WallsPos[1][0], self.y - WallsPos[1][1]].L[2] == 0):
                # Si la case 1 est non explorer
                if MapProba[self.x - WallsPos[0][0], self.y - WallsPos[0][1]].L[2] == 0:
                    # Je vais voir la case et confirm ses beliefs
                    MapBelief[self.x - WallsPos[0][0], self.y - WallsPos[0][1]].run(MapProba, MapBelief)

                    if MapBelief[self.x - WallsPos[0][0], self.y - WallsPos[0][1]].L[0] == 0:
                        WallsPos.remove([WallsPos[1][0], WallsPos[1][1]])
                        return

                if MapProba[self.x - WallsPos[1][0], self.y - WallsPos[1][1]].L[2] == 0:

                    MapBelief[self.x - WallsPos[1][0], self.y - WallsPos[1][1]].run(MapProba, MapBelief)
                    if MapBelief[self.x - WallsPos[1][0], self.y - WallsPos[1][1]].L[0] == 0:
                        WallsPos.remove([WallsPos[0][0], WallsPos[0][1]])


            elif MapProba[self.x - WallsPos[0][0], self.y - WallsPos[0][1]].L[2] == 0 and \
                    MapProba[self.x - WallsPos[1][0], self.y - WallsPos[1][1]].L[2] == 0:
                #print("Two unexplored cells")
                if MapProba[self.x - WallsPos[0][0], self.y - WallsPos[0][1]].L[2] == 0:
                    MapBelief[self.x - WallsPos[0][0], self.y - WallsPos[0][1]].run(MapProba, MapBelief)
                    MapBelief[WallsPos[1][0], WallsPos[1][1]].run(MapProba, MapBelief)
#                    if MapBelief[WallsPos[1][0], WallsPos[1][1]].L[0] == 0 and \
#                            MapBelief[self.x - WallsPos[0][0], self.y - WallsPos[0][1]].L[0] == 0:
#                        #print("Wall cell", self.x - WallsPos[0][0] - WallsPos[1][0],self.y - WallsPos[0][1] - WallsPos[1][1])

            else:

                for i, j in zip([-1, -1, 1, 1], [-1, 1, -1, 1]):
                    if MapProba[self.x + i, self.y + j].L[2] == 0 and MapBelief[self.x + i, self.y + j].L[0] != 1:
                        MapBelief[self.x + i, self.y + j].run(MapProba, MapBelief)
                        return

                WallHere, NoWall = self.ProbaNoWall(MapProba, MapBelief, WallsPos)
                #print("Un wall est posé en ", self.x + WallHere[0], self.y + WallHere[1], " et pas de wall en ",self.x + NoWall[0], self.y + NoWall[1])
                WallsPos.remove(NoWall)

                MapBelief[self.x + NoWall[0], self.y + NoWall[1]].L[0] = 0
                #print("Jai trouver une sortie")

#Get out of the wall if it stick for more than 3 cells
    def Longueur3(self, MapProba, MapBelief):
        self.run(MapProba, MapBelief)
        self.PréLongueur3(MapProba, MapBelief)
#        print("==================Longueur = 3", self.x, self.y)
        for i, j in zip([-1, 1, 0, 0], [0, 0, -1, 1]):
            if MapBelief[self.x + i, self.y + j].WallValid == 1:
#                print("==================Longueur = 3 et je vais en ", self.x - i, self.y - j)

                MapBelief[self.x - i, self.y - j].run(MapProba, MapBelief)
                break

    def PréLongueur3(self, MapProba, MapBelief):
        #print("Prelongueur", self.x, self.y)
        for i, j in zip([-3, -3, 3, 3, -1, -1, 1, 1], [-1, 1, -1, 1, -3, 3, -3, 3]):
            #print("case : ", self.x + i, self.y + j, MapBelief[self.x + i, self.y + j].WallValid)
            if MapBelief[self.x + i, self.y + j].WallValid == 1:
                MapBelief[self.x + i, self.y + j].StraightWall(MapBelief)


#Method use if there is 3 walls around
    def TroisMurs(self, MapProba, MapBelief, WallsPos):
        Walls = []
        #print("3 walls")
        for i, j in zip([-1, -1, 1, 1], [-1, 1, -1, 1]):
            try:
                if MapProba[self.x + i, self.y + j].L[2] == 0 and MapBelief[self.x + i, self.y + j].L[0] != 1:
                    if MapBelief[self.x + i, self.y + j].L[0] == 0.2:
                        for k, l in zip([-1, 1, 0, 0], [0, 0, -1, 1]):
                            #print("straight wall")
                            Walls = MapBelief[self.x + i + k, self.y + j + l].StraightWall(MapBelief)
                            #print("Fin tu straght walls:", WallsPos, "===", Walls)
                            if Walls != None and len(Walls) == 1:
                                try:
                                    WallsPos.remove(abs(Walls[0][1]), abs(Walls[0][0]))
                                    self.DeuxMurs(MapProba, MapBelief, WallsPos)
                                except:
                                    pass
                                break
                            else:
                                pass
                    else:
                        print("La case ", self.x + i, self.y + j, " est safe, allons y", self.x, self.y)
                        addPos(self.x + i, self.y + j)
                        return
            except:
                pass

        #print("ici?", self.x, self.y)
        for i in range(-1, 2):
            for j in range(-1, 2):
                try:
                    if MapProba[self.x + i, self.y + j].L[2] == 0 and MapBelief[self.x + i, self.y + j].L[0] != 1:
                        print("La case ", self.x + i, self.y + j, " est safe, allons y", self.x, self.y)
                        addPos(self.x + i, self.y + j)
                        MapBelief[self.x + i, self.y + j].run(MapProba, MapBelief)
                        break
                except:
                    pass

#Method use if there is 2 walls in diagonal
    def ProbaNoWall(self, MapProba, MapBelief, WallsPos):
        VerticalPosProba = 0.5
        HorizontalPosProba = 0.5
        for i in range(-5, 6):
            try:
                if MapBelief[self.x + WallsPos[0][0] + i, self.y + WallsPos[0][1]].WallValid == 1:
                    VerticalPosProba *= 0.5
                if MapBelief[self.x + WallsPos[0][0], self.y + WallsPos[0][1] + i].WallValid == 1:
                    VerticalPosProba *= 0.5
            except:
                pass
        for i in range(-5, 6):
            try:
                if MapBelief[self.x + WallsPos[1][0] + i, self.y + WallsPos[1][1]].WallValid == 1:
                    HorizontalPosProba *= 0.5
                if MapBelief[self.x + WallsPos[1][0], self.y + WallsPos[1][1] + i].WallValid == 1:
                    HorizontalPosProba *= 0.5
            except:
                pass
        if VerticalPosProba < HorizontalPosProba:
            WallHere = WallsPos[1]
            NoWall = WallsPos[0]
        else:
            WallHere = WallsPos[0]
            NoWall = WallsPos[1]
        return WallHere, NoWall



#Spread the human temperature
    def Prediction_Human(self, MapProba, MapBelief, WallsPos):
        if self.L[1] == 0:
            for i in range(-2, 3):
                for j in range(-2, 3):
                    try:
                        if MapProba[self.x + i, self.y + j].L[2] == 1:
                            pass
                        else:
                            if self.x + i >= 0 and self.y + j >= 0 and self.x + i <= 20 and self.y + j <= 20:
                                MapBelief[(self.x + i), (self.y + j)].L[1] = 0
                    except:
                        pass
        elif self.L[1] == 0.3:
            for i in range(-2, 3):
                for j in range(-2, 3):
                    try:
                        if MapProba[self.x + i, self.y + j].L[2] == 1:
                            pass
                        else:
                            if self.x + i >= 0 and self.y + j >= 0 and self.x + i <= 20 and self.y + j <= 20:
                                MapBelief[self.x + i, self.y + j].L[1] *= 1
                    except:
                        pass
            for i in range(-1, 2):
                for j in range(-1, 2):
                    try:
                        if MapProba[self.x + i, self.y + j].L[2] == 1:
                            pass
                        else:
                            if self.x + i >= 0 and self.y + j >= 0 and self.x + i <= 20 and self.y + j <= 20:
                                MapBelief[(self.x + i), (self.y + j)].L[1] *= 0.6
                    except:
                        pass
        elif self.L[1] == 0.6:
            try:
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        if MapProba[self.x + i, self.y + j].L[2] == 1:
                            pass
                        else:
                            if self.x + i >= 0 and self.y + j >= 0 and self.x + i <= 20 and self.y + j <= 20:
                                MapBelief[(self.x + i), (self.y + j)].L[1] *= 1
            except:
                pass
        else:
            # Human to be saved

            print("-----------------------------------------------")
            print("Human to save ", self.x, ", ", self.y)
            print("-----------------------------------------------")
            return
        if self.L == [0.5, 0.3] or self.L == [0.5, 0]:
            self.Nothing_Wall(MapProba, MapBelief, WallsPos)


#Check the value around if it sense a human temperature = 0.3
    def CheckValue03(self, MapProba, MapBelief):
        self.run(MapProba, MapBelief)
        MapProba[self.x, self.y].L[2] = 1
#        print("Check Value 0.3 ------", self.x, self.y, "------", self.L)
        if self.L[1] == 0.6:
            print("Je me rapproche il est a une case de ", self.x, self.y)
            xreprise, yreprise = self.Human_Around_06(MapProba, MapBelief)
            return xreprise, yreprise
        else:
            return None, None


    def Human_Around_03(self, MapProba, MapBelief):
        self.run(MapProba, MapBelief)
        MapProba[self.x, self.y].L[2] = 1
        for i, j in zip([-1, -1, 1, 1], [-1, 1, -1, 1]):

            try:
#                print("0.3 Si i=", i, "et j=", j, "x+i = ", self.x + i, "y+j = ", self.y + j)
                if MapProba[self.x + i, self.y + j].L[2] == 0 and MapBelief[self.x + i, self.y + j].L[0] != 1:
                    #print("Je satisfais les conditions")
                    xreprise, yreprise = MapBelief[self.x + i, self.y + j].CheckValue03(MapProba, MapBelief)
                    #print("0.3 Liste ", MapBelief[self.x + i, self.y + j].L)
                    if MapBelief[xreprise, yreprise].L[1] == 0:
#                        print("Belief people xreprise, yreprise = 0 à ", xreprise, yreprise)
                        addPos(xreprise, yreprise)
                        MapBelief[xreprise, yreprise].run(MapProba, MapBelief)
                        break

                else:
                    pass
                    #print("Je ne les respecte pas ")
            except:
                pass


#Check the value around if it sense a human temperature = 0.3
    def CheckValue06(self, MapProba, MapBelief, i=0, j=0):
        self.run(MapProba, MapBelief)
        MapProba[self.x, self.y].L[2] = 1
        #print("Check Value 0.6 ------", self.x, self.y, "------", self.L)
        if self.L[1] != 1:
            #print("Pas la bonne voie")
            return 0
        else:
            incrementHuman()
            savedHuman(self.x, self.y)
            for k in range(-2, 3):
                for l in range(-2, 3):
                    if self.x + k >= 0 and self.y + l >= 0 and self.x + i + k <= 20 and self.y + j + l <= 20:
                        MapProba[self.x + k, self.y + l].L[1] = 0
                        MapBelief[self.x + k, self.y + l].L[1] = 0

            for k in range(len(MapProba)):
                for l in range(len(MapProba)):
                    if MapProba[k, l].L[1] == 1:
                        MapProba[k, l].Set_Human(MapProba)
                        MapProba[k, l].RemoveThroughWall(MapProba)

            return 1, self.x, self.y

    def Human_Around_06(self, MapProba, MapBelief):
        self.run(MapProba, MapBelief)
        MapProba[self.x, self.y].L[2] = 1
        Found = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                try:
                    #print("\nSi i=", i, "et j=", j, "x+i = ", self.x + i, "y+j = ", self.y + j, "[", self.x, self.y,"]")
                    if MapProba[self.x + i, self.y + j].L[2] == 0 and MapBelief[self.x + i, self.y + j].L[0] != 1:
                        #print("Je satisfais les conditions je vais en", self.x + i, self.y + j)
                        Found, xreprise, yreprise = MapBelief[self.x + i, self.y + j].CheckValue06(MapProba, MapBelief,
                                                                                                   i, j)
                        #print("Liste ", MapBelief[self.x + i, self.y + j].L, "Found ", Found)

                        if MapBelief[self.x + i, self.y + j].L[1] == 0:
                            #print("Belief human = 0 autour de ", self.x, self.y)
                            return xreprise, yreprise
                    else:
                        pass
                        #print("Je ne satisfais pas les conditions je ne vais pas en", self.x + i, self.y + j)
                except:
                    continue
            if Found == 0:
                pass
            else:
                break


#Explore a direction if no information on the cell [0,0]
    def GoExplore(self, MapProba, MapBelief):
        MapProba[self.x, self.y].L[2] = 1
        #print("\n=========Exploration=====[", self.x, self.y, " ]===")
        # [Haut, Bas, Droite, Gauche]
        # print("Exploration")
        self.Direction = [0, 0, 0, 0]
        for i in range(self.x + 1, 20):
            self.Direction[1] += 1.5 * MapBelief[i, self.y].L[1] - MapBelief[i, self.y].L[1]
        for i in range(self.x):
            self.Direction[0] += 1.5 * MapBelief[i, self.y].L[1] - MapBelief[i, self.y].L[0]
        for i in range(self.y + 1, 20):
            self.Direction[2] += 1.5 * MapBelief[self.x, i].L[1] - MapBelief[self.x, i].L[0]
        for i in range(self.y):
            self.Direction[3] += 1.5 * MapBelief[self.x, i].L[1] - MapBelief[self.x, i].L[0]

        Maximoum = self.Direction.index(max(self.Direction))
        #print("Direction", self.Direction, Maximoum, self.x, self.y)
        if Maximoum == 0:
#            print("Exploration, NextStep : ", self.x - 1, self.y)
            hit = MapBelief[self.x - 1, self.y].Mouvement(MapProba, MapBelief)
            if hit:
                return

        elif Maximoum == 1:
#            print("Exploration, NextStep : ", self.x + 1, self.y)
            hit = MapBelief[self.x + 1, self.y].Mouvement(MapProba, MapBelief)
            if hit:
                return
        elif Maximoum == 2:
#            print("Exploration, NextStep : ", self.x, self.y + 1)
            hit = MapBelief[self.x, self.y + 1].Mouvement(MapProba, MapBelief)
            if hit:
                return
        else:
#            print("Exploration, NextStep : ", self.x, self.y - 1)
            hit = MapBelief[self.x, self.y - 1].Mouvement(MapProba, MapBelief)
            if hit:
                return
            
            
#Find the cell with the lowest probability of wall
    def ProbabilisticWay(self, MapProba, MapBelief):
        MapProba[self.x, self.y].L[2] = 1
        #print("\n=========ProbaWay====[", self.x, self.y, " ]====")
        self.Around = []
        self.Liste = []
        Compteur = 0
        if self.L != [0, 0]:
            for i in range(-1, 2):
                for j in range(-1, 2):
                    try:
                        if self.x + i >= 0 and self.y + j >= 0 and self.x + i <= 20 and self.y + j <= 20:
                            if MapProba[self.x + i, self.y + j].L[2] != 1:
                                if MapBelief[self.x + i, self.y + j].L[0] < 1e-9 and \
                                        MapBelief[self.x + i, self.y + j].L[0] != 0:
                                    MapBelief[self.x + i, self.y + j].run(MapProba, MapBelief)
                                    MapBelief[self.x, self.y].run(MapProba, MapBelief)
                                else:
                                    self.Around.append([self.x + i, self.y + j])
                                    self.Liste.append(MapBelief[self.x + i, self.y + j].L)

                    except:
                        pass
            for i in range(len(self.Liste)):
                if self.Liste[i][0] == 1:
                    Compteur += 1

            if Compteur == len(self.Liste):
                for j, k in zip([-1, -1, 1, 1], [-1, 1, -1, 1]):
                    try:
                        if MapBelief[self.x + j, self.y + k].L[0] != 1:
                            MapBelief[self.x + j, self.y + k].run(MapProba, MapBelief)
                    except:
                        pass
            else:
                self.BestWay, self.NextPos = minimize(self.Liste, self.Around)
                addPos(self.NextPos[0], self.NextPos[1])
                return


    def getOut(self, MapProba, MapBelief):
        """
        For the second phase of the exploration, provides a way to break the loop.
        """
        # [Haut, Bas, Droite, Gauche]

        self.coefExp = 5
        self.coefWall = 2
        self.Direction = [0, 0, 0, 0]
        # Left
        for j in range(0, self.y):
            if self.y + j >= 0:
                self.Direction[3] += (
                            self.coefExp * (1 - MapProba[self.x, j].L[2]) - self.coefWall * MapBelief[self.x, j].L[0])
            else:
                self.Direction[3] = -1
        # Right
        for j in range(self.y + 1, 20):
            if self.y + j < 20:
                self.Direction[2] += (
                            self.coefExp * (1 - MapProba[self.x, j].L[2]) - self.coefWall * MapBelief[self.x, j].L[0])
            else:
                self.Direction[2] = -1
        # Up
        for i in range(0, self.x):
            if self.x + i >= 0:
                self.Direction[0] += (
                            self.coefExp * (1 - MapProba[i, self.y].L[2]) - self.coefWall * MapBelief[i, self.y].L[0])
            else:
                self.Direction[0] = -1
        # Down
        for i in range(self.x + 1, 20):
            if self.x + i < 20:
                self.Direction[1] += (
                            self.coefExp * (1 - MapProba[i, self.y].L[2]) - self.coefWall * MapBelief[i, self.y].L[0])
            else:
                self.Direction[1] = -1
        maxDir = self.Direction.index(max(self.Direction))
        if maxDir == 0:
#            print(f"Get out of this area - Next position {self.x - 1, self.y}")
            self.nextpos = [self.x - 1, self.y]
        elif maxDir == 1:
#            print(f"Get out of this area - Next position {self.x + 1, self.y}")
            self.nextpos = [self.x + 1, self.y]
        elif maxDir == 2:
#            print(f"Get out of this area - Next position {self.x, self.y + 1}")
            self.nextpos = [self.x, self.y + 1]
        elif maxDir == 3:
#            print(f"Get out of this area - Next position {self.x, self.y - 1}")
            self.nextpos = [self.x, self.y - 1]
        addPos(self.nextpos[0], self.nextpos[1])
        hit = MapBelief[self.nextpos[0], self.nextpos[1]].Mouvement(MapProba, MapBelief)
        if hit == 1:
            return 1
        else:
            return 0

    def run(self, MapProba, MapBelief):
        print("Moving to ", self.x, self.y)
        incrementCounter()
        MapProba[self.x, self.y].L[2] = 1
        self.ConfirmBelief(MapProba)
        hit = self.Prediction_Wall(MapProba, MapBelief)
        nbrWalls, WallsPos = self.WallAround(MapProba, MapBelief)
        self.Prediction_Human(MapProba, MapBelief, WallsPos)
        self.ConfirmBelief(MapProba)  # We reconfirm as the predictions will also predict on the case we are on

    def Mouvement(self, MapProba, MapBelief, i=0, j=0):
        incrementCounter()
        print("Moving to ", self.x, self.y)
        if MapProba[self.x, self.y].L[0] == 1:
            self.hitWall = 1

            return 1
        self.ConfirmBelief(MapProba)
        MapProba[self.x, self.y].L[2] = 1
        hit = self.Prediction_Wall(MapProba, MapBelief)
        nbrWalls, WallsPos = self.WallAround(MapProba, MapBelief)
        if nbrWalls == 3 and self.L[1] == 0:
            self.TroisMurs(MapProba, MapBelief, WallsPos)
        else:
            self.Prediction_Human(MapProba, MapBelief, WallsPos)
            self.ConfirmBelief(MapProba)

            if self.x == 3 and MapProba[self.x - 1, self.y].L[2] != 1 and MapBelief[self.x - 1, self.y].L[0] != 1:
                hit = MapBelief[self.x - 1, self.y].Mouvement(MapProba, MapBelief)
                if hit :
                    return
            elif self.y == 3 and MapProba[self.x, self.y - 1].L[2] != 1 and MapBelief[self.x, self.y - 1].L[0] != 1:
                hit = MapBelief[self.x, self.y - 1].Mouvement(MapProba, MapBelief)
                if hit :
                    return
            elif self.L == [0, 0]:
                self.GoExplore(MapProba, MapBelief)
            elif self.L[1] == 0.3:
                self.Human_Around_03(MapProba, MapBelief)
            elif self.L[1] == 0.6:
                for i, j in zip([1, 1, -1, -1], [-1, 1, -1, 1]):
                    if MapBelief[self.x + i, self.y + j].WallValid == 1:
                        MapBelief[self.x - i, self.y + j].run(MapProba, MapBelief)

                        if MapBelief[self.x - i, self.y + j].L[0] != 0:
                            MapBelief[self.x + i, self.y - j].run(MapProba, MapBelief)
                incrementHuman()
                savedHuman(self.x - 1, self.y - 1)
                for k in range(-2, 3):
                    for l in range(-2, 3):
                        if self.x + k >= 0 and self.y + l >= 0 and self.x + k <= 20 and self.y + l <= 20:
                            MapProba[self.x + k - 1, self.y + l - 1].L[1] = 0
                            MapBelief[self.x + k - 1, self.y + l - 1].L[1] = 0
                for k in range(len(MapProba)):
                    for l in range(len(MapProba)):

                        if MapProba[k, l].L[1] == 1:
                            MapProba[k, l].Set_Human(MapProba)
                            MapProba[k, l].RemoveThroughWall(MapProba)
                #print("Je suis arrivé a la fin", self.x, self.y)
            else:
                self.ProbabilisticWay(MapProba, MapBelief)
        return 0


def PosHuman(x_Human, y_Human, Map):
    for x, y in zip(x_Human, y_Human):
        Map[x, y].Set_Human(Map)
        Map[x, y].RemoveThroughWall(Map)


def PourcentPeople(MapBelief):
    TotalCase = 20 * 20
    People = 0
    for i in range(len(MapBelief)):
        for j in range(len(MapBelief)):
            People += MapBelief[i, j].L[1]
    Pourcent = People / TotalCase
    return Pourcent



def findMaxL_Human(L1, L2):
    maxlist = []
    for i in range(len(L1)):
        maxlist.append(max(L1[i], L2[i]))
    return maxlist


def findMaxL_Wall(L1, L2):
    maxlist = []
    for i in range(len(L1)):
        maxlist.append(max(L1[i], L2[i]))
    return maxlist


def minimize(LBelief, LPos):
    #print("-----------------------------")
    #print("LBelief ", LBelief)
    #print("LPos ", LPos)
    Index = 0
    Priorite = 0
    nbr05 = 0

    liste05 = []
    listepos = []
    for i in range(len(LBelief)):
        if LBelief[i][0] == 0.5:
            nbr05 += 1
    if nbr05 >= 3:
        #print("Nombre 0,5")
        for i in range(len(LBelief)):
            if LBelief[i][0] == 0.5:
                liste05.append(LPos[i])
                listepos.append(i)
        #print(liste05, listepos, len(liste05) // 2)
        #print("aaaaa", liste05[len(liste05) // 2], listepos[len(liste05) // 2])
        return listepos[-1], liste05[-1]

    else:
        for i in range(len(LBelief)):
            if LBelief[i][0] < 0.001 and LBelief[i][0] > 1e-9:
                Priorite += 1
        #print("Priorite = : ", Priorite)
        if Priorite == 0:
            Lowest = 1

            for i in range(len(LBelief)):
                if LBelief[i][0] < Lowest:
                    Lowest = LBelief[i][0]
                    Index = i

            #print("---Low---", Lowest, Index, LPos[Index])
            return Lowest, LPos[Index]
        elif Priorite == 2 or Priorite == 1:
            # print("Priorite = : ", Priorite)

            Lowest = 1
            for i in range(len(LBelief)):
                if LBelief[i][0] <= Lowest and LBelief[i][0] > 1e-9:
                    Lowest = LBelief[i][0]
                    Index = i
            #        print ("---Low---", Lowest, Index, LPos[Index])
            return Lowest, LPos[Index]

        elif Priorite > 2:
            # print("Priorite = : ", Priorite)

            Lowest = 1
            for i in range(len(LBelief)):
                if LBelief[i][0] <= Lowest and LBelief[i][0] >= 1e-6:
                    Lowest = LBelief[i][0]
                    Index = i
            #        print ("---Low---", Lowest, Index, LPos[Index])
            return Lowest, LPos[Index]


def FindTheHumanAround(LBelief, LPos):
    NextPos = []
    Highest = 0
    Identique = LBelief[0][1]
    Compteur = 0
    for i in range(len(LBelief)):
        if Identique == LBelief[i][1]:
            Compteur += 1
    #    print("Compteur = ", Compteur , "len(LBelief) = ", len(LBelief))
    if Compteur == len(LBelief):
        Highest = Identique
        NextPos = LPos[len(LBelief) // 2]
    else:
        for i in range(len(LBelief)):
            if LBelief[i][1] >= Highest:
                Highest = LBelief[i][1]
                NextPos = LPos[i]
    # print("Highest", Highest, NextPos)
    return Highest, NextPos




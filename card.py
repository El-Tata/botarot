#!/usr/bin/env python2
# -*- coding: utf8 -*-

class Card():
    def __init__(self, trump, value, color, points):
        self.trump = trump
        self.value = value
        self.color = color
        self.points = points
        self.strg = self.setStrg()

    #endDef

    def setStrg(self):
        if self.isTrump():
            return "\x1b[1;37;43m " + self.trump[0:self.trump.find('.')] + " \x1b[0;0;0m "
        else:
            if self.color in ["Club", "Spade"]:
                finalStr = "\x1b[1;37;40m "
            elif self.color in ["Heart", "Diamond"]:
                finalStr = "\x1b[1;37;41m "
            #endIf
            if self.value == "King":
                finalStr += "Kg"
            elif self.value == "Knight":
                finalStr += "Kt"
            else:
                finalStr += self.value if len(self.value)<=2 else self.value[0]
            return finalStr + "_" + self.color[0] +" \x1b[0;0;0m "
        #endIf
    #endDef


    def isTrump(self):
        return (self.trump != None)
    #endDef

    def isOudler(self):
        return (self.isTrump() and (self.trump == "1.I - The Magician" or self.trump == "0.0 - The Fool" or self.trump == "21.XXI - The World"))
    #endDef
#endClass

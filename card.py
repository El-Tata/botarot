#!/usr/bin/env python2
# -*- coding: utf8 -*-

class Card():
    def __init__(self, trump, value, color, points):
        self.trump = trump
        self.value = value
        self.color = color
        self.points = points
    #endDef

    def isTrump(self):
        return (self.trump != None)
    #endDef

    def isOudler(self):
        return (self.isTrump() and (self.trump == "I - The Magician" or self.trump == "0 - The Fool" or self.trump == "XXI - The World"))
    #endDef
#endClass

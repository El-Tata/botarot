#!/usr/bin/env python2
# -*- coding: utf8 -*-

class Card():
    def __init__(self, trump, value, color, point):
        self.trump = trump
        self.value = value
        self.color = color
        self.point = point
    #endDef

    def isTrump(self):
        return (self.trump != None)
    #endDef

    def isOudler(self):
        return (self.isTrump() and (self.trump == '1' or self.trump == 'excuse' or self.trump == '21'))
    #endDef
#endClass

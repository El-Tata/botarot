#!/usr/bin/env python2
# -*- coding: utf8 -*-

import card

class Player():
    def __init__(self, name):
        self.name = name
        self.cards = []
        self.points = 0
    #endDef

    def addCard(self, card):
        self.cards.append(card)
    #endDef

    def playCard(self, card):
        if (not card in self.cards):
            return Card(None, None, None, None)
        else:
            #vérifier légitimité
            return self.cards.pop()#indice de la carte#)
        #endIf
     #endDef

#endClass

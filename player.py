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

    def showCards(self):
        handLst = []
        handStr = "Your cards : "
        for idx, card in enumerate(self.cards):
            if not (idx+1)%10:
                handLst.append(handStr)
                handStr = ""
            #endIf
            handStr += card.strg
        #endFor
        handLst.append(handStr)
        return handLst
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

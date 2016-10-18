#!/usr/bin/env python2
# -*- coding: utf8 -*-

import card

class Player():
    def __init__(self, name):
        self.name = name
        self.cards = []
        self.bid = "passe"
        self.taker = False
        self.points = 0
    #endDef

    def countCardValue(self, val):
        c = 0
        for card in self.cards:
            if card.value == val:
                c += 1
            #endIf
        #endFor
        return c
    #endDef

    def countCardTrump(self):
        c = 0
        for card in self.cards:
            if card.isTrump():
                c += 1
            #endIf
        #endFor
        return c
    #endDef

    def countCardOudler(self):
        c = 0
        for card in self.cards:
            if card.isOudler():
                c += 1
            #endIf
        #endFor
        return c
    #endDef

    def addCard(self, card):
        self.cards.append(card)
    #endDef

    def sortHand(self):
        self.cards.sort()
    #endDef

    def cardsToStr(self):
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

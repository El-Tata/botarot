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
        """
        This method returns the number of cards of the value "val" in the hand of the player.
        """
        c = 0
        for card in self.cards:
            if card.value == val:
                c += 1
            #endIf
        #endFor
        return c
    #endDef

    def countCardTrump(self):
        """
        This method returns the number of trumps in the hand of the player.
        """
        c = 0
        for card in self.cards:
            if card.isTrump():
                c += 1
            #endIf
        #endFor
        return c
    #endDef

    def countCardOudler(self):
        """
        This method returns the number of oudlers in the hand of the player.
        """
        c = 0
        for card in self.cards:
            if card.isOudler():
                c += 1
            #endIf
        #endFor
        return c
    #endDef

    def addCard(self, card):
        """
        This method adds a card in the hand of the player.
        """
        self.cards.append(card)
    #endDef

    def sortHand(self):
        """
        This method sort the cards in the hand of the player.
        """
        self.cards.sort()
    #endDef

    def cardsToStr(self):
        """
        This method returns a list of formated strings of the name of the cards in the hand of the player.
        The list is useful to separate the cars in groups of 10, otherwise the string is too long for one msg on irc.
        """
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
        """
        /!\Not finished/!\
        This method check if the card is playable (define what is "playable" here) by the player and eventually remove it from his hand and return it.
        """
        if (not card in self.cards):
            return None
        else:
            #vérifier légitimité
            return self.cards.pop()#indice de la carte#)
        #endIf
     #endDef

#endClass

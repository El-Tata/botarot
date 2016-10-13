#!/usr/bin/env python2
# -*- coding: utf8 -*-


from card import *
from tarot_deck import *
from player import *
import random


class Game():
    def __init__(self, chan, serv, botRef):
        self.channel = chan
        self.serv = serv
        self.botRef = botRef
        self.players = []
        self.pli = [] #en anglais?
        self.nest = []
        self.deck = TarotDeck(botRef)
        self.deck.generateCards()
    #endDef

    def isRandNestOk(self, randNest):
        for currIdx, val in enumerate(randNest):
            for idx in range(currIdx+1, len(randNest)):
                if (val == randNest[idx] or val+1 == randNest[idx+1]):  #si on trouve des doublons ou qu'on trouve deux valeurs consécutives (randNest est trié)
                    return false
                #endIf
            #endFor

        for idx, val in enumerate(randNest):    #ici on vérifie qu'on a bien toujours des multiples de 3 cartes entre deux cartes choisies pour le chien (randNest est tj trié)
            if idx == 0:
                if (val-1)%3:
                    return false
                #endIf
            else:
                if (val-randNest[idx-1]-1)%3:
                    return false
                #endIf
            #endIf
        #endFor
        return true
    #endDef


    def generateNest(self):
        if (len(self.players) == 3 or len(self.players) == 4):
            randNest = [0, 0, 0, 0, 0, 0]
        elif (len(self.players) == 5):
            randNest = [0, 0, 0]
        else:
            return "Error : " + str(len(self.players)) + " players"
        #endIf
        while (not self.isRandNestOk(randNest)):
            randNest = [random.randint(3, 74) for i in range(len(randNest))]
            randNest.sort()
        #endWhile
        return randNest
    #endDef


    def dealingNoShuffle(self, randNest):
        serv.action(self.channel, "deals...")
        idxPlayer = 0
        countCard = 0
        while (self.deck):
            if countCard in randNest:
                self.nest.append(self.deck.pop(0)); #le chien récupère la première carte courante du paquet
                countCard += 1
            else:
                for i in range(3):
                    self.players[idxPlayer].addCard(self.deck.pop(0))   #le joueur récupère la première carte courante du paquet
                #endFor
                idxPlayer = (idxPlayer + 1) % len(self.players)
                countCard += 3
            #endIf
        #endWhile
    #endDef


    def auction(self):
        from botinstance import bot
        self.botRef.sendMsg(self.chan, "Auction time !")
    #endDef


#    def contracts(self):
#    def annonces(self):

    def start(self, who):
        for card in self.deck.cards:
            if card.trump == None:
                print(str(card.value) + " of " + str(card.color) + ", for " + str(card.points) + " points.")
            else:
                print("Trump : " + str(card.trump))
        self.botRef.sendMsg(self.channel, "Tarot game launched by " + who + ". Waiting for 2-4 more players.")
        self.players.append(who)

    #endDef

#endClass

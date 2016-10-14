#!/usr/bin/env python2
# -*- coding: utf8 -*-


from card import *
from tarot_deck import *
from player import *
import random


class Game():
    def __init__(self, chan, serv, botRef, who):
        self.channel = chan
        self.serv = serv
        self.botRef = botRef
        self.players = [Player(who)]
        self.trick = [] #en anglais?
        self.nest = []
        self.deck = TarotDeck(botRef)
        self.deck.generateCards()
    #endDef

    def isRandNestOk(self, randNest):
        for idx, val in enumerate(randNest[:len(randNest)-2]):
            if (val == randNest[idx+1] or val+1 == randNest[idx+1]):  #si on trouve des doublons ou qu'on trouve deux valeurs consécutives (randNest est trié)
                return False
            #endIf
        #endFor

        for idx, val in enumerate(randNest):    #ici on vérifie qu'on a bien toujours des multiples de 3 cartes entre deux cartes choisies pour le chien (randNest est tj trié)
            if idx == 0:
                if (val)%3:
                    return False
                #endIf
            else:
                if (val-randNest[idx-1]-1)%3:
                    return False
                #endIf
            #endIf
        #endFor
        return True
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
        self.botRef.sendAct(self.channel, "deals...")
        idxPlayer = 0
        countCard = 0
        print(randNest)
        while countCard < 78:
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
        self.botRef.sendMsg(self.chan, "Auction time !")
    #endDef


#    def contracts(self):
#    def annonces(self):

    def gameManager(self):
        strPl = ""
        for pl in self.players:
            strPl += pl.name + " "
        self.botRef.sendMsg(self.channel, "Tarot starts with " + str(len(self.players)) + " players : \x1b[1m" + strPl + "\x1b[0m")
        self.dealingNoShuffle(self.generateNest())
        for pl in self.players:
            for s in pl.showCards():
                self.botRef.sendNtc(pl.name, s)
    #endDef

    def addPlayer(self, nick):
        lstNicks = [pl.name for pl in self.players]
        if nick not in lstNicks:
            self.players.append(Player(nick))
            self.botRef.sendMsg(self.channel, "\x1b[1m" + self.players[-1].name + "\x1b[0m" + " joins this game of tarot !")

            if len(self.players) == 3:
                self.botRef.sendMsg(self.channel, "Already \x1b[1m3 players\x1b[0m. Game will start in 20 seconds...")
                self.botRef.execDelay(20, self.gameManager)
            #endIf
        else:
            self.botRef.sendMsg(self.channel, nick+": tu as déjà rejoint la partie !")
        #endIf
    #endDef

#endClass

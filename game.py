#!/usr/bin/env python2
# -*- coding: utf8 -*-

import card
import random
import player

class Game():
    def __init__(self, chan):
        self.channel = chan
        self.deck = []
        self.players = []
        self.nest = []
    #endDef

    def generateCards(self):
        colors = ["Heart", "Club", "Diamond", "Spade"]
        pips = [["1", 0.5], ["2", 0.5], ["3", 0.5], ["4", 0.5], ["5", 0.5], ["6", 0.5], ["7", 0.5], ["8", 0.5], ["9", 0.5], ["10", 0.5], ["Jack", 2], ["Knight", 3], ["Queen", 4], ["King", 5]]
        for color in colors:
            for pip in pips:
                self.deck.append(Card(trump = None, value = pips[pip[0]], color = colors[color], point = pips[pip[1]]))
            #endFor
        #endFor

        trumps = [  "0 - The Fool",
                    "I - The Magician",
                    "II - The High Priestess",
                    "III - The Empress",
                    "IV - The Emperor",
                    "V - The Hierophant",
                    "VI - The Lovers",
                    "VII - The Chariot",
                    "VIII - Justice",
                    "IX - The Hermit",
                    "X - Wheel of Fortune",
                    "XI - Strength",
                    "XII - Hanged Man",
                    "XIII - Death",
                    "XIV - Temperance",
                    "XV - The Devil",
                    "XVI - The Tower",
                    "XVII - The Star",
                    "XVIII - The Moon",
                    "XIX - The Sun",
                    "XX - Judgement",
                    "XXI - The World"]
        for trump in trumps:
            self.deck.append(Card(trump = trump, value = None, color = None, point = 4.5 if (trump=="0 - The Fool" or trump=="I - The Magician" or trump=="XXI - The World") else 0.5))
        #endFor
    #endDef

    def shuffle(self):
        random.shuffle(self.deck)
        serv.action(self.channel, "shuffle the deck...")
    #endDef


    def generateNest(self):
        if (len(self.players) == 3 or len(self.players) == 4):
            randNest = [0, 0, 0, 0, 0, 0]
        elif (len(self.players) == 5):
            randNest = [0, 0, 0]
        #endIf
        while (not self.isRandNestOk(randNest)):
            randNest = [random.randint(3, 74) for i in range(len(randNest))]
            randNest.sort()
        #endWhile
        return randNest


    def isRandNestOk(self, randNest):
        for currIdx, val in enumerate(randNest):
            for idx in range(currIdx+1, len(randNest)):
                if (val == randNest[idx] or val+1 == randNest[idx+1]):  #si on trouve des doublons ou qu'on trouve deux valeurs consécutives (randNest est trié)
                    return false
                #endIf
            #endFor

        for idx, val in enumerate(randNest):    #ici on vérifie qu'on a bien toujours des multiples de 3 cartes entre deux cartes choisies pour le chien
            if idx == 0:
                if (val-1)%3:
                    return false
                #endIf
            else:
                if (val-randNest[idx-1]-1)%3:
                    return false
                #endIf
            #endIf
        return true


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


#endClass

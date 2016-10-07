#!/usr/bin/env python2
# -*- coding: utf8 -*-

import card
import random
import player

class Game():
    def __init__(self):
        self.cards = []
        self.players = []
        self.nest = []
    #endDef

    def generateCards(self):
        colors = ["Heart", "Club", "Diamond", "Spade"]
        pips = [["1", 0.5], ["2", 0.5], ["3", 0.5], ["4", 0.5], ["5", 0.5], ["6", 0.5], ["7", 0.5], ["8", 0.5], ["9", 0.5], ["10", 0.5], ["Jack", 2], ["Knight", 3], ["Queen", 4], ["King", 5]]
        for color in colors:
            for pip in pips:
                self.cards.append(Card(trump = None, value = pips[pip[0]], color = colors[color], point = pips[pip[1]]))
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
            self.cards.append(Card(trump = trump, value = None, color = None, point = (trump=="0 - The Fool" or trump=="I - The Magician" or trump=="XXI - The World") ? 4.5 : 0.5))
        #endFor
    #endDef

    def shuffle(self):
        random.shuffle(self.cards)
    #endDef

    def distributionNoShuffle(self):
        randNest = [0, 0, 0]
        while ( randNest[0] == randNest[1]-1 or randNest[0] == randNest[1] or randNest[0] == randNest[1]+1
                randNest[0] == randNest[2]-1 or randNest[0] == randNest[2] or randNest[0] == randNest[2]+1
                randNest[1] == randNest[2]-1 or randNest[1] == randNest[2] or randNest[1] == randNest[2]+1):
            randNest = [random.randint(1, 76), random.randint(1, 76), random.randint(1, 76)]
        #endWhile

        idxPlayer = 0
        idxCard = 0
        while (idxCard < 78):
            if idxCard in randNest:
                self.nest.append(card)
            else:
                self.players[idxPlayer].addCard(self.cards[idxCard])



#endClass

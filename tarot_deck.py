#!/usr/bin/env python2
# -*- coding: utf8 -*-

#from botarot import *

from card import *
import random

class TarotDeck():
    def __init__(self, botRef):
        self.botRef = botRef
        self.cards = []


    def shuffle(self):
        random.shuffle(self.cards)
        #endDef


    def generateCards(self):
        colors = ["Heart", "Club", "Diamond", "Spade"]
        pips = [["1", 0.5], ["2", 0.5], ["3", 0.5], ["4", 0.5], ["5", 0.5], ["6", 0.5], ["7", 0.5], ["8", 0.5], ["9", 0.5], ["10", 0.5], ["Jack", 1.5], ["Knight", 2.5], ["Queen", 3.5], ["King", 4.5]]
        for color in colors:
            for pip in pips:
                self.cards.append(Card(trump = None, value = pip[0], color = color, points = pip[1]))
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
            self.cards.append(Card(trump = trump, value = None, color = None, points = 4.5 if (trump=="0 - The Fool" or trump=="I - The Magician" or trump=="XXI - The World") else 0.5))
        #endFor
        self.shuffle()
    #endDef

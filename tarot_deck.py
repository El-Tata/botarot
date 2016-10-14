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

        trumps = [  "0.0 - The Fool",
                    "1.I - The Magician",
                    "2.II - The High Priestess",
                    "3.III - The Empress",
                    "4.IV - The Emperor",
                    "5.V - The Hierophant",
                    "6.VI - The Lovers",
                    "7.VII - The Chariot",
                    "8.VIII - Justice",
                    "9.IX - The Hermit",
                    "10.X - Wheel of Fortune",
                    "11.XI - Strength",
                    "12.XII - Hanged Man",
                    "13.XIII - Death",
                    "14.XIV - Temperance",
                    "15.XV - The Devil",
                    "16.XVI - The Tower",
                    "17.XVII - The Star",
                    "18.XVIII - The Moon",
                    "19.XIX - The Sun",
                    "20.XX - Judgement",
                    "21.XXI - The World"]
        for trump in trumps:
            self.cards.append(Card(trump = trump, value = None, color = None, points = 4.5 if (trump=="0.0 - The Fool" or trump=="1.I - The Magician" or trump=="21.XXI - The World") else 0.5))
        #endFor
        self.shuffle()
    #endDef

    def pop(self, idx=-1):
        return self.cards.pop(idx)

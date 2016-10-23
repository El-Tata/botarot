#!/usr/bin/env python2
# -*- coding: utf8 -*-

#from botarot import *

from card import *
import random

class TarotDeck():
    def __init__(self):
        self.cards = []
        self.strgCards = []

    def shuffle(self):
        """ This method shuffle the cards of the deck. To use only once at the beginning of a game, juste after the cards generation."""
        random.shuffle(self.cards)
        #endDef


    def generateCards(self):
        """ This method generate all the cards in the deck."""
        colors = ["Heart", "Club", "Diamond", "Spade"]
        pips = [["1", 0.5], ["2", 0.5], ["3", 0.5], ["4", 0.5], ["5", 0.5], ["6", 0.5], ["7", 0.5], ["8", 0.5], ["9", 0.5], ["10", 0.5], ["Jack", 1.5], ["Knight", 2.5], ["Queen", 3.5], ["King", 4.5]]
        for color in colors:
            for pip in pips:
                self.cards.append(Card(trump = None, value = pip[0], color = color, points = pip[1]))
                self.strgCards.append(self.cards[-1].strgPoor)
            #endFor
        #endFor

        trumps = [  "EX.0 - The Fool",
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
            self.cards.append(Card(trump = trump, value = None, color = None, points = 4.5 if (trump=="EX.0 - The Fool" or trump=="1.I - The Magician" or trump=="21.XXI - The World") else 0.5))
            self.strgCards.append(self.cards[-1].strgPoor)
        #endFor
        self.shuffle()
    #endDef

    def pop(self, idx=-1):
        """ This method returns the card of index idx of the deck (by default, the last one)."""
        return self.cards.pop(idx)
    #end"Def

    def append(self, card):
        """ This method adds a card to the deck."""
        self.cards.append(card)
    #endDef

    def cut(self):
        """ This method cut the deck in the middle. To use before deal."""
        rdi = random.randint(34, 44)
        for i in range(rdi):
            self.append(self.pop())
        #endFor
    #endDef

#endClass

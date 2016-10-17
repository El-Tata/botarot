#!/usr/bin/env python2
# -*- coding: utf8 -*-


from card import *
from tarot_deck import *
from player import *
import random


class Game():
    def __init__(self, numG, chan, botRef, who):
        self.numG = numG
        self.channel = chan
        self.botRef = botRef
        self.players = [Player(who)]
        self.numTurn = -1
        self.takers = []
        self.callWhat = "King"
        self.trick = []
        self.nest = []
        self.deck = TarotDeck()
        self.deck.generateCards()
        self.bids = ["passe", "petite", "garde", "garde sans", "garde contre"]
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

    def call(self, strCrd):
        if not strCrd in self.deck.strgCards:   #si la chaine ne correspond pas à une carte
            self.botRef.sendMsg(self.channel, self.takers[0].name + ": I do not know this card... ")

        elif (strCrd[0] != self.callWhat[0]) or (strCrd[0] == 'K' and strCrd[1] != self.callWhat[-1]):  #si la carte n'est pas de la bonne hauteur
            self.botRef.sendMsg(self.channel, self.takers[0].name + ": you cannot call this card. You must call a " + self.callWhat + ".")

        elif strCrd in [c.strgPoor for c in self.takers[0].cards]:   #si le joueur a déjà cette carte en main
            self.botRef.sendMsg(self.channel, self.takers[0].name + ": you cannot call this card !")

        else:
            card = None
            for c in self.nest:
                if c.strgPoor == strCrd:
                    card = c
            if card:
                self.botRef.sendNtc(self.takers[0] + "Bad luck, the " + card.value + " of " + card.color + " is in the nest !")
            else:
                for pl in self.players:
                    for c in pl.cards:
                        if c.strgPoor == strCrd:
                            card = c
                            break
                        #endIf
                    if card:
                        pl.taker = True
                        self.takers.append(pl)
                        break
                    #endIf
                #endFor

                self.botRef.sendMsg(self.channel, self.takers[0].name + " calls the " + card.strg + "(" + card.value + " of " + card.color + ").")
                self.botRef.sendNtc(self.takers[1].name, "You are in team with " + self.takers[0].name + ".")

            self.botRef.games[self.numG][1] = "main phase" #contrats ? annonces ?
        #endIf
    #endDef


    def auction(self, nick, bid):
        player = None
        for pl in self.players:
            if pl.name == nick:
                player = pl
            #endIf
        #endFor
        if player == None:
            return
        elif player != self.players[self.numTurn%len(self.players)]:
            self.botRef.sendMsg(self.channel, nick + ": not your turn to bid.")
        elif bid in self.bids:
            if bid == "passe":
                player.bid = bid
                self.botRef.sendMsg(self.channel, nick + " pass.")
            else:
                for pl in self.players:
                    if pl.bid == "":
                        pass
                    if self.bids.index(pl.bid) >= self.bids.index(bid):
                        self.botRef.sendMsg(self.channel, nick + ": this bid is too low, " + pl.name + " said " + pl.bid + ".")
                        self.botRef.sendMsg(self.channel, self.players[self.numTurn].name + ": your turn to speak.")
                        return
                    #endIf
                #endFor
                player.bid = bid
                self.botRef.sendMsg(self.channel, nick + " says " + "\x1b[1m" + bid.title() + "\x1b[0m")
            #endIf
            self.numTurn -= 1
        else:
            self.botRef.sendMsg(self.channel, nick + ": this bid is not valid.")
        #endIf

        if -self.numTurn > len(self.players):    #quand tout le monde est passé, on détermine le preneur
            tkr = 0
            for pl in self.players:
                if self.bids.index(pl.bid) > self.bids.index(self.players[tkr].bid):
                    tkr = self.players.index(pl)
                #endIf
            #endFor
            self.players[tkr].taker = True
            self.takers.append(self.players[tkr])
            self.botRef.sendMsg(self.channel, "\x1b[1m" + self.takers[0].name + "\x1b[0m is the taker.")

            if len(self.players) == 5:  #si on joue à 5, on détermine ce que doit appeler le preneur

                if self.takers[0].countCardValue("King") == 4:
                    self.callWhat = "Queen"
                    if self.takers[0].countCardValue("Queen") == 4:
                        self.callWhat = "Knight"
                        if self.takers[0].countCardValue("Knight") == 4:
                            self.callWhat = "Jack"
                            if self.takers[0].countCardValue("Jack") == 4:
                                callWhat = ""
                            #endIf
                        #endIf
                    #endIf
                #endIf
                if self.callWhat != "":
                    self.botRef.sendMsg(self.channel, self.takers[0].name + ": you shall call a " + self.callWhat + ", with 'call <card>'.")
                    self.botRef.games[self.numG][1] = "call"
                else:
                    self.botRef.games[self.numG][1] = "main phase"
                #endIf
            else:
                self.botRef.games[self.numG][1] = "main phase"
            #endIf
        else:
            self.botRef.sendMsg(self.channel, self.players[self.numTurn].name + ": your turn to speak.")
        #endIf
    #endDef


#    def contracts(self):
#    def annonces(self):

    def showCards(self, player):
        for s in player.cardsToStr():
            self.botRef.sendNtc(player.name, s)

    def gameManager(self):
        strPl = ""
        for pl in self.players:
            strPl += pl.name + " "
        #endFor
        self.botRef.sendMsg(self.channel, "Tarot starts with \x1b[1m" + str(len(self.players)) + " players\x1b[0m : \x1b[1m" + strPl + "\x1b[0m")
        self.dealingNoShuffle(self.generateNest())
        for pl in self.players:
            self.showCards(pl)
        #endFor

        self.botRef.games[self.numG][1] = "auctions"
        self.botRef.sendMsg(self.channel, "\x1b[1mAuction time !\x1b[0m Bid with 'bid passe|petite|garde|garde sans|garde contre'")
        self.botRef.sendMsg(self.channel, self.players[self.numTurn].name + ": your turn to speak.")

    #endDef

    def addPlayer(self, nick):
        if len(self.players) == 5:
            self.botRef.sendMsg(self.channel, nick + ": Already 5 players, you cannot join the game :/ .")
        lstNicks = [pl.name for pl in self.players]
        if nick not in lstNicks:
            self.players.append(Player(nick))
            self.botRef.sendMsg(self.channel, "\x1b[1m" + self.players[-1].name + "\x1b[0m" + " joins this game of tarot !")

            if len(self.players) == 3:
                self.botRef.sendMsg(self.channel, "Already 3 players. Game will start in 20 seconds...")
                self.botRef.execDelay(20, self.gameManager)
            #endIf
        else:
            self.botRef.sendMsg(self.channel, nick+": you already joined the game !")
        #endIf
    #endDef

#endClass

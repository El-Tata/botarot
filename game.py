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
        self.petsec = ""
        self.takers = []
        self.callWhat = "King"
        self.trick = []
        self.nest = []
        self.deck = TarotDeck()
        self.deck.generateCards()
        self.bids = ["passe", "petite", "garde", "garde sans", "garde contre"]
        self.tkrCards = []
        self.defCards = []
    #endDef

    def isRandNestOk(self, randNest):
        """ This method check if the positions of the cards for the nest in the deck are legit."""
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
        """ This method generate a list of position to take the cards for the nest during the deal."""
        if (len(self.players) == 3 or len(self.players) == 4):
            randNest = [0, 0, 0, 0, 0, 0]
        elif (len(self.players) == 5):
            randNest = [0, 0, 0]
        else:   #shouldn't happen
            return "Error : " + str(len(self.players)) + " players"
        #endIf
        while (not self.isRandNestOk(randNest)):
            randNest = [random.randint(3, 74) for i in range(len(randNest))]
            randNest.sort()
        #endWhile
        return randNest
    #endDef


    def dealingNoShuffle(self, randNest):
        """ This method deals the cards beetwen all the players and the nest."""
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

    def dealAgain(self):
        """ This method brings back all the cards of the game in the deck, cuts the deck, and deals."""
        for pl in self.players: #on récupère les cartes de tout le monde
            while pl.cards:
                self.deck.append(pl.cards.pop())
            #endWhile
        #endFor
        while self.nest:
            self.deck.append(self.nest.pop())
        #endWhile
        while self.tkrCards:
            self.deck.append(self.tkrCards.pop())
        #endWhile
        while self.defCards:
            self.deck.append(self.defCards.pop())
        #endWhile
        while self.trick:
            self.deck.append(self.trick.pop())
        #endWhile
        self.deck.cut()
        self.dealingNoShuffle(self.generateNest())  #on redistribue
        for pl in self.players:
            self.showCards(pl)
        #endFor
    #endDef

    def manageNest(self):
        """ This method manages what to do with the nest, according to the taker's bid."""
        if self.takers[0].bid in self.bids[1:3]:    #petite or garde
            while self.nest:
                self.takers[0].addCard(self.nest.pop())
            self.showCards(self.takers[0])
            self.botRef.sendMsg(self.channel, self.takers[0].name + ": I added the nest in your hand. Please choose "  + str(3 if len(self.players) == 5 else 6) + " cards to remove from your hand, by giving their position in this list (from 1 to " + str(len(self.takers[0].cards)) + ").")
            self.botRef.games[self.numG][1] = "nest"
#            self.botRef.sendMsg(self.channel, "Waiting for " + self.takers[0] + " to choose his/her cards amongst the nest.")
            #endIf
        elif self.takers[0].bid == "garde sans":
            while self.nest:
                self.tkrCards.append(self.nest.pop())
            #endWhile
            for pl in self.players:
                pl.sortHand()
            #endFor
            self.botRef.games[self.numG][1] = "announces"
        elif self.takers[0].bid == "garde contre":
            while self.nest:
                self.defCards.append(self.nest.pop())
            #endWhile
            for pl in self.players:
                pl.sortHand
            #endFor
            self.botRef.games[self.numG][1] = "announces"
        #endIf
    #endDef

    def takerPicksNest(self, strIdx):
        """ This method allows the taker to choose which cards he/she want to drop."""
        listIdx = strIdx.split(" ")
        for i in range(len(listIdx)):
            listIdx[i] = int(listIdx[i])
        if len(listIdx) != (3 if len(self.players) == 5 else 6):
            self.botRef.sendMsg(self.channel, self.takers[0].name + ": you must choose " + str(3 if len(self.players) == 5 else 6) + " cards.")
        elif max(listIdx) > len(self.takers[0].cards) or min(listIdx) < 1:
            self.botRef.sendMsg(self.channel, self.takers[0].name + ": the index must be between 1 and " + str(len(self.takers[0].cards)) + ".")
        else:
            listIdx.sort()
            for i in range(len(listIdx)):
                if listIdx[i-1] == listIdx[i]:
                    self.botRef.sendMsg(self.channel, self.takers[0].name + ": you can not remove the same card twice.")
                    return
                #endIf
            #endFor
            for i in range(len(listIdx)-1, -1, -1):
                #listIdx est triée et parcourue à l'envers (de la plus grande à la plus petite valeur), les indices des cartes dans la main du preneur ne se décalent pas
                self.tkrCards.append(self.takers[0].cards.pop(listIdx[i]-1))
            #endFor
            for pl in self.players:
                pl.sortHand()
            #endFor
            self.botRef.games[self.numG][1] = "annouces"
        #endIf
    #endDef

    def call(self, strCrd):
        """ This method manage the call, for a 5-players game. It checks the validity of the call, and inform the player called."""
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
                if self.bids.index(self.takers[0].bid) > 2:
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

#            self.botRef.games[self.numG][1] = "main phase" #annonces ?
            self.manageNest()
        #endIf
    #endDef


    def auction(self, nick, bid):
        """ This method manage the auction phase. Whose turn it is, what the player can (not) say, and eventually, what the taker has to call in the case of a 5-players game."""
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
                self.botRef.sendMsg(self.channel, nick + " passes.")
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
        elif bid == "help":
            self.botRef.sendMsg(self.channel, "You can bid with 'bid petite|garde|garde sans|garde contre'")
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
            if self.players[tkr].bid == "passe":    #tout le monde a passé
                self.botRef.sendMsg(self.channel, "Everybody passed ! I take back your cards and deal again...")
                self.dealAgain()
                self.players.insert(0, self.players.pop(-1))    #on fait tourner la liste des joueurs
                self.numTurn = -1   #et on réinitialise le compteur
                self.botRef.sendMsg(self.channel, self.players[self.numTurn].name + ": your turn to speak.")
                return
            #endIf

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
                    self.manageNest()
#                    self.botRef.games[self.numG][1] = "main phase"
                #endIf
            else:
                self.manageNest()
#                self.botRef.games[self.numG][1] = "main phase"
            #endIf
        else:
            self.botRef.sendMsg(self.channel, self.players[self.numTurn].name + ": your turn to speak.")
        #endIf
    #endDef


#    def annonces(self):

    def showCards(self, player):
        """ This method sends notices to the player with all his/her cards prompted in a fancy way."""
        for s in player.cardsToStr():
            self.botRef.sendNtc(player.name, s)
        #endFor
     #endDef


    def launchAuctions(self):
        """ This method lauch the auction phase, or abort if someone annouced the petit sec."""
        if self.botRef.games[self.numG][1] != "petit sec":
            return
        #endIf
        self.botRef.games[self.numG][1] = "auctions"
        self.botRef.sendMsg(self.channel, "\x1b[1mAuction time !\x1b[0m Bid with 'bid passe|petite|garde|garde sans|garde contre'")
        self.botRef.sendMsg(self.channel, self.players[self.numTurn].name + ": your turn to speak.")
    #endDef


    def checkPetitSec(self):
        """ This method check if there is a petit sec and lauchs the auctions right now or in 5 seconds if there is a petit sec (in order to let the time to the player to annouce it)."""
        petitSec = False
        for pl in self.players: #si un joueur n'a que le petit comme atout, il faut lui laisser l'opportunité de relancer la donne
            if pl.countCardOudler() == 1 and "1" in [ c.strgPoor for c in pl.cards]:
                self.botRef.sendNtc(pl.name, "Your only oudler is the Petit. You have 5 seconds to ask for re-deal with 'petit sec' if you wish.")
                self.petsec = pl.name
                petitSec = True
            #endIf
        #endFor

        self.botRef.games[self.numG][1] = "petit sec"
        if petitSec:
            self.botRef.execDelay(5, self.launchAuctions())
        else:
            self.launchAuctions()
        #endIf
    #endDef

    def petitSec(self, nick):
        """ This method re-lauchs the game if a player annouces the petit sec (and if he it legit)"""
        if nick != self.petsec:
            self.botRef.sendMsg(self.channel, nick + ": lol nope")
            return
        #endIf
        self.botRef.sendMsg(self.channel, "Okay, I deal again.")
        self.dealAgain()
        self.botRef.games[self.numG][1] = "launched"    #c'est l'état précédent
        self.checkPetitSec()
    #endDef


    def start(self):
        """ This is the method to call to launch the game, 20 seconds after the 3rd player joined the game. All the evolution of the game work with a system of state defined in the attribut game from the class Botarot, and updated throughout the methods of the class Game."""
        strPl = ""
        for pl in self.players:
            strPl += pl.name + " "
        #endFor
        self.botRef.sendMsg(self.channel, "Tarot starts with \x1b[1m" + str(len(self.players)) + " players\x1b[0m : \x1b[1m" + strPl + "\x1b[0m")
        self.dealingNoShuffle(self.generateNest())
        for pl in self.players:
            self.showCards(pl)
        #endFor
        self.checkPetitSec()
    #endDef


    def addPlayer(self, nick):
        """ This method allows up to 5 players to join the game. However, as soon as there is 3 players ready, the game will begin in 20 seconds."""
        if len(self.players) == 5:
            self.botRef.sendMsg(self.channel, nick + ": Already 5 players, you cannot join the game :/ .")
        lstNicks = [pl.name for pl in self.players]
        if nick not in lstNicks:
            self.players.append(Player(nick))
            self.botRef.sendMsg(self.channel, "\x1b[1m" + self.players[-1].name + "\x1b[0m" + " joins this game of tarot !")

            if len(self.players) == 3:
                self.botRef.sendMsg(self.channel, "Already 3 players. Game will start in 20 seconds...")
                self.botRef.execDelay(20, self.start)
            #endIf
        else:
            self.botRef.sendMsg(self.channel, nick+": you already joined the game !")
        #endIf
    #endDef


    def takersContract(self):
        """ This method returns the number of points the taker's team has to make in order to validate the contract."""
        if len(self.players == 5):
            return [56, 51, 41, 36][self.takers[0].countCardOudler() + self.takers[1].countCardOudler()]
        else:
            return [56, 51, 41, 36][self.takers[0].countCardOudler()]

#endClass

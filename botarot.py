#!/usr/bin/env python2
# -*- coding: utf8 -*-

import irclib
import ircbot

#import card
import game
import random

class Botarot(ircbot.SingleServerIRCBot):
    def __init__(self):
        ircbot.SingleServerIRCBot.__init__(self, [("irc.iiens.net", 6667)],
                                           "Botarot",
                                           "Bot pour jouer au tarot (indev) réalisé en Python avec ircbot")
        self.chans = ["#test-ircbot"]
        self.savaTab = ["sava", "sava ", "sava ? ", "sava ! ", "sava ?! ", "sava !? ", "sava!!!! ", "sava???? ", "sava. ", "sava... "]
        for i in range(3):
            self.savaTab.append("sava")
            self.savaTab.append("sava ")
        #endFor
        for i in range(2):
            self.savaTab.append("sava")
            self.savaTab.append("sava ? ")
            self.savaTab.append("sava ! ")
            self.savaTab.append("sava. ")
        #endFor

#        self.gameState = None #["launched", "auctions", "call", "main phase"]
        self.games = []   #[[instance of Game(), state of the game], [inst. of G(), st of g.], [...], ...]
        self.whoToSpeak = None
        self.dickLuck = 499
    #endDef

    def get_version(self):
        return "Botarot, the bot for tarot ! - by ElTata"
    #endDef

    def strDick(self, string):
        if self.dickLuck < 0:
            return string
        #endIF
        strL = []
        curSpc = string.find(' ')
        while curSpc >= 0:
            strL.append(string[0 : curSpc+1])
            string = string[curSpc+1:]
            curSpc = string.find(' ')
        #endWhile
        strL.append(string)
        string = ''
        for i in range(len(strL)):
            if not random.randint(0,self.dickLuck):   #1 chance sur dickLuck (500 à la base)
                strL[i] = "bite "
            #endIf
            string += strL[i]
        #endFor
        return string
    #endDef


    def sendMsg(self, dest, msg):
        self.serv.privmsg(dest, self.strDick(msg))
    #endDef

    def sendNtc(self, dest, msg):
        self.serv.notice(dest, msg)
    #endDef

    def sendAct(self, dest, msg):
        self.serv.action(dest, msg)
    #endDef

    def execDelay(self, time, func, args=()):
        self.serv.execute_delayed(time, func, args)
    #endDef


    def on_welcome(self, serv, ev):
        """
        Méthode appelée une fois connecté et identifié.
        """
        self.serv = serv
        for chan in self.chans:
            serv.join(chan)
            self.sendMsg(chan, "Hi everybody ! Guess what ? I have a tarot deck...")
    #endDef

    def gameInChan(self, chan):
        for g in self.games:
            if chan == g[0].channel:
                return g
        return None

    def on_pubmsg(self, serv, ev):
        msg = ev.arguments()[0]
        auth = irclib.nm_to_n(ev.source())
        g = self.gameInChan(ev.target())

        if "bite" in msg.lower() and auth != "Botarot":
            c = msg.lower().count('bite')
            self.dickLuck -= int((c*c)/2)+1
            if self.dickLuck <= 7:
                self.sendMsg(ev.target(), "Félicitations, on est arrivé à 1 bite tous les 7 mots ! Au prochain 'bite', le compteur sera réinitialisé.")
            #endIf
            if self.dickLuck <= 6:
                self.dickLuck = 499

        if msg.startswith("Botarot:"):
            if msg.endswith(":") or msg.endswith(" "):
                self.sendMsg(ev.target(), "J'écoute.")
            #endIf
            if "sava" in msg:
                self.sava(ev.target(), serv)
            elif msg[9:] == "tarot":
                if ev.target() in [g[0].channel for g in self.games]:
                    self.sendMsg(ev.target(), auth+": A game is already running on this chan !")
                else:
                    self.runGame(auth, serv, ev.target())
                #endIf
            elif msg[9:] == "bite?":
                self.sendMsg(ev.target(), "Chacun de mes mots a 1 chance sur " + str(self.dickLuck + 1) + " d'être 'bite'.")
            elif auth == "ElTata":
                if msg[9:] == "casse toi":
                    if ev.target() == self.chans[0]:
                        self.sendMsg(ev.target(), "Non, je reste #ici.")
                    else:
                        if g:
                            self.games.remove(g)
                        #endIf
                        self.chans.remove(ev.target())
                        serv.part(ev.target(), self.strDick("Ok... :'("))
                    #endIf
                elif "go" in msg and "#" in msg:
                    self.chans.append(msg[msg.find('#'):])
                    serv.join(self.chans[-1])
                #endIf
            #endIf
        elif g:
            if msg.lower() == "my cards":
                for pl in g[0].players:
                    if pl.name == auth:
                        g[0].showCards(pl)
#            elif auth == g[0].players[0].name and msg.lower() in ["drop game", "cancel game"]:
#²                self.games.remove(g)
#                self.sendMsg(ev.target(), auth + " stopped the game. I'm available for another one ;).")
            elif g[1] == "launched" and msg.lower() == "join":
                g[0].addPlayer(auth)
            elif g[1] == "auctions" and msg.lower().startswith("bid "):
                g[0].auction(auth, msg.lower()[msg.find(' ')+1:])
            elif g[1] == "call" and auth == g[0].takers[0].name and msg.lower().startswith("call "):
                g[0].call(msg[msg.find(' ')+1:])
            #endIf
        #endIf
    #endDef

    def sava(self, chan, serv):
        savaStr = ""
        rdi = int(1.0/random.expovariate(3))+1  #on simule une loi de poisson de paramètre 3, et +1 pour éviter le 0
        if rdi > 13:
            rdi = 13    #faut pas que ça soit, trop long, ho (et 13 c'est bien, c'est premier)
        for i in range(rdi):
            savaStr += self.savaTab[random.randint(0,len(self.savaTab)-1)]
        #endFor
        self.sendMsg(chan, savaStr)
        return
    #endDef

    def runGame(self, starter, serv, chan):
        self.games.append([game.Game(len(self.games), chan, self, starter), "launched"])
        self.sendMsg(self.games[-1][0].channel, "Tarot game launched by \x1b[1m" + self.games[-1][0].players[0].name + "\x1b[0m. Waiting for 2-4 more players. Say 'join' to participate.")

#        self.g.addPlayer("DECK")
#        for card in self.g.deck.cards:
#            self.g.players[1].addCard(card)
#        self.g.showCards(self.g.players[1])

    #endDef


#endClass

Botarot().start()

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
        self.channel = ["#test-ircbot"]
        self.savaTab = ["sava", "sava ", "sava ? ", "sava ! ", "sava ?! ", "sava !? ", "sava!!!! ", "sava???? ", "sava. ", "sava..."]
        for i in range(3):
            self.savaTab.append("sava")
            self.savaTab.append("sava ")
            #endFor
        for i in range(2):
            self.savaTab.append("sava ? ")
            self.savaTab.append("sava ! ")
            self.savaTab.append("sava. ")
            #endFor
        self.gameLaunched = False
        self.g = None
    #endDef

    def get_version(self):
        return "Botarot, the bot for tarot ! - by ElTata"
    #endDef

    def on_welcome(self, serv, ev):
        """
        Méthode appelée une fois connecté et identifié.
        """
        self.serv = serv
        for chan in self.channel:
            serv.join(chan)
            serv.privmsg(chan, "Hi everybody ! Guess what ? I have a tarot deck...")
    #endDef

    def sendMsg(self, dest, msg):
        self.serv.privmsg(dest, msg)
        return
    #endDef

    def execDelay(self, time, func, args=()):
        irclib.serverConnection.execute_delayed(self, time, func, args)
    #endDef


    def on_pubmsg(self, serv, ev):
        msg = ev.arguments()[0]
        if msg.startswith("Botarot:"):
            if msg.endswith(":") or msg.endswith(" "):
                serv.privmsg(ev.target(), "J'écoute.")
            #endIf
            if "sava" in msg:
                self.sava(ev.target(), serv)
            elif msg[9:] == "tarot":
                self.runGame(irclib.nm_to_n(ev.source()), serv, ev.target())
            elif irclib.nm_to_n(ev.source()) == "ElTata":
                if "casse" in msg and "toi" in msg:
                    self.sendMsg(ev.target(), "Ok... :'(")
                    serv.disconnect()
                #endIf
            #endIf
        elif self.gameLaunched:
            if msg == "join" and len(self.g.players) < 5:
                self.g.addPlayer(irclib.nm_to_n(ev.source()))
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
        self.gameLaunched = True
        self.g = game.Game(chan, serv, self, starter)
        self.sendMsg(self.g.channel, "Tarot game launched by " + self.g.players[0] + ". Waiting for 2-4 more players. Say 'join' to participate.")
    #endDef


#endClass

Botarot().start()

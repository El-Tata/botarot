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
        self.channel = "#test-ircbot"
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
    #endDef

    def get_version(self):
        return "Botarot, the bot for tarot ! - by ElTata"
    #endDef

    def on_welcome(self, serv, ev):
        """
        Méthode appelée une fois connecté et identifié.
        """
        self.serv = serv
        serv.join(self.channel)
        serv.privmsg(self.channel, "Hi everybody ! Guess what ? I have a tarot deck...")
    #endDef



    def on_pubmsg(self, serv, ev):
        msg = ev.arguments()[0]
        if msg.startswith("Botarot:"):
            if msg.endswith(":") or msg.endswith(" "):
                serv.privmsg(self.channel, "J'écoute.")
            #endIf
            if "sava" in msg:
                self.sava(self.channel, serv)
            elif msg[9:] == "tarot":
                self.runGame(irclib.nm_to_n(ev.source()), serv)
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

    def runGame(self, starter, serv):
        g = game.Game(self.channel, serv, self)
        g.start(starter)
    #endDef

    def sendMsg(self, dest, msg):
        self.serv.privmsg(dest, msg)
        return
    #endDef

#endClass

Botarot().start()

#!/usr/bin/env python2
# -*- coding: utf8 -*-

import irclib
import ircbot

#import card
import game

class Botarot(ircbot.SingleServerIRCBot):
    def __init__(self):
        ircbot.SingleServerIRCBot.__init__(self, [("irc.iiens.net", 6667)],
                                           "Botarot",
                                           "Bot pour jouer au tarot (indev) réalisé en Python avec ircbot")
        self.channel = "#test-ircbot"
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
            if msg[9:] == "tarot":
                self.runGame(irclib.nm_to_n(ev.source()), serv)
            #endIf
        #endIf
    #endDef

    def runGame(self, starter, serv):
        g = game.Game(self.channel, serv, self)
        g.start(starter)
    #endDef

    def sendMsg(self, dest, msg):
        self.serv.privmsg(dest, msg)
    #endDef

#endClass

Botarot().start()

#!/usr/bin/env python2
# -*- coding: utf8 -*-

import irclib
import ircbot

import card
import game

class Botarot(ircbot.SingleServerIRCBot):
    def __init__(self):
        ircbot.SingleServerIRCBot.__init__(self, [("irc.iiens.net", 6667)],
                                           "Botarot",
                                           "Bot pour jouer au tarot (indev) réalisé en Python avec ircbot")
    #endDef

    def get_version(self):
        return "Botarot, the bot for tarot ! - by ElTata"
    #endDef

    def on_welcome(self, serv, ev):
        """
        Méthode appelée une fois connecté et identifié.
        """
        serv.join("#test-ircbot")
        serv.action("#test-ircbot", "salue tout le monde.")
    #endDef

#endClass


if __name__ == "__main__":
    Botarot().start()
#endIf

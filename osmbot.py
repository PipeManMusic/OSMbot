#!/usr/bin/env python
##    OSMBot - A IRC BOT for the #opensourcemusicians@freenode.net channel
##    Copyright (C) 2001  Ricardo Lameiro and help of [LSD] and others to come
##
##    This program is free software: you can redistribute it and/or modify
##    it under the terms of the GNU General Public License as published by
##    the Free Software Foundation, either version 3 of the License, or
##    (at your option) any later version.
##
##    This program is distributed in the hope that it will be useful,
##    but WITHOUT ANY WARRANTY; without even the implied warranty of
##    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##    GNU General Public License for more details.
##
##    You should have received a copy of the GNU General Public License
##    along with this program.  If not, see <http://www.gnu.org/licenses/>.
# Code is available at http://github.com/PipeManMusic/OSMbot.git
# More info will be added to the Open Source Musicians Podcast WIKI
#
#

import feedparser
from ircbot import SingleServerIRCBot
from irclib import irc_lower
#import feedparser
import eliza
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
#import question
import re

therapist = eliza.eliza()
#feed = feedparser.parse('http://opensourcemusician.libsyn.com/rss')
#--- IRC SETUP
server = "irc.freenode.net"
port = 6667
channel = '#opensourcemusicians'
nickname = 'OSMBot'

class OsmBot(SingleServerIRCBot):
    def __init__(self, channel, nickname, server, port=6667):
        SingleServerIRCBot.__init__(self, [(server, port)], nickname, nickname)
        self.channel = channel
    def on_nicknameinuse(self, c, e):
        c.nick(c.get_nickname() + "_") 
    def on_pubmsg (self, c, e):
        a = e.arguments()[0].split(":", 1)
        if len(a) > 1 and irc_lower(a[0]) == irc_lower(self.connection.get_nickname()):
            question = irc_lower(a[1].strip())
            if question == "latest episode":
                self.getLatestEpisode(c)
            elif question[:11] == 'get episode':
                self.getEpisode(question, c)
            else:
                self.eliza_parser(question, c)
    def on_welcome(self, c, e):
        c.join(self.channel)

    def eliza_parser(self, question, c):
        c.privmsg(channel, therapist.respond(question))

    def getLatestEpisode(self, c):
        feed = feedparser.parse("http://opensourcemusician.libsyn.com/rss")
        c.privmsg(channel, feed['items'][0]['links'][1]['href'])

    def getEpisode(self, question, c):
        feed = feedparser.parse("http://opensourcemusician.libsyn.com/rss")
        for item in feed['items']:
            search = question[11:]+'(?![0-9])'
            if re.search(search, item['title']):
                c.privmsg(channel, item['title'])
                c.privmsg(channel, item['links'][1]['href'])

bot = OsmBot(channel, nickname, server, port)
bot.start()


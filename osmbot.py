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

import string
from ircbot import SingleServerIRCBot
import time
from midiutil.MidiFile import MIDIFile
from datetime import datetime
import feedparser

feed = feedparser.parse('http://opensourcemusician.libsyn.com/rss')

ntime = time.time()
MidiDict = {}

#--- Midi file setup
osmMidi = MIDIFile(1)

#naming the file with the date and hour
filename = datetime.now().strftime("%Y%m%d%H%M%S") + ".mid"


track = 0
postime = 0
nextbeat = 0

#adding name to the track
osmMidi.addTrackName(track, postime, "OSM BoT MElody")
#tempo for the midi file to play
osmMidi.addTempo(track, postime, 110)

#--- IRC SETUP
server = "irc.freenode.net"
port = 6667
channel = '#opensourcemusicians'
nickname = 'DansBot'

#---Importer from file
t = open('midilist', 'r')
for i in range(97):
    linha = t.readline()
    lido = string.split(linha, " ")
    nota = string.strip(lido[0])
    notamidi = string.strip(lido[1])
    MidiDict[nota] = notamidi
t.close
class OsmBot(SingleServerIRCBot):
    def __init__(self, channel, nickname, server, port=6667):
        SingleServerIRCBot.__init__(self, [(server, port)], nickname, nickname)
        self.channel = channel
    def on_pubmsg (self, c, e):
        input = str(e.arguments()[0])
        if input[:1]== "!":
            note = input[1:]
            self.command_parser(note, c)
        else:
            pass
    def on_welcome(self, c, e):
        c.join(self.channel)

    def command_parser(self, note, c):
        if note.lower() == "help":
            print "help command"
        elif note.lower() == "usage":
            c.privmsg( channel, '''Usage: to start a command use the '!' char and a note representation in the format like "!C#3" or "!bb2" or !f3. The note index range from C0 to C8. The rest is represented by "!r" ''')
        elif note.lower() == "midi":
            print "midi command"
            midiWriteFile()
        elif note.lower() == "about":
            c.privmsg( channel, "The main goal of the bot music game, is to record note entry and rests over time, in a colaborative way, and then export it as a midi file. ")
        elif note.lower() == "license":
            print "license command"
        elif note.lower() == "r":
            c.privmsg(channel, "rest received")
            self.midinewrest(c)
        elif note.lower() == "quit":
            c.privmsg( channel,  "In your dreams, that only for testing.....")
        elif note.lower() == "latest":
            c.privmsg(channel,  feed.entries[0].title)
            c.privmsg(channel, feed.entries[0].link)
        else:
            self.note_parser(note, c)

    def note_parser(self, note, c):
        try:
            mnote = int(MidiDict[note.lower()])
            self.midinewnote(mnote, c)
            c.privmsg(channel, "note received")
        except KeyError:
            c.privmsg( channel,  "Do you really know what you are doing???")
            
    def midinewnote(self, mnote, c):
        #'writes a midi note and the duration. argument is the midi note number'
        global nextbeat
        time1 = noteTime()
        channel = 0
        track1 = 0
        velocity = 120
        osmMidi.addNote(track1, channel, mnote, nextbeat, time1, velocity)
#--- midi writer to file

    def midinewrest(self, c):
        #writes a midi note with Velocity = 0 to make a rest
        global nextbeat
        time1 = noteTime()
        channel = 0
        track1 = 0
        velocity = 0
        mrest = 0
        osmMidi.addNote(track1, channel, mrest, nextbeat, time1, velocity)




def midiWriteFile():
    global filename
    file = open(str(filename), "wb")
    osmMidi.writeFile(file)
    file.close()
    


def noteTime():
    global nextbeat
    Ntime = time.time() - ntime
    Rtime = Ntime / 100
    nextbeat1 = nextbeat
    nextbeat = nextbeat1 + Rtime
    return Rtime


bot = OsmBot(channel, nickname, server, port)
bot.start()


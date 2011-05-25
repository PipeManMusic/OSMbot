import aiml
from ircbot import SingleServerIRCBot
from irclib import irc_lower
from libosmbot import *

kernel = aiml.Kernel()

kernel.learn("brain.xml")

server = "irc.freenode.net"
port = 6667
channel = "#opensourcemusicians"
nickname = "Babybot"

class OsmBot(SingleServerIRCBot):
    def __init__(self, channel, nickname, server, port=6667):
        SingleServerIRCBot.__init__(self, [(server, port)], nickname, nickname)
        self.channel = channel
    def on_nicknameinuse(self, c, e):
        c.nick(c.get_nickname() + "_")
    def on_welcome(self, c, e):
        c.join(self.channel)
    def on_pubmsg(self, c, e):
        a = e.arguments()[0].split(":", 1)

        if len(a)>1 and irc_lower(a[0]) == irc_lower(self.connection.get_nickname()):
            question = irc_lower(a[1].strip())
            responce = kernel.respond(question)
            if responce[0] == "_":
                func = responce[1:]
                
                if func in globals().keys() and callable(globals()[func]):
                    c.privmsg(channel, globals()[ func]())
                else:
                    c.privmsg(channel, "I don't know that command")
            else:
                c.privmsg(channel, responce)
    def testCommand(self):
        return "I am a test command"

bot = OsmBot(channel, nickname, server, port)
bot.start()

import aiml
from libosmbot import *

kernel = aiml.Kernel()

kernel.learn("brain.xml")

while True:
    responce = kernel.respond(raw_input("> "))
    if responce[0] == "_":
        func = responce[1:]
        print "command = " + func
        if func in locals().keys() and callable(locals()[func]):
            locals()[func]()
        else:
            print "function not found"
    else:
         print responce

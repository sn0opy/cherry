#! /usr/bin/env python3
from threading import Thread
import asyncore

from irc import IRCConn
import console
import modules

# Set up modules
mods = modules.Modules()

# Set up connections
freenode = IRCConn("irc.freenode.net", 6667, "henrikbot", "henriks bot", "botbot", mods)
freenode.start()

# array of server connections
conns = [freenode]

# Set up console
console = console.Console(mods, conns)
console_thread = Thread(target=console.cmdloop)
console_thread.start()

# Enter I/O loop
try:
    asyncore.loop()
except KeyboardInterrupt:
    print("CTRL+C pressed.\n")
    asyncore.close_all()

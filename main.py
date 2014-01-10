#! /usr/bin/env python3
from threading import Thread
import asyncore

from irc import IRCConn
import console
import modules
import config

# Set up modules
mods = modules.Modules()

# Set up connections
conns = []
for c in config.connections:
    i = IRCConn(c['server'], c['port'], c['nick'], c['realname'], c['username'], mods)
    if 'nspw' in c:
        i.setnspw(c['nspw'])
    if 'channels' in c:
        i.setautojoin(c['channels'])
    i.start()
    conns.append(i)

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

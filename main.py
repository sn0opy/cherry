#!/usr/bin/env python2.7

# CONFIGURATION
HOST = "chat.freenode.net"
PORT = 6667
NICK = "Klaus"
REALNAME = "Klaus"
USERNAME = "Klaus"

import threading, time
import irc, console, modules
import config as config

conn = irc.IRC(HOST, PORT, NICK, REALNAME, USERNAME)
modules = modules.Modules(conn)
cons = console.Console(conn, modules)

# channels that are to be automatically joined on connection
conn.addchannel("#/dev/urandom")
conn.addchannel("#Klaus")

modules.loadmodules()

print("Starting console thread..")
cons_thread = threading.Thread(target=cons.cmdloop)
cons_thread.start()
print("Starting connection loop..")

conn.start()

while conn.active:
	print("Disconnected! Reconnecting in 5 seconds..")
	time.sleep(5)
	conn.start()

print("Closing up!")

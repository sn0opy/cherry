#! /usr/local/bin/python2.7

# CONFIGURATION
HOST = "irc.freenode.net"
PORT = 6667
NICK = "Cherryklaus"
REALNAME = "Cherry"
USERNAME = "Cherry"

import threading, time
import irc, console, modules

conn = irc.IRC(HOST, PORT, NICK, REALNAME, USERNAME)
modules = modules.Modules(conn)
cons = console.Console(conn, modules)

# channels that are to be automatically joined on connection
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

# a simple "ping" module to serve as an example on how to use the plugin architecture

# this trigger will be looked for by the IRC bot
trigger = ".ping"

# this is the function that will be executed when triggering off

# sendmsg is a function pointer which can be used to send a message to
# a channel or person
def irc_cmd(sender, rcpt, msg, sendmsg):
	sendmsg(rcpt, sender + ": pong")

#! /usr/bin/pyton3

import socket, sys, re, random
import asynchat, asyncore

# TODO: make this modular
import yt

class IRC(asynchat.async_chat):

	def __init__(self, server, port, nick, realname, username):
		asynchat.async_chat.__init__(self)

		self.nick = nick
		self.realname = realname
		self.username = username
		self.server = server
		self.port = port
		self.active = True

		self.channels = []
		self.commands = []

		self.thread = None

		self.buffer = ""
		self.listen = False
		self.set_terminator("\r\n")

	def start(self):
		self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
		asynchat.async_chat.connect( self, (self.server, self.port) )
		try:
			asyncore.loop()
		except KeyboardInterrupt:
			print("CTRL+C pressed..")
			self.quit("CTRL+C")
			sys.exit(1)

	def quit(self, reason=None):
		if reason is not None:
			self.write("QUIT :%s" % reason)
		else:
			self.write("QUIT :bye")
		self.active = False
		self.close_when_done()

	def nick(self, nick):
		self.nick = nick
		write(u"NICK " + nick)

	def write(self, text):
		out = text + u"\r\n"
		self.push(out.encode('utf-8', 'ignore'))

	def privmsg(self, target, message):
		self.write(u"PRIVMSG " + target + u" :" + message)

	def addchannel(self, channel):
		self.channels.append(channel)

	def join(self, channel):
		self.write("JOIN " + channel)

	def part(self, channel):
		self.write("PART " + channel)

	def addcommand(self, command):
		self.commands.append(command)

	def clearcommands(self):
		self.commands = []

	def handle_connect(self):
		self.write("NICK " + self.nick)
		self.write("USER " + self.username + " * " + self.username + " :" + self.realname)

	def collect_incoming_data(self, data):
		self.buffer += data

	def do8ball(self, sender, rcpt, message):
		split = re.split("(\[\s\]\s[^\[\]]+)+?\s?", message)
		choices = [x for x in split if len(x) > 0]
		
		choice = random.randint(0, len(choices)-1)

		out = sender + ":"
		for i in range(len(choices)):
			if choice == i:
				pos = choices[i].find("]")+1
				out += " [x]" + choices[i][pos:]
			else:
				out += " " + choices[i]
		self.privmsg(rcpt, out)


	def found_terminator(self):
		buf = ""
		try:
			buf = self.buffer.decode("utf-8")
		except UnicodeDecodeError:
			buf = self.buffer.decode("iso-8859-1")

		line = buf.split(" ", 3)
		self.buffer = ""

		if line[0] == "PING":
			self.write("PONG " + line[1][1:])
		elif len(line) > 1 and line[1] == "001": # we are connected 
			for c in self.channels:
				self.join(c)
		elif len(line) > 1 and line[1] == "PRIVMSG":
			sender = line[0][1:line[0].find("!")]
			message = line[3][1:]

			# is this a query?
			if line[2] == self.nick:
				recipient = sender
			else:
				recipient = line[2]

			if line[2] == self.nick:
				print("[%s]: %s" % (sender, message))

			if self.listen:
				print("[%s]: <%s> %s" % (recipient, sender, message))

			if re.match("^((?:\[\s\]\s[^\[\]]+\s?)+)", message) is not None:
				self.do8ball(sender, recipient, message)

			if yt.getytid(message) is not None:
				if recipient != "#k" and recipient != "#/dev/null":
					id = yt.getytid(message)
					if id:
						info = yt.getinfo(id)
						if info:
							self.privmsg(recipient, "\x02title:\x02 " + info[0] +  " [rating: " + info[1] + "]")

			for c in self.commands:
				cmdname, cmdfunc = c
				if message.startswith(cmdname):
					cmdfunc(sender, recipient, message, self.privmsg)


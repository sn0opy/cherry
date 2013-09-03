# the Console class makes use of Pythons cmd library to offer interaction with the bot
# during runtime

import cmd, sys

class Console(cmd.Cmd):
	conn = None

	def __init__(self, conn, modules):
		cmd.Cmd.__init__(self)
		self.prompt = "cherry > "
		self.conn = conn
		self.modules = modules

	def precmd(self, line):
		line = line.decode("utf-8")
		return line

	def do_EOF(self, line):
		return True

	def do_load(self, line):
		"""load [modname]"""
		if self.modules.load(line):
			print("success!")

	def do_rehash(self, line):
		"""reloads all modules and registers them"""
		self.modules.reloadmodules()

	def do_die(self, line):
		"""die [reason]"""
		self.conn.quit(line)
		return True

	def do_raw(self, line):
		"""raw <rawcmd>"""
		self.conn.write(line)

	def do_nick(self, line):
		"""nick <nickname>"""
		self.conn.nick(line)

	def do_listen(self, line):
		"""toggles listen mode"""
		self.conn.listen = not self.conn.listen
		print("listen mode is now [%s]" % ("on" if self.conn.listen else "off"))

	def do_join(self, line):
		"""join <channel>"""
		self.conn.join(line)

	def do_part(self, line):
		"""part <channel>"""
		self.conn.part(line)

	def do_say(self, line):
		"""say <target> <message>"""
		args = line.split(u" ", 1)
		if len(args) > 1:
			self.conn.privmsg(args[0], args[1])


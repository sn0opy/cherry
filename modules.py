# provides simple support for reloadable modules

# modules must have a global variable named "trigger" which contains the trigger
# as well as a function called "irc_cmd" which is called by the bot when the trigger
# has been matched

# modules can be also be loaded during runtime on the console

modnames = ['mod_hlk', 'mod_imdb', 'mod_ping', 'mod_tv', 'mod_yt', 'mod_vimeo']

class Modules(object):
	def __init__(self, conn):
		global modnames
		self.mods = {}
		for n in modnames:
			self.mods[n] = None
		self.conn = conn

	def loadmodules(self):
		for n in self.mods.keys():
			mod = __import__(n)
			self.mods[n] = mod
			self.conn.addcommand((mod.trigger, mod.irc_cmd))

	def reloadmodules(self):
		self.conn.clearcommands()
		for k, v in self.mods.iteritems():
			print("reloading " + k + "..")
			reload(v)
			self.conn.addcommand((v.trigger, v.irc_cmd))

	def load(self, name):
		if name in self.mods:
			return False

		try:
			mod = __import__(name)
		except ImportError as e:
			print("Could not load module: " + e.args[0])
			return False

		self.mods[name] = mod
		self.conn.addcommand((mod.trigger, mod.irc_cmd))
		return True

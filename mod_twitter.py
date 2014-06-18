import re, urllib, tweetpony
import html.parser
from modules import BaseModule
import twitter

class TwitterModule(BaseModule):
	def __init__(self):
		self.twre = re.compile(r"(.*)status(?:es)?\/(\d+)")

	def getinfo(self, twid):
		user = "N/A"
		text = ""

		try:
			api = tweetpony.API(twitter.api['consumer_key'], twitter.api['consumer_secret'], twitter.api['access_token_key'], twitter.api['access_token_secret'])
			status = api.get_status(id = twid)

			if status.user.screen_name is not -1:
				user = "@" +status.user.screen_name
			if status.text is not -1:
				text = status.text
				return (user, text)
		except Exception as err:
			return("Error", "Konnte Daten nicht abrufen")

	def getid(self, text):
		global trigger
		retval = None
		result = self.twre.search(text)
		if result:
			try:
				retval = result.group(2)
			except IndexError:
				retval = None
		else:
			retval = None

		return retval

	def onprivmsg(self, conn, sender, to, message):
		id = self.getid(message)
		if id:
			info = self.getinfo(int(id))
			text = info[1].splitlines()
			for line in text:
				if line is text[0]:
					conn.privmsg(to, "\x0312Twitter\x03: "+info[0]+": "+line)
				else:
					conn.privmsg(to, line)

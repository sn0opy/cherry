import re
import requests
from lxml import html
from urllib.parse import urlparse
from modules import BaseModule

class VimeoModule(BaseModule):
	def geturl(self, text):
		retval = None
		u = re.search("(?P<url>https?://[^\s]+)", text)
		if u is not None:
			u = u.group("url")
			try:
				o = urlparse(u)
				if o.scheme is not None:
					exclude = ['www.youtube.com', 'youtube.com', 'vimeo.com', 'twitter.com', 'open.spotify.com']
					if o.netloc in exclude:
						retval = None
					else:
						retval = u
			except IndexError:
				retval = None
		return retval

	def getTitle(self, url):
		r = requests.get(url).text
		return html.fromstring(r).xpath('//title/text()')

	def onprivmsg(self, conn, sender, to, message):
		url = self.geturl(message)
		if url is not None:
			info = self.getTitle(url)
			if info:
				conn.privmsg(to, "Title: " + info[0])

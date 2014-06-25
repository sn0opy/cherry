import re
import requests
from lxml import html
from urllib.parse import urlparse
from modules import BaseModule

class TitleModule(BaseModule):
	exclude_sites = ['www.youtube.com', 'youtube.com', 'vimeo.com', 'twitter.com', 'open.spotify.com', 'play.spotify.com']
	def geturl(self, text):
		retval = None
		u = re.search("(?P<url>https?://[^\s]+)", text)
		if u is not None:
			u = u.group("url")
			try:
				o = urlparse(u)
				if o.scheme is not None:
					if o.netloc in self.exclude_sites:
						retval = None
					else:
						retval = u
			except IndexError:
				retval = None
		return retval

	def getTitle(self, url):
		r = requests.get(url, headers = { 'User-Agent' : 'Cherry IRC Bot' })
		r.encoding = "UTF-8"
		return html.fromstring(r.text).xpath('//title/text()')

	def onprivmsg(self, conn, sender, to, message):
		url = self.geturl(message)
		if url is not None:
			info = self.getTitle(url)
			if info:
				title = info[0][0:100].lstrip().rstrip()
				conn.privmsg(to, "Title: " + title)

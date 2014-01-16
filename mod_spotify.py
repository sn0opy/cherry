import re, urllib
from modules import BaseModule

try:
	import xml.etree.cElementTree as ET
except ImportError:
	import xml.etree.ElementTree as ET

class SpotifyMod(BaseModule):
	def __init__(self):
		self.spotifyre = re.compile(r'(.*)(?!spotify\:|http(?!s))\:\/\/[a-z]+\.spotify\.com\/(track|artist|album)(?:\:|\/)([a-zA-Z0-9]+)')

	def getinfo(self, query, type):
		url = "http://ws.spotify.com/lookup/1/?uri=spotify:" + type + ":" + query
		try:
			fh = urllib.request.urlopen(url)
			root = ET.fromstring(fh.read())
			if len(root) > 0:
				artist = ""
				name = ""
				released = ""
				album = ""		
	
				for child in root:
					if child.tag.find("artist") is not -1:
						for schild in child:
							if artist == "":
								artist = schild.text.rstrip()
					if child.tag.find("name") is not -1:
						name = child.text.rstrip()
					if child.tag.find("released") is not -1:
						released = child.text
					if child.tag.find("album") is not -1:
						for schild in child:
							if schild.tag.find("name") is not -1:
								album = schild.text.rstrip()
	
				return (artist, name, released, album)
		except:
			return None

	def getquery(self, text):
		retval = None
		
		result = self.spotifyre.search(text)
		if result:
			try:
				retval = (result.group(3), result.group(2))
			except IndexError:
				retval = None
		return retval

	def onprivmsg(self, conn, sender, to, message):
	    qry = self.getquery(message)
	    if qry is not None:
	        info = self.getinfo(qry[0], qry[1])
	        if info:
	            albuminfo = " | Album: " + info[3] if qry[1] == "track" else ""
	            releasedinfo = " (" + info[2] + ")" if info[2] != "" else ""
	
	            out = qry[1].title() + ": " + info[1] + releasedinfo + " | Artist: " + info[0] + albuminfo
	
	            conn.privmsg(to, "\x0303Spotify\x03: " + out)



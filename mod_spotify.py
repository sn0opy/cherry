import re
import urllib.request
import json
from modules import BaseModule

class SpotifyMod(BaseModule):
	def __init__(self):
		self.spotifyre = re.compile(r'(.*)(?!spotify\:|http(?!s))\:\/\/[a-z]+\.spotify\.com\/(track|artist|album)(?:\:|\/)([a-zA-Z0-9]+)')

	def getinfo(self, query, type):
		url = "https://api.spotify.com/v1/" + type + "s/" + query
		fh = urllib.request.urlopen(url)
		json_data = json.loads(fh.read().decode("utf-8"))

		artist = ""
		name = ""
		released = ""
		album = ""

		if 'artists' in json_data:
			artist = json_data['artists'][0]['name']

		if 'name' in json_data:
			name = json_data['name']

		if 'album' in json_data:
			album = json_data['album']['name']

		if 'release_date' in json_data:
			released = json_data['release_date']

		return (type, artist, name, album, released)

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
			out = "Keine Info verfügbar"
			if info:
				if info[0] == "track":
					out = "Track: " + info[2] + " | Artist: " + info[1] + " | Album: " + info[3]

				if info[0] == "album":
					out = "Album: " + info[2] + " | Artist: " + info[1] + " | Released : " + info[4]

				if info[0] == "artist":
					out = "Artist: " + info[2]

			conn.privmsg(to, "\x0303Spotify\x03: " + out)

# retrieve metadata from Spotify's API

import re, urllib

try:
	import xml.etree.cElementTree as ET
except ImportError:
	import xml.etree.ElementTree as ET

trigger = "(.*)(?!spotify\:|http(?!s))\:\/\/[a-z]+\.spotify\.com\/(track|artist|album)(?:\:|\/)([a-zA-Z0-9]+)"

def irc_cmd(sender, rcpt, msg, sendmsg):
	qry = getquery(msg)
	if qry:
		info = getinfo(qry[0], qry[1])
		if info:
			albuminfo = " | Album: " + info[3] if qry[1] == "track" else ""
			out = qry[1].title() + ": " + info[1] + " (" + info[2] + ") | Artist: " + info[0] + albuminfo
				
			sendmsg(rcpt, "\x0303Spotify\x03: " + out)


def getinfo(query, type):
	url = "http://ws.spotify.com/lookup/1/?uri=spotify:" + type + ":" + query
	try:
		fh = urllib.urlopen(url)
		root = ET.fromstring(fh.read())
		if len(root) > 0:
			artist = ""
			name = ""
			released = "N/A"
			album = ""		

			for child in root:
				if child.tag.find("artist") is not -1:
					for schild in child:
						artist = schild.text.rstrip()
				if child.tag.find("name") is not -1:
					name = child.text.rstrip()
				if child.tag.find("released") is not -1:
					released = child.text
				if child.tag.find("album") is not -1:
					for schild in child:
						album = schild.text.rstrip()

			return (artist, name, released, album)
	except:
		return None


def getquery(text):
	global trigger
	retval = None
	
	retxt = re.compile(trigger)
	result = retxt.search(text)
	if result:
		try:
			retval = (result.group(3), result.group(2))
		except IndexError:
			retval = None
	else:
		retval = None
	return retval

print getinfo("6Symp1XeJ6NIyrIiGskNmN", "track")

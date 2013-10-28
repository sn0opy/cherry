# resolves youtube URLs to their title and rating by using the YouTube API

import re, urllib

try:
	import xml.etree.cElementTree as ET
except ImportError:
	import xml.etree.ElementTree as ET

trigger = "(.*)youtube\.([A-Za-z]+)\/watch\?v=([A-Za-z0-9-_]+)(&*)(.*)"

def irc_cmd(sender, rcpt, msg, sendmsg):
	id = getytid(msg)
	if id:
		info = getinfo(id)
		if info:
			sendmsg(rcpt, "\x0300You\x0304Tube\x03: " + info[0] +  " | Rating: " + info[1] + " | Uploader: " + info[2] + " | Duration: " + info[3])

def getinfo(id):
	url = "http://gdata.youtube.com/feeds/api/videos/" + id
	try:
		fh = urllib.urlopen(url)
		root = ET.fromstring(fh.read())
		if len(root) > 0:
			title = "N/A"
			rating = "0"
			uploader = "N/A"
			duration = "0s"
			for child in root:
				if child.tag.find("title") is not -1:
					title = child.text
				if child.tag.find("rating") is not -1:
					rating = child.attrib['average']
				if child.tag.find("author") is not -1:
					uploader = child[0].text
				if child.tag.find("group") is not -1:
					for schild in child:
						if schild.tag.find("duration") is not -1:
							duration = convertSec(schild.get("seconds"))
			return (title, rating[:3], uploader, duration)
		return None
	except:
		return None


def getytid(text):
	global trigger
	retval = None
	
	retxt = re.compile(trigger)
	result = retxt.search(text)
	if result:
		try:
			retval = result.group(3)
		except IndexError:
			retval = None
	else:
		retval = None
	return retval


def convertSec(sec):
	m, s = divmod(int(sec), 60)
	h, m  = divmod(m, 60)

	if s > 0:
		out = str(s)+"s"
	else:
		out = "0s"
	if m > 0:
		out = str(m)+"m "+out
	if h > 0:
		out = str(h)+"h "+out

	return str(out)

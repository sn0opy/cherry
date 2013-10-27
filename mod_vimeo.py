# resolves Vimeo URLs to their title and rating by using the Vimeo API

import re, urllib, datetime

try:
	import xml.etree.cElementTree as ET
except ImportError:
	import xml.etree.ElementTree as ET

trigger = "(.*)vimeo\.com\/(\d+)"

def irc_cmd(sender, rcpt, msg, sendmsg):
	id = getid(msg)
	if id:
		info = getinfo(id)
		if info:
			sendmsg(rcpt, "\x0303Vimeo\x03: " + info[0] +  " | Uploader: " + info[1] + " | Likes: " + info[2] + " | Duration: " + info[3])

def getinfo(id):
	url = "http://vimeo.com/api/v2/video/" + id + '.xml'
	try:
		fh = urllib.urlopen(url)
		root = ET.fromstring(fh.read())
		if len(root) > 0:
			title = "N/A"
			rating = "0"
			uploader = "N/A"
			duration = "0s"
			for child in root[0]:
				if child.tag.find("title") is not -1:
					title = child.text
				if child.tag.find("stats_number_of_likes") is not -1:
					rating = child.text
				if child.tag.find("user_name") is not -1:
					uploader = child.text
				if child.tag.find("duration") is not -1:
					duration = convertSec(child.text)
			return (title, uploader, rating, duration)
		return None
	except:
		return None


def getid(text):
	global trigger
	retval = None
	
	retxt = re.compile(trigger)
	result = retxt.search(text)
	if result:
		try:
			retval = result.group(2)
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

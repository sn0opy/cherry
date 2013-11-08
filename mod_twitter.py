# retrieve the Tweet text and a few informations from a given Twitter URL

import re, urllib, tweetpony
from HTMLParser import HTMLParser

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET


trigger = "(.*)status(?:es)?\/(\d+)"

def irc_cmd(sender, rcpt, msg, sendmsg):
	id = getid(msg)
	if id:
		info = getinfo(int(id))
		text = info[1].splitlines()

		for line in text:
			parser = HTMLParser()

			if(line == text[0]):
				sendmsg(rcpt, "\x0312Twitter\x03: "+info[0]+": "+parser.unescape(line))
			else:
				sendmsg(rcpt, parser.unescape(line))


def getinfo(twid):
	user = "N/A"
	text = ""

	config = __import__('config')

	try:
		api = tweetpony.API(config.consumer_key, config.consumer_secret, config.access_token_key, config.access_token_secret)
		status = api.get_status(id = twid)
	
		if status.user.screen_name is not -1:
			user = "@" +status.user.screen_name
		if status.text is not -1:
			text = status.text	

		return (user, text)
	except Exception:	
		return ("Error", "Tweet konnte nicht geladen werden.")		
	

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


# resolves youtube URLs to their title and rating by using the YouTube API

import re, urllib

try:
	import xml.etree.cElementTree as ET
except ImportError:
	import xml.etree.ElementTree as ET


ytre = re.compile(r'(.*)youtube\.([A-Za-z]+)\/watch\?v=([A-Za-z0-9-_]+)(&*)(.*)')

def getinfo(id):
	url = "http://gdata.youtube.com/feeds/api/videos/" + id
	try:
		fh = urllib.urlopen(url)
		root = ET.fromstring(fh.read())
		if len(root) > 0:
			title = "N/A"
			rating = "\u221E"
			for child in root:
				if child.tag.find("title") is not -1:
					title = child.text
				if child.tag.find("rating") is not -1:
					rating = child.attrib['average']
			return (title, rating[:3])
		return None
	except:
		return None


def getytid(text):
	global ytre
	retval = None

	result = ytre.search(text)
	if result:
		try:
			retval = result.group(3)
		except IndexError:
			retval = None
	else:
		retval = None
	return retval

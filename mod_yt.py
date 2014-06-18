import re
import urllib
from modules import BaseModule

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

class YTModule(BaseModule):
	def __init__(self):
		self.ytre = re.compile(r'(.*)youtube\.([A-Za-z]+)\/watch\?v=([A-Za-z0-9-_]+)(&*)(.*)')

	def getytid(self, text):
		retval = None
		s = self.ytre.search(text)
		if s:
			try:
				retval = s.group(3)
			except IndexError:
				retval = None
		return retval

	def convertSec(self, sec):
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

	def getinfo(self, id):
		url = "http://gdata.youtube.com/feeds/api/videos/" + id
		try:
			fh = urllib.request.urlopen(url)
			root = ET.fromstring(fh.read())
			if len(root) > 0:
				title = "N/A"
				rating = "\u221E"
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
								duration = self.convertSec(schild.get("seconds"))

				return (title, rating[:3], uploader, duration)
			return None
		except:
			pass
			return None

	def onprivmsg(self, conn, sender, to, message):
		ytid = self.getytid(message)
		if ytid is not None:
			if to != "#k" and to != "#/dev/null":
				info = self.getinfo(ytid)
				if info:
					conn.privmsg(to, "\x0300You\x0304Tube\x03: " + info[0] +  " | Rating: " + info[1] + " | Uploader: " + info[2] + " | Duration: " + info[3])

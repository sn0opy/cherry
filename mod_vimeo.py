import re
import urllib
from modules import BaseModule

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

class VimeoModule(BaseModule):
	def __init__(self):
		self.vmre = re.compile(r'(.*)vimeo\.com\/(\d+)')

	def getytid(self, text):
		retval = None
		s = self.vmre.search(text)
		if s:
			try:
				retval = s.group(2)
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
		url = "http://vimeo.com/api/v2/video/" + id + '.xml'
		try:
			fh = urllib.request.urlopen(url)
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
						duration = self.convertSec(child.text)
				
				return (title, uploader, rating, duration)
			return None
		except:
			pass
			return None

	def onprivmsg(self, conn, sender, to, message):
		ytid = self.getytid(message)
		if ytid is not None:
			info = self.getinfo(ytid)
			if info:
				conn.privmsg(to, "\x0303Vimeo\x03: " + info[0] +  " | Uploader: " + info[1] + " | Likes: " + info[2] + " | Duration: " + info[3])

# this module looks up the previous and next airdate of a tv show
# it uses TVRage's XML API to do so

import urllib

trigger = "^\.tv"

try:
	    import xml.etree.cElementTree as ET
except ImportError:
	    import xml.etree.ElementTree as ET

def irc_cmd(sender, rcpt, msg, sendmsg):
	global trigger
	arg = msg[len(trigger):].lstrip()

	if len(arg) > 0:
		try:
			fh = urllib.urlopen("http://services.tvrage.com/feeds/episodeinfo.php?exact=1&show=" + arg)
		except IOError:
			sendmsg(rcpt, "Could not connect to TVRage API..")
			return

		try:
			root = ET.fromstring(fh.read())
		except ET.ParseError:
			sendmsg(rcpt, "No results.")
			return

		if len(root) > 0:
			name = root.find("name").text

			out = name;

			if root.find("latestepisode") is not None:
				out += " :: Latest Episode: "
				lep = root.find("latestepisode")
				
				if lep.find("title") is not None:
					out += lep.find("title").text + " "
				if lep.find("number") is not None:
					out += "[" + lep.find("number").text + "] "
				if lep.find("airdate") is not None:
					out += lep.find("airdate").text
			if root.find("nextepisode") is not None:
				out += " :: Next Episode: "
				nep = root.find("nextepisode")

				if nep.find("title") is not None:
					out += nep.find("title").text + " "
				if nep.find("number") is not None:
					out += "[" + nep.find("number").text + "] "
				if nep.find("airdate") is not None:
					out += nep.find("airdate").text

			sendmsg(rcpt, "\x02TV:\x02 " + out)
		else:
			sendmsg(rcpt, "No results.")

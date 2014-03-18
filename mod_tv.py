import urllib.request
import urllib.parse
import modules
from modules import BaseModule

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

class TVModule(BaseModule):
    def lookup(self, title):
        info = {}

        t = urllib.parse.quote(title)

        try:
            fh = urllib.request.urlopen("http://services.tvrage.com/feeds/episodeinfo.php?exact=1&show=" + t)
            root = ET.fromstring(fh.read())
        except ET.ParseError:
            return "No match"
        except urllib.error.HTTPError:
            return "HTTP error"

        info["name"] = root.find("name").text

        if root.find("latestepisode") is not None:
            lep = root.find("latestepisode")
            if lep.find("title") is not None:
                info["title"] = lep.find("title").text
            if lep.find("number") is not None:
                info["number"] = lep.find("number").text
            if lep.find("airdate") is not None:
                info["airdate"] = lep.find("airdate").text
        if root.find("nextepisode") is not None:
            nep = root.find("nextepisode")
            if nep.find("title") is not None:
                info["ntitle"] = nep.find("title").text
            if nep.find("number") is not None:
                info["nnumber"] = nep.find("number").text
            if nep.find("airdate") is not None:
                info["nairdate"] = nep.find("airdate").text
        return info

    def onprivmsg(self, conn, sender, to, message):
        arg = self.extractarg(".tv", message)

        def getval(k, r):
            if k in r: return r[k]
            else: return "N/A"

        res = self.lookup(arg)
        msg = "No results or no connection."
        if type(res) is dict:
            msg = "\x02TV:\x02 "
            msg += res["name"] + " :: Latest Episode:"
            msg += " \"" + getval("title", res) + "\""
            msg += " [" + getval("number", res) + "]"
            msg += " " + getval("airdate", res)

            if 'ntitle' in res:
                msg += " :: Next Episode: \"" + getval("ntitle", res) + "\""
                msg += " [" + getval("nnumber", res) + "]"
                msg += " " + getval("nairdate", res)
        elif type(res) is str:
            msg = res

        if to == conn.nick:
            conn.privmsg(sender, msg)
        else:
            conn.privmsg(to, msg)

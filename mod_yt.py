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

    def getinfo(self, id):
        url = "http://gdata.youtube.com/feeds/api/videos/" + id
        try:
            fh = urllib.request.urlopen(url)
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
            pass
        return None

    def onprivmsg(self, conn, sender, to, message):
        ytid = self.getytid(message)
        if ytid is not None:
            if to != "#k" and to != "#/dev/null":
                info = self.getinfo(ytid)
                if info:
                    conn.privmsg(to, "\x02title:\x02 " + info[0] +  " [rating: " + info[1] + "]")

import urllib.request
import urllib.parse
from modules import BaseModule
import wolfram

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

class WAModule(BaseModule):
    def __init__(self):
        self.url = "https://api.wolframalpha.com/v2/query?appid=" + wolfram.api['appid'] + "&reinterpret=true&format=plaintext&input="

    def lookup(self, term):
        term_quoted = urllib.parse.quote(term)

        try:
            fh = urllib.request.urlopen(self.url + term_quoted)
            root = ET.fromstring(fh.read())
        except ET.ParseError:
            return "Invalid response"
        except urllib.error.HTTPError:
            return "HTTP error"

        if root.attrib['success']:
            pods = 2 if int(root.attrib['numpods']) > 1 else 1
            
            out = ""
            for pod in root[:pods]:
                out += " | "
                if 'title' in pod.attrib:
                    out += pod.attrib['title'] + ": "
                for subpod in pod:
                    if 'title' in subpod.attrib and len(subpod.attrib['title']) > 0:
                        out += subpod.attrib['title'] + ": "
                    for elem in subpod.findall("plaintext"):
                        if elem.text:
                            out += elem.text
        else:
            out = "Query unsuccessful"

        out = out.replace("\n", " :: ")
        return out[:508] + ".." if len(out) > 508 else out

    def onprivmsg(self, conn, sender, to, message):
        if not message.lstrip().startswith(".wa"):
            return
        arg = self.extractarg(".wa", message)
        
        if to == conn.nick:
            rcpt = sender
        else:
            rcpt = to

        if arg is not None and len(arg) > 0:
            response = self.lookup(arg)
            conn.privmsg(rcpt, "\x0304Wolfram\x0307Alpha\x03:" + response)
        else:
            conn.privmsg(rcpt, "usage: .wa <question>")

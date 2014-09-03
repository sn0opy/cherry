from modules import BaseModule
import re
import random

class EightBallModule(BaseModule):
    def do8ball(self, message):
        split = re.split("(\[\s\]\s[^\[\]]+)+?\s?", message)
        choices = [x for x in split if len(x) > 0]
        choice = random.randint(0, len(choices)-1)

        out = ""
        for i in range(len(choices)):
            if choice == i:
                pos = choices[i].find("]")+1
                out += " [x]" + choices[i][pos:]
            else:
                out += " " + choices[i]
        return out

    def onprivmsg(self, conn, sender, to, message):
        if re.match("^((?:\[\s\]\s[^\[\]]+\s?)+)", message) is None:
            return
        result = self.do8ball(message)

        if to == conn.nick:
            rcpt = sender
        else:
            rcpt = to
        conn.privmsg(rcpt, sender + ":" + result)



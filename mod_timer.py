from threading import Timer
from modules import BaseModule

class TimerModule(BaseModule):
    def settimer(self, time, conn, rcpt, msg):
        def timerfunc(conn, rcpt, msg):
            conn.privmsg(rcpt, msg)
        t = Timer(time*60, timerfunc, [conn, rcpt, msg])
        t.start()

    def printusage(self, conn, to):
        conn.privmsg(to, "usage: .timer <minutes> <msg>")

    def onprivmsg(self, conn, sender, to, message):
        arg = self.extractarg(".timer", message)

        # send to channel or user?
        if to == conn.nick:
            rcpt = sender
        else:
            rcpt = to

        if not arg:
            return
        # arguments not empty
        if len(arg) > 0:
            s = arg.split(" ", 1)
            # >= 2 arguments (time, message)
            if len(s) > 1 and len(s[1]) > 0:
                try:
                    time = int(s[0])
                    msg = s[1]
                    self.settimer(time, conn, rcpt, sender + ": " + msg)
                    conn.privmsg(rcpt, sender + ": timer set!")
                except Exception as e:
                    print("error in mod_timer:", e)
                    self.printusage(conn, to)
            else:
                self.printusage(conn, to)

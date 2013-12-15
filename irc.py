import socket
import asynchat

class IRCConn(asynchat.async_chat):

    def __init__(self, server, port, nick, realname, username, mods):
        asynchat.async_chat.__init__(self)

        self.server = server
        self.port = port
        self.nick = nick
        self.realname = realname
        self.username = username
        self.mods = mods
        self.active = True

        self.buffer = []
        self.set_terminator(b"\r\n")

    def start(self):
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        asynchat.async_chat.connect(self, (self.server, self.port))

    def write(self, text):
        out = text + "\r\n"
        self.push(out.encode(errors="ignore"))

    def privmsg(self, rcpt, msg):
        self.write("PRIVMSG " + rcpt + " :" + msg)

    def handle_connect(self):
        self.write("NICK " + self.nick)
        self.write("USER " + self.username + " * " + self.username + " :" + self.realname)

    def join(self, channel):
        self.write("JOIN " + channel)

    def quit(self, msg=None):
        if msg is not None:
            self.write("QUIT :disconnecting")
        else:
            self.write("QUIT :" + msg)
        self.active = False
        self.close_when_done()

    def parse(self, buf):
        line = buf.split(" ", 3)

        if line[0] == "PING":
            self.write("PONG " + line[1][1:])
        #elif len(line) > 1 and line[1] == "001": # we are connected
        elif len(line) > 1 and line[1] == "PRIVMSG":
            sender = line[0][1:line[0].find("!")]
            message = line[3][1:]

            self.mods.onprivmsg(self, sender, line[2], message)

    def collect_incoming_data(self, data):
        self.buffer.append(data)

    def found_terminator(self):
        buf = b"".join(self.buffer).decode("utf-8", "replace")
        self.buffer = []

        self.parse(buf)

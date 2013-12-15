from cmd import Cmd
import sys

class Console(Cmd):

    def __init__(self, modules, conns):
        Cmd.__init__(self)

        self.modules = modules
        self.conns = conns

        self.sid = None
        self.prompt = "cherry () > "
        self.intro = "welcome to cherry. type \"help\" to list commands.\n"

    def do_reload(self, line):
        """reload
        reloads all external modules"""
        self.modules.reload()

    def do_join(self, line):
        """join <channel> [server]
        joins channel on server (if specified).
        if server parameter is not set, the command will fallback to the current default server"""
        args = line.lstrip().split(" ", 1)
        if len(args) > 1:
            try:
                sid = int(args[1])
                if len(self.conns)-1 >= sid:
                    self.conns[sid].join(args[0])
                else:
                    print("server index invalid")
            except ValueError:
                print("invalid server parameter")
        else:
            if self.sid is not None:
                self.conns[self.sid].join(args[0])
            else:
                print("no server index set")

    def do_server(self, line):
        """server <number>
        sets the default server to use when executing commands
        if the argument is empty, it will return the list of servers"""
        args = line.lstrip().split(" ", 1)
        if len(args[0]) > 0:
            try:
                sid = int(args[0])
                if len(self.conns)-1 >= sid:
                    self.sid = sid
                    self.prompt = "cherry (%i) > " % sid
                else:
                    print("invalid server index")
            except ValueError:
                print("invalid input")
        else:
            for i in range(len(self.conns)):
                print("%i:\t%s" % (i, self.conns[i].server))


    def do_exit(self, line):
        """exit <reason>
        closes the irc connections with reason as a quit message (if specified)
        and terminates the bot"""
        for c in self.conns:
            print("closing connection: " + c.server)
            if len(line) > 0:
                c.quit(line)
            else:
                c.quit("bot shutting down")
        return True

import inspect
import imp
import traceback, sys

from irc import IRCConn
from console import Console

MODULES = ["mod_tv", "mod_imdb"]

class Modules():
    # dictionary with modname mapped to (module, obj)
    modules = {} 

    def instantiate(self, m):
        for attr in dir(m):
            attr = getattr(m, attr)
            if(inspect.isclass(attr) and
                    inspect.getmodule(attr) == m and
                    issubclass(attr, BaseModule)):
                return attr()

    def __init__(self):
        global MODULES
        for s in MODULES:
            try:
                m = __import__(s)
                print("Loaded %s .." % s)
            except Exception as e:
                print("Could not load module %s: %s" % (s, str(e)))
                continue
            self.modules[s] = (m, self.instantiate(m))

    def reload(self):
        for key, val in self.modules.items():
            print("Reloading %s .." % (key))
            try:
                reloadedmod = imp.reload(val[0])
                newinstance = self.instantiate(reloadedmod)
                self.modules[key] = (reloadedmod, newinstance)
            except Exception as e:
                print("Could not reload module %s: %s" (key, str(e)))

    def onprivmsg(self, conn, sender, to, message):
        for key, val in self.modules.items():
            try:
                val[1].onprivmsg(conn, sender, to, message)
            except Exception as e:
                excname = type(e).__name__
                tb = traceback.extract_tb(sys.exc_info()[2])[-1]
                print(traceback.extract_tb(sys.exc_info()[2]))
                print("Error running privmsg() handler in %s [line %i]: %s: %s" % (key, tb[1], excname, str(e)))

class BaseModule():
    def onprivmsg(self, conn, sender, to, message):
        pass

    def extractarg(self, trigger, message):
        if message.startswith(trigger):
            _, arg = message.split(trigger, 1)
            return arg.lstrip()
        return None

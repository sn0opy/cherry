import inspect
import imp

from irc import IRCConn
from console import Console

MODULES = ["mod_tv", "mod_imdb", "mod_yt", "mod_weather", "mod_spotify", "mod_vimeo", "mod_twitter"]

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
            self.load(s)

    def load(self, name):
        try:
            m = __import__(name)
            self.modules[name] = (m, self.instantiate(m))
            print("Loaded %s." % name)
        except Exception as e:
            print("Could not load module %s: %s" % (name, str(e)))

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
                print("Error running privmsg() handler in %s: %s: %s" % (key, excname, str(e)))

class BaseModule():
    def onprivmsg(self, conn, sender, to, message):
        pass

    def extractarg(self, trigger, message):
        if message.startswith(trigger):
            _, arg = message.split(trigger, 1)
            return arg.lstrip()
        return None

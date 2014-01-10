import sqlite3
import json
from modules import BaseModule

from urllib.parse import quote
from urllib.request import urlopen

api_key = "c685583bbf624f1f"

class WeatherMod(BaseModule):
    def connect(self):
        self.db = sqlite3.connect("mod_weather.db")
        self.db.cursor().execute("CREATE TABLE IF NOT EXISTS locations (nick text PRIMARY KEY COLLATE NOCASE, location text DEFAULT '')")

    def disconnect(self):
        self.db.close()

    def setlocation(self, nick, location):
        self.connect()
        c = self.db.cursor()
        c.execute("INSERT OR REPLACE INTO locations (nick, location) VALUES (?, ?)", (nick, location))
        self.db.commit()
        self.disconnect()

    def getlocation(self, nick):
        retval = None
        self.connect()
        c = self.db.cursor()
        try:
            c.execute("SELECT location FROM locations WHERE nick = ?", (nick,))
            retval = c.fetchone()[0]
        except:
            pass
        
        self.disconnect()
        return retval

    def load(self, key, features, query, timeout=5):
        FEATURES = ['geolookup', 'conditions', 'forecast', 'astronomy', 'radar', 'satellite', 'webcams', 'history', 'alerts', 'hourly', 'hourly7day', 'forecast7day', 'yesterday', 'autocomplete', 'almanac', 'lang']
        API_URL = 'http://api.wunderground.com/api/{key}/{features}/q/{query}.{format}'

        data = {}
        data['key'] = key
        data['features'] = '/'.join([f for f in features if f in FEATURES])
        data['query'] = quote(query)
        data['format'] = 'json'
        fh = urlopen(API_URL.format(**data), timeout=timeout)
        results = json.loads(fh.read().decode("utf-8"))
        return results

    # this assumes that there is no key with a "." in the name aka it's a nasty hack
    def getkey(self, keypath, d):
        keys = keypath.split(".")

        v = d
        for k in keys:
            if k in v:
                v = v[k]
            else:
                return None
        return v

    def requestdata(self, location):
        global api_key
        try:
            r = self.load(api_key, ['conditions', 'forecast'], location)
        except:
            return "Sorry, could not query the weather API."

        if 'error' in r['response'] or 'results' in r['response']:
            reply = "Please be more specific."
        else:
            name = self.getkey('current_observation.display_location.full', r)
            cur_w = self.getkey('current_observation.weather', r)
            cur_c = self.getkey('current_observation.temp_c', r)
            cur_f = self.getkey('current_observation.temp_f', r)

            reply = "%s :: Currently: %s %iC/%iF" % (name, cur_w, cur_c, cur_f)

            tomorrow = self.getkey('forecast.simpleforecast.forecastday', r)
            if tomorrow and len(tomorrow) > 1:
                fc = tomorrow[1]

                tmr_w = self.getkey('conditions', fc)
                tmr_lc = self.getkey('low.celsius', fc)
                tmr_lf = self.getkey('low.fahrenheit', fc)
                tmr_hc = self.getkey('high.celsius', fc)
                tmr_hf = self.getkey('high.fahrenheit', fc)

                reply += " :: Tomorrow: %s - Low: %sC/%sF - High: %sC/%sF" % (tmr_w, tmr_lc, tmr_lf, tmr_hc, tmr_hf)
        return reply


    def onprivmsg(self, conn, sender, to, message):
        if not message.lstrip().startswith(".weather"):
            return

        result = sender + ": usage: .weather <location> (will be saved after first call and then used for future requests made by you)"

        if to == conn.nick:
            rcpt = sender
        else:
            rcpt = to

        arg = self.extractarg(".weather", message)
        if not arg:
            location = self.getlocation(sender)
            if location is not None:
                result = self.requestdata(location)
        else:
            result = self.requestdata(arg)
            self.setlocation(sender, arg)

        conn.privmsg(rcpt, result)


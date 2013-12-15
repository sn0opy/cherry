import urllib
import json
from modules import BaseModule

class IMDBModule(BaseModule):
    def onprivmsg(self, conn, sender, to, message):
        arg = self.extractarg(".imdb", message)
        if not arg:
            return

        if to == conn.nick:
            rcpt = sender
        else:
            rcpt = to

        if len(arg) > 0:
            try:
                q = urllib.parse.quote(arg)
                fh = urllib.request.urlopen("http://www.omdbapi.com/?i=&t=" + q + "&r=json&plot=short")
            except IOError:
                conn.privmsg(to, "Could not connect to IMDb API.")

            try:
                str_response = fh.read().decode("utf-8")
                result = json.loads(str_response)

                if 'Error' in result:
                    conn.privmsg(rcpt, "Error: " + result['Error'])
                    return

                out = result['Title']

                if 'Year' in result:
                    out += " (" + result['Year'] + ") ::"
                out += " http://imdb.com/title/" + result['imdbID'] + " ::"

                if 'Plot' in result:
                    out += " Plot: " + result['Plot'] + " ::"
                if 'Genre' in result:
                    out += " Genre: " + result['Genre'] + " ::"
                if 'imdbRating' in result:
                    out += " Rating: " + result['imdbRating']
                if 'imdbVotes' in result:
                    out += " (" + result['imdbVotes'] + " votes)"

                conn.privmsg(rcpt, out)
            except ValueError:
                conn.privmsg(rcpt, "Could not parse IMDb output..")

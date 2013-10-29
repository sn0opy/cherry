# looks up movie titles in the IMDb to display information about that movie

import urllib, json

trigger = "^\.imdb"

def irc_cmd(sender, rcpt, msg, sendmsg):
	global trigger

	arg = msg[len(trigger) - 2:].lstrip()

	if len(arg) > 0:
		try:
			fh = urllib.urlopen("http://www.omdbapi.com/?i=&t=" + urllib.quote(arg.encode("utf-8")) + "&r=json&plot=short")
		except IOError:
			sendmsg(rcpt, "Could not connect to IMDb API..")

		try:
			result = json.loads(fh.read())

			if 'Error' in result:
				sendmsg(rcpt, "Error: " + result['Error'])
				return

			out = "\x0308IMDb\x03: "+ result['Title']

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

			sendmsg(rcpt, out)
		except ValueError:
			sendmsg(rcpt, "Could not parse IMDb output..")

# displays server information of half-life1/goldsrc engine based gameservers

import socket, struct

HOST = "foo.bar"
PORT = 27015

trigger = "^\.hl"

def irc_cmd(sender, rcpt, msg, sendmsg):
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.settimeout(2.0)
	
	try:
		s.sendto('\xFF\xFF\xFF\xFFTSource Engine Query\0', (HOST, PORT ))
		ret, addr = s.recvfrom(4096)
	except:
		sendmsg(rcpt, "%s: It seems that the server is currently offline." % sender)
		return

	spl = ret.split("\x00")
	server = spl[0][6:]
	level = spl[1]

	ppos = ret.find(spl[3])+len(spl[3])+3
	try:
		cplayers, maxplayers = struct.unpack("bb", ret[ppos:ppos+2])
	except struct.error:
		cplayers, maxplayers = (-1, -1)
	
	sendmsg(rcpt, "[%s:%i] %s :: %s :: %i/%i" % (addr[0], addr[1], server, level, cplayers, maxplayers))

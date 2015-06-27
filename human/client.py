import socket
import sys
import csv
import os
import time
from traceback import format_exception

 
me = 0
game = sys.argv[1]
human = sys.argv[2]
hostname = sys.argv[3]
if len(sys.argv)==5:
	server = sys.argv[4]

while True:#so it allow user to click before logistics starts
	try:
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		server_address = (hostname, 1234)
		sock.connect(server_address)
		break
	except socket.error, (value,message):#this overide traceback, and not logging into any err file
		if sock:
			sock.close()

		print "-"*50
		print "Connecting to logistics ...\n"
		print "Because: ",message,"\n"
		time.sleep(5)



welcome = sock.recv(1024)
S_msgs={"s1":"Your partner is coming soon, Please wait for a moment ...\n"}

if welcome:
	print "welcome"
else:
	print "server failed to send welcome message."
	sock.close()
	sys.exit()

# sock.send("1 2")#a game and human ID
if len(sys.argv)==5:#crash recovery
	sock.send('%s %s %s' % (game, human, server))
	sock.close()
	sys.exit()

else:

	sock.send('%s %s' % (game, human))
s_p=sock.recv(1024)#get server and port
if s_p:
	print "i'm agent:",human,"and Server and port from logistics: ",s_p
else:
	print "server failed to send s and p."
	sock.close()
	sys.exit()	


s,p=s_p.split()
sock.send(human+" "+p+" "+s)#human port server to get partner or wait
waiting = sock.recv(1024)
if waiting:
	print S_msgs[waiting]
else:
	print "Server failed to send out waiting message."
	sock.close()
	sys.exit()

sock.send("c1")

row=[game,s,p]

with open(os.getenv("HOME")+"/Desktop/logs/clients/"+'c%s.csv' % human,'w') as f:#only subject#,no group 
	logger=csv.writer(f)
	logger.writerow(row)

def wait_go(conn):
	matter=conn.recv(1024)#wait or go
	if matter:
		print "Ok ..."
	else:
		print "Server failed to send partner or s."
		sock.close()
		sys.exit()
		return

	if matter == "go":
		print "You are ready to go!"
	elif matter == "s2":
		print "Waiting for your Server ..."
		conn.send("c2")
		wait_go(conn)
	else:
		print "What? an err: ", matter
wait_go(sock)

# print goMessage

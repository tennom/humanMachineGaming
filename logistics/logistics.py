from itertools import combinations
from random import sample,shuffle,random
from time import ctime
import os
import csv

players=[1,2,3,4]
shuffle(players,random)#No one has an idea who is playing against who
print players

combos=set(list(combinations(players,2)))

posibile=set()
counter=0
matches=[]
for i in combos:
	if i not in posibile:
		busy=set()
		# temp=set()
		temp=[]
		for i in combos:
			if i[0] not in busy and i[1] not in busy:
				posibile.add(i)
				temp.append(i)
				for k in i:
					busy.add(k)
					counter+=1
		combos=combos - posibile
		matches.append(temp)
   		
games=sample(matches,3)
# print games
game_human={}
register={}

def allocateP(game_human):
	P4S1=[]
	P4S2=[]
	for i in range(1,4):#3 games
		for j in range(1,5):#4 agents
			s_p=game_human[str(i)+" %d"%(j)]
			# print "game ",i," human: ",j,":",s_p
			server, port = s_p.split()
			if server == "1":
				if int(port)%2 == 0:
					P4S1.append(port)
			else:
				if int(port)%2 == 0:
					P4S2.append(port)
	# print P4S1,P4S2
	s_ports={1:P4S1,2:P4S2}
	# row=[game,s,p]
	for k in [1,2]:#allocate in server directories 
		with open(os.getenv("HOME")+"/Desktop/logs/servers/%d.csv"%k,'w') as f:
			logger=csv.writer(f)
			logger.writerow(s_ports[k])

def logistics():
	g=1#for game
	p=0#port
	for game in games:
		s=1#server
		for pair in game:
			game_human[str(g)+" "+str(pair[0])]=str(s)+" "+str(p)

			register[str(pair[0])+" "+str(p)]={str(pair[0])+" "+str(p):False}#adding to its own 

			# row2=[str(pair[0])+" "+str(p),str(pair[0])+" "+str(p),False,s,g]
			register[str(pair[1])+" "+str(p+1)]={str(pair[0])+" "+str(p):False}#adding to pair's
			
			p+=1
			game_human[str(g)+" "+str(pair[1])]=str(s)+" "+str(p)

			# row=[str(g)+" "+str(pair[1]),str(s)+" "+str(p)]
			# logger1.writerow(row)

			register[str(pair[0])+" "+str(p-1)][str(pair[1])+" "+str(p)]  = False

			# row2.extend([str(pair[0])+" "+str(p),str(pair[0])+" "+str(p),False,s,g]

			register[str(pair[1])+" "+str(p)][str(pair[1])+" "+str(p)]  = False

			p+=1
			s+=1
		g+=1
	allocateP(game_human)
	return game_human,register
	# print game_human
	# print register['X1 2']


logistics()
print game_human
# print register



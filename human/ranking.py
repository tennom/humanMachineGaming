import os
import csv


# some = [["Z1","3"],["Z5","1.1"],["B2","2"]]

def rank(data):#list of ['id','score']
	ranks = sorted(data, key=lambda (k,v): (float(v)),reverse=True)
	counter=1
	prev_score=10000.0
	rankings=[]
	for i in ranks:
		if abs(float(i[1])-float(prev_score)) < 0.001:
			counter-=1
		score="%.2f"%float(i[1])
		rankings.append("   #"+str(counter)+(13-len(str(counter)))*" "+i[0]+ (11-len(i[0]))*' ' +score+(7-len(score))*" ")
		prev_score=i[1]
		counter+=1

	return rankings

def read_rows(game):

	if not os.access(os.environ["HOME"]+"/Desktop/logs/clients/%s.csv" % game, os.R_OK):
		creat_f=open(os.environ["HOME"]+"/Desktop/logs/clients/%s.csv" % game,'w')#creating one
		writer = csv.writer(creat_f)
		writer.writerow(["ID","Score"])#header
		creat_f.close()
	data=[]
	with open(os.getenv("HOME")+"/Desktop/logs/clients/%s.csv" % game,'r') as f:
		rows=csv.reader(f)
		counter=0
		for row in rows:
			if counter != 0:
				data.append(row)  
			counter+=1  
	return data


def write_row(game,new_data):#new_data is a list of strings
	if not os.access(os.environ["HOME"]+"/Desktop/logs/clients/%s.csv" % game, os.R_OK):
		creat_f=open(os.environ["HOME"]+"/Desktop/logs/clients/%s.csv" % game,'w')#creating one
		writer = csv.writer(creat_f)
		writer.writerow(["ID","Score"])#header
		creat_f.close()
	f=open(os.environ["HOME"]+"/Desktop/logs/clients/%s.csv" % game,'a')
	writer = csv.writer(f)
	writer.writerow(new_data)
	f.close()
# junks=[['G2', '0.968000'], ['T0', '0.872000'], ['T1', '0.738667'], ['G3', '0.666667'], ['G0', '0.568000'], ['megaS++', '0.434666'], ['G4', '0.400000'], ['human', '0.336000'], ['megaS++', '0.336000'], ['G1', '0.301333']]
# for j in rank(junks):
# 	print j

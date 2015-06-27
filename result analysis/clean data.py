import csv
import glob, os
import sys
pairs=[]
def read_in(fn='DataSet.csv'):
	with open(fn,'rU') as f:
		rows = csv.reader(f, delimiter=',')
		names=[('','')]
		existing = {}
		for row in rows: 
			if row[1] == 'Communication':
				if row[3]+row[4] != names[-1][0]+names[-1][1]: ##bad code
					transition = [row[6],row]
				else:
					pass
				if row[3]+row[4] == names[-1][0]+names[-1][1]:
					# print row[3]+row[4]
					# print row
					if transition !=None:
						existing[transition[0]]=transition[1]
					transition=None
					existing[row[6]]=row
					nickname=row[3]

					if row[0] == "Prisoners' Dilemma":
						game='3'
					elif row[0] == "Chicken":
						game="1"
					elif row[0] == "Alternator Game":
						game='2'
					else:
						print "Error: no game is called ", row[0]
						sys.exit()

				else:
					
					if len(names) < 2:
						pass
					else:	
						# if row[0] == "Prisoners' Dilemma":
						# 	game='3'
						# elif row[0] == "Chicken":
						# 	game="1"
						# elif row[0] == "Alternator Game":
						# 	game='2'
						# else:
						# 	print "Error: no game is called ", row[0]
						# 	sys.exit()
						# print names
						# nickname=row[3]
						player1,player2=find_file(nickname,game)
						appender(game,existing,player1,player2)
						existing={}	

					names.append((row[3],row[4]))
					

		# return names[2:-1] ##2 because dump item and file header, -1 to exclude megaSpp

def appender(game,existing,player1,player2):
	global pairs
	if game == "1":
		rounds = 54
	elif game == '2':
		rounds = 47
	elif game == '3':
		rounds = 51
	if player1 == {}:
		pass
	else:
		# iters =0
		for i in range(1,rounds+1): 
			temp=[]
			temp.extend(existing[str(i)])
			temp.extend(player1[str(i)])
			temp.extend(player2[str(i)])
			pairs.append(temp)
		# if iters == 0:
		# 	print existing['1']
		# 	print "------------------------------------------"
		# 	print player1["1"]
		# 	print player2["1"]
		# 	sys.exit()




def find_file(nickname,game):
	dirs = glob.glob('cheaptalk/talk/*')
	nicknames={}

	for i in dirs:
		nicknames[i.split('/')[-1]] = 1

	if nicknames.get(nickname,0) == 1: 
		files = glob.glob('cheaptalk/talk/%s/*' % nickname)
		filename=files[int(game)-1]
	else:
		filename = None
		game = None

	return promotive_talks(filename,game)
	
# find_file('ABL',1)

def promotive_talks(filename,game):
	if filename == None:
		return {},{}

	with open(filename, 'r') as csvfile:
		rows = csv.reader(csvfile)
		rows=list(rows)

		ur_dict = {}
		his_dict = {}
		temp_counter = 0
		data=rows
		for i in data:
			if temp_counter == 0:#excape the headers
				temp_counter += 1
			else:
				bundle1 = i[5].split('$')[0] ##speech acts sent by you
				if len(bundle1) != 0:
					your_talk = bundle1.split(';')
					your_talk = filter(None,your_talk)#filter empty speeches out
				else:
					your_talk = []

				bundle2 = i[7].split('$')[0]
				if len(bundle2) != 0:
					his_talk = bundle2.split(';')
					his_talk = filter(None,his_talk)
				else:
					his_talk = []
				if len(your_talk) != 0:
					ur_values=parse_speech(your_talk,game)
				else:
					ur_values=["0"]*11

				if len(his_talk) != 0:
					his_values=parse_speech(his_talk,game)
				else:
					his_values=["0"]*11

				ur_dict[i[0]]=ur_values
				his_dict[i[0]]=his_values
		return ur_dict,his_dict




def parse_speech(speeches,game):
	# print "this is the game ",game
	check_list={}
	bins=['Fair','Bully','Constrained','Generous','Threat','Responses','Explanations','Praise','Coordinations',"Transition","Curses"]
	if game == '3':
		F= ['15 AC','16 AC', '15 BD','16 BD']
		B=['15 AD', '15 BC','16 BC', '16 AD']
	elif game == '1':
		F=['15 BD', '16 BD', '15 AC', '16 AC']
		B=['15 AD', '15 BC','16 AD', '16 BC']
	elif game == '2': 
		F= ['18 AF CD', '18 CD AF','16 CD','16 AF', '16 CF', '16 FC','15 CF', '15 FC', '16 BE', '16 EB','15 BE', '15 EB']
		B= ['15 AF', '15 CD']
	else:
		print "Error: the three legal game IDs are 1 = Chicken,2 = Blocks and 3 = Prisoner's Dilemma, but yours is ", game 

	for i in speeches:
		if len(i) > 2:
			if i in F:
				check_list['Fair'] = 1
			elif i in B:
				check_list['Bully'] = 1
			elif i[:2] == '17': 
				check_list["Constrained"] = 1
			else:
				check_list["Generous"] = 1
		else:
			if i in ['0','13']:
				check_list['Threat'] = 1
			elif i in ['1','2']:
				check_list['Responses'] = 1
			elif i in ['3','4','12']:
				check_list['Explanations'] = 1
			elif i in ['5','6']:
				check_list['Praise'] = 1
			elif i in ['7','8']:
				check_list['Coordinations'] = 1
			elif i in ['9','10']:
				check_list['Transition'] = 1
			elif i in ['11','14']:
				check_list['Curses'] = 1
			else:
				print 'Error, this is NOT a recognized speech ID: ', i
				print '*'*34	
	
	values=[]
	for i in bins:
		values.append(check_list.get(i,0))

	return values

# files = glob.glob('cheaptalk/talk/%s/*' % "Babay")
# filename=files[2]
# d=promotive_talks(filename,'3')[0]
# print d['1']
read_in()

write_file = open('cheaptalk/clean_data_talk.csv','w')
file_obj = csv.writer(write_file)
file_header=['Game','Communication','Pairing','Name1','Name2','Group','Round','Action1',
			'Action2','Payoff1',"Payoff2","RecipCoop",'Fair','Bully','Constrained',
			'Generous','Threat','Responses','Explanations','Praise','Coordinations',"Transition","Curses",
			'Fair','Bully','Constrained','Generous','Threat','Responses','Explanations','Praise',
			'Coordinations',"Transition","Curses"]
file_obj.writerow(file_header)

for i in pairs:
	file_obj.writerow(i)
write_file.close()

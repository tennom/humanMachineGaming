import csv
import sys
import ast
import matplotlib.pyplot as pyplot

def add_one(nick,one,two,three):
	row=[]
	row.append(nick)
	# row.append(1)
	row.append(one)
	# row.append(2)
	row.append(two)
	# row.append(3)
	row.append(three)

	survey=open("survey.csv",'a')
	logger = csv.writer(survey)
	logger.writerow(row)
	survey.close()


def read_in(nick,game=1):
	with open("survey2.csv",'rU') as f:
		rows = csv.reader(f, delimiter=',')
		new_data={}
		for row in rows:
			# print row
			temp={}
			temp[1]=ast.literal_eval(row[1])
			temp[2]=ast.literal_eval(row[2])
			temp[3]=ast.literal_eval(row[3])

			new_data[row[0]]=temp
		return new_data[nick][game]	
def test(nickname,game):
	'''To catch some human errors in manual data entry'''
	assert len(nickname) > 0
	assert len(game) == 9
	# assert len(game) == 6
	assert(all((type(i)==int and i<6) for i in game[:5]))
	assert(all((type(i)==str) for i in [game[5],game[6]]))
	assert len(game[5])==6
	assert len(game[6])==6

def test_nick(nicks):
	'''testing if all the nick names are found in data entered'''
	counter = 1
	for i in nicks:
		assert read_in(i,2)
		print counter, ': PASS'
		counter +=1
##stupid manual entering survey data since we forgot to collect it electrically
# nickname = "Lav"
# one   = [2,5,4,5,3,'555511','555111','34','']
# two   = [1,5,4,5,3,'555511','555111','348','']
# three = [2,5,5,5,3,'555511','555111','348','']

# for i in [one,two,three]:
# 	test(nickname,i)
# add_one(nickname,one,two,three)
# print nickname,"is done!"
# ###with talk excluding arnuk(human vs robot)
# partner_b = ["Hash50",'LK','Lav','TooToo','biodun','clc','BO1533','NICK','Ninkas','bzman','winner']
# partner_ch = ['ALPHA','Babay','Ben','Lelita','MDM','Qustro','gokill','ligtho','marvin','private','sheen','shunik']
# partner_p = ['EPE','OK','clouds','ABCDE','ABL','NUKK','osenat','p97','spark','monkey','rghost','sachin']
###with talk excluding arnuk(human vs human)
# partner_b = ['ABL','Qustro','Babay','sachin','Ben','p97','Lelita','clouds','ligtho','spark','MDM','ABCDE','monkey',
# 			'ALPHA','NUKK','private','OK','gokill','rghost','marvin','sheen','EPE','shunik','osenat']
# partner_ch = ['ABL','NICK','clc','monkey','Hash50','EPE','Lav','p97','LK','clouds','NUKK','BO1533',
# 				'OK','TooToo','osenat','Ninkas','rghost','bzman','sachin','biodun','winner','spark']
# partner_p = ['Babay','biodun','Ben','Lav','BO1533','private','clc','ALPHA','LK','Lelita','marvin','bzman',
# 				'NICK','Qustro','sheen','Hash50','shunik','Ninkas','TooToo','gokill','winner','ligtho']
###without talk(human vs robot)
partner_b = ['BOZO','L69','Isra','Star','abcdz','django','mike','plush','spike','victor']
partner_ch = ['R2D2','avenger','kai','Dust','XAB','comrad','flyer','t4t','musket','wasbol']
partner_p = ['atom','Hey','MBEAST','asdf','bonus','herb','spider','vojta','mifleh','ruqaia']
###without talk(human vs human)
# partner_b = ['Hey','comrad','mifleh','musket','R2D2','MBEAST','vojta','XAB','atom','wasbol','Dust','bonus','herb',
# 				'flyer','kai','asdf','ruqaia','avenger','t4t','spider']
# partner_ch = ['abcdz','vojta','Hey','mike','mifleh','spike','plush','MBEAST','bonus','django','BOZO','spider','herb',
# 				'Isra','L69','atom','ruqaia','Star','victor','asdf']
# partner_p = ['abcdz','XAB','comrad','mike','R2D2','plush','spike','musket','avenger','Star',
# 				'BOZO','t4t','Dust','django','flyer','Isra','kai','victor','L69','wasbol']
# print len(partner_b)
# test_nick(partner_p) ##testing nicks are found in file
# print read_in('BOZO',1)

survey12={}
def q1q2(nicks,game):
	global survey12
	for nick in nicks:
		q1,q2 = read_in(nick,game)[:2]
		if q1 == 0:
			survey12['missing']=survey12.get('missing',0) + 1
		elif q1 == 1:
			survey12['robot']=survey12.get('robot',0) + 1
		elif q1 == 2:
			survey12['human']=survey12.get('human',0) + 1
		else:
			print 'this is q1', q1
			print 'error in your code'

		survey12[q2] = survey12.get(q2,0) + 1
game_id=1
for j in [partner_ch,partner_b,partner_p]:
	q1q2(j,game_id)
	game_id+=1

# for i in range(1,6):
# 	print 'Percentage of %d: %.2f' % (i,float(survey12[i])/35)
# for j in ['missing','robot','human']:
# 	print 'Percentage of %s: %.2f' % (j,float(survey12[j])/35)
print survey12
fracts = [float(survey12[1])/35,float(survey12[2])/35,float(survey12[3])/35,
			float(survey12[4])/35,float(survey12[5])/35] 
# fracts = [float(survey12['robot'])/30, float(survey12['human'])/30]
# labels = ["robot", "human"]
labels = ['dumb human', 'less than avg. human', 'avg. human','above avg. human','very smart human']
colors =['brown','grey','cyan','magenta','green']
# colors =['magenta','green']
explode=(0, 0, 0, 0, 0.05)
pyplot.axis("equal")
pyplot.pie(fracts, explode=explode, labels=labels, colors=colors, autopct="%1.1f%%", shadow=True)
# pyplot.legend(labels, loc=(-0.05, 0.05), shadow=True)
pyplot.title("Rankings on intelligence of Mega S++ (w/ talk)")
pyplot.show()


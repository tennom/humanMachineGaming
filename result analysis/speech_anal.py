import csv
import glob, os
import sys
from collections import Counter

import matplotlib.pyplot as plt
import numpy as np

rocks = []
add_max_comply = {}
add_max_comply1 = {}
def counting(d,element):
	d[element]=d.get(element,0)+1

def filter_plans(l,plan):
	if plan in l:
		return True
	else:
		return False
def compliance(chat,row):
	plan=chat.split()
	# print len(plan) > 1 and (row[9]+row[14] in plan or row[14]+row[9] in plan)
	return len(plan) > 1 and (row[9]+row[14] in plan or row[14]+row[9] in plan)

def promotive_talks(filename,game):
	if game == "chicken":
		col_sol = 84
	elif game == 'blocks':
		col_sol = 70
	elif game == 'prisoners':
		col_sol = 60
	else:
		print "you typed the wrong game name."
		sys.exit()
	speeches = []
	with open(filename, 'r') as csvfile:
		rows = csv.reader(csvfile)
		rows=list(rows)

		# counter = 0
		# for i in rows:

		# 	if counter == 0:
		# 		counter+=1
		# 	else:
		# 		if (int(i[11]) + int(rows[counter+1][11])) /2 == col_sol:
		# 			if (int(i[16]) + int(rows[counter+1][16])) /2 == col_sol:
		# 				counter += 5
		# 				break
		# 		else:
		# 			counter += 1
		# if counter < 9:
		# 	data = rows[1:counter]
		# 	print 'found in less than 10'
		# else:
		# 	data = rows[counter-8:counter+1]
		# 	print 'from ',counter-8,'to',counter+1
		# 	print 'after 10 rounds','#'*12
		ur_dict = {}
		his_dict = {}
		temp_counter = 0
		data=rows
		for i in data:
			if temp_counter == 0:#excape the headers
				temp_counter += 1
			else:
				bundle1 = i[5].split('$')[0]
				if len(bundle1) != 0:
					your_talk = bundle1.split(';')
					# print your_talk
					your_talk = filter(None,your_talk)#filter empty speeches out
				else:
					your_talk = []
				bundle2 = i[7].split('$')[0]
				if len(bundle2) != 0:
					his_talk = bundle2.split(';')
					# print his_talk
					his_talk = filter(None,his_talk)
				else:
					his_talk = []

				if len(your_talk) != 0:#count the comformants 
					map(lambda x: counting(ur_dict,x), [y for y in your_talk if compliance(y,i)])
				if len(his_talk) != 0:
					map(lambda x: counting(his_dict,x), [y for y in his_talk if compliance(y,i)])

				speeches.extend(your_talk)
				speeches.extend(his_talk)

		global add_max_comply, add_max_comply1 #
		keys = []
		keys.extend(ur_dict.keys())
		keys.extend(his_dict.keys())
		keys=list(set(keys))
		print keys
		for key in keys:
			# if key == '18 AF CD':
			# 	add_max_comply1['18 AF CD'] = add_max_comply1.get('18 AF CD',0) + ur_dict.get("18 CD AF",0)+his_dict.get("18 CD AF",0)
			# # elif key == '18 CD AF':
			# # 	pass
			# else:	
			add_max_comply[key] = add_max_comply.get(key,0) +max([ur_dict.get(key,0),his_dict.get(key,0)])
			add_max_comply1[key] = add_max_comply1.get(key,0) + ur_dict.get(key,0)+his_dict.get(key,0)#max([ur_dict.get(key,0),his_dict.get(key,0)])

	global rocks
	# print len(speeches)
	rocks.extend(speeches)


check = 'prisoners'


files = glob.glob('speechStuff/top10/%s/*.csv' % check)
for i in files:
	promotive_talks(i, check)

print len(files)
# print rocks[:15]
# print add_max_comply
# print "#"*15
# print add_max_comply1
counts = Counter(rocks)

sorted_counts=sorted(counts.items(),key=lambda x: x[1])
# # print sorted_counts
print sorted_counts[-10:]
comformants=[]  #[0]*(len(sorted_counts))
others=[]  #[0]*(len(sorted_counts))
names=[]

indx=0
for i in sorted_counts:
	if i[1] > 1:
		if i[0] == '18 AF CD':
			keep = indx
		elif i[0] == '18 CD AF':
			discard = indx
		names.append(i[0])
		comformants.append(add_max_comply1.get(i[0],0))
		others.append(i[1]-add_max_comply1.get(i[0],0))
		indx+=1
	# comformants[indx]=add_max_comply1.get(i[0],0)
	# others[indx] = i[1]-add_max_comply1.get(i[0],0)

## combine '18 AF CD' and '18 CD AF'
# del names[discard]
# comformants[keep] += comformants[discard]
# del comformants[discard]
# others[keep] += others[discard]
# del others[discard]	

def autolabel(bars,c='black',more=0):
	for bar in bars:
		height = bar.get_height()
		if height > 35:
			plt.text(bar.get_x()+bar.get_width()/2., 30, '%d'%int(height),ha='center',va='bottom',color=c)
		elif height > 7: 
			plt.text(bar.get_x()+bar.get_width()/2., height*0.6, '%d'%int(height),ha='center',va='bottom',color=c)
		# elif height == 5:
		# 	plt.text(bar.get_x()+bar.get_width()/2., 23, '%d'%int(height),ha='center',va='bottom',color=c)
		elif height >3:
			plt.text(bar.get_x()+bar.get_width()/2., height+more, '%d'%int(height),ha='center',va='bottom',color=c)
# print values
width=0.5
p1 = plt.bar( np.arange(0,len(names)), comformants, width, color='#9932cc')
p2 = plt.bar( np.arange(0,len(names)), others, width, color='#d2691e', bottom=comformants)
plt.legend( (p1[0],p2[0]),('compliance','other'),loc=2 )
plt.ylabel("counts of speech and action compliance")
plt.xlabel("speeches (IDs)")
plt.xticks(np.arange(0,len(names)),names,rotation=45, rotation_mode="anchor", ha="right")
plt.yticks(np.arange(0,40,5))
plt.title("Top 7 pairs (%s)" % check)
autolabel(p2,'black',-2)
autolabel(p1,'black', -2)
plt.show()
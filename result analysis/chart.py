import csv
import glob, os

check='chicken'
verses="hh"
is_talk = 'withTalk'

data = {}
rounds=None
def open_file(file_name,sig=False):
	with open(file_name, 'r') as csvfile:
		rows = csv.reader(csvfile, delimiter='\t')
		# rows = csv.reader(csvfile, delimiter=',')
		counter=1
		for row in rows:
			data.setdefault(counter,[0,0])
			if sig:
				data[counter][0]+=float(row[3])
				data[counter][1]+=float(row[2])	
			else:			
				data[counter][0]+=float(row[2])
				data[counter][1]+=float(row[3])
			# data[counter][0]+=float(row[0])
			# data[counter][1]+=float(row[1])
			# print row
			counter+=1
		# print counter
		global rounds
		if rounds != None:#check point for missing data
			if rounds == counter:
				pass
			else:
				print "data missing in one file."
		else:
			rounds=counter


# print data[1]
files = glob.glob('actions/%s/%s/%s/*.txt' % (is_talk,check,verses))
# files = glob.glob('anal/hr/%s/*.csv'%check)

print len(files)
# print files



for f in files:
	open_file(f)
	# if "_megaS++_activity_0" in f:
	# 	open_file(f)
	# else:
	# 	open_file(f,True)


for j in xrange(1,rounds):#average over number of subjects.

	data[j][0]=data[j][0]/len(files)
	data[j][1]=data[j][1]/len(files)

plot_data = open('anal/%s/%s/%s%s2.csv' % (is_talk,check,verses,check), 'w')#two columns
logger = csv.writer(plot_data)

for i in xrange(1,rounds):
	logger.writerow(data[i])
plot_data.close()

def plot_ready(filename):
	with open(filename, 'r') as csvfile:
		rows = csv.reader(csvfile)
		ready=open('anal/%s/%s%s_plot.csv' % (is_talk,verses,check),'w')
		logger = csv.writer(ready)
		for row in rows:
			logger.writerow([(float(row[0])+float(row[1]))/2])
		ready.close()

# plot_ready('anal/%s/%s/%s%s2.csv' % (is_talk,check,verses,check))




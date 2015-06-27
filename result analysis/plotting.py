import csv
import matplotlib.pyplot as plt
import sys
from numpy import repeat,convolve


check="chicken"
verses='rr'
is_talk="withTalk"
window = 5

if check == "chicken":
	rounds = 55
elif check == "blocks":
	rounds = 50
elif check == "prisoners":
	rounds = 52
else:
	print check,"is wrong name, reenter."
	sys.exit()

def movingAverage(values,window):#for smothing out the plot
	weights = repeat(1.0, window)/window
	movingAVG = convolve(values,weights, 'valid')
	return movingAVG

#real plotting
x1=[]
y1=[]
with open('actions/%s/%s%s_plot.csv' % (is_talk,verses,check),'r') as f:
# with open('anal/withTalk/robot_plot.csv','r') as f:
	rows = csv.reader(f)
	counter=1
	for row in rows:
		x1.append(counter)
		y1.append(float(row[0]))
		counter+=1

is_talk="withoutTalk"
# verses='hr'
x2=[]
y2=[]
with open('actions/%s/%s%s_plot.csv' % (is_talk,verses,check),'r') as f:
	rows = csv.reader(f)
	counter=1
	for row in rows:
		x2.append(counter)
		y2.append(float(row[0]))
		counter+=1

# x1=[]
# x2=[]
# y1=[]
# y2=[]
# with open('actions/%s/%s%s_plot.csv' % (is_talk,verses,check),'r') as f:
# 	rows = csv.reader(f)
# 	counter=1
# 	for row in rows:
# 		x1.append(counter)
# 		x2.append(counter)
# 		y1.append(float(row[0]))
# 		y2.append(float(row[1]))
# 		counter+=1

# is_talk="withoutTalk"
# x3=[]
# x4=[]
# y3=[]
# y4=[]
# with open('actions/%s/%s%s_plot.csv' % (is_talk,verses,check),'r') as f:
# 	rows = csv.reader(f)
# 	counter=1
# 	for row in rows:
# 		x3.append(counter)
# 		x4.append(counter)
# 		y3.append(float(row[0]))
# 		y4.append(float(row[1]))
# 		counter+=1

y1_MA = movingAverage(y1,window)
y2_MA = movingAverage(y2,window)
# y3_MA = movingAverage(y3,7)
# y4_MA = movingAverage(y4,7)


plt.xlabel('Rounds')
plt.ylabel('Average Scores')
# plt.title('With talk vs without(Mega S++ vs Human in %s)'%check)
plt.title('Mega S++ selfplay in %s'%check)
# plt.plot(x1,y1,'b--',label='Human')
# plt.plot(x2,y2,'r--',label='MegaS++')
plt.plot(x1[len(x1)-len(y1_MA):],y1_MA,'b-',label='w/ talk')
plt.plot(x2[len(x2)-len(y2_MA):],y2_MA,'r-',label='w/o talk')
# plt.plot(x3[len(x3)-len(y3_MA):],y3_MA,linestyle='-',color='#20E0E5',label='w/o talk human', marker="o",markevery=6)
# plt.plot(x4[len(x4)-len(y4_MA):],y4_MA,linestyle='-',color='#ee4ed7',label='w/o talk MegaS++', marker="o",markevery=6)

plt.legend(loc='upper left')
plt.axis([1,rounds,0.0,1.0])
plt.grid(True)
plt.show()
from Tkinter import *
# from ttk import Style as sty,Button as bt,Notebook as nb

import tkMessageBox
import sys
import socket
from math import ceil

import tkFont
import random
from time import sleep,ctime
from threading import Thread#gameover count down


import os
import csv
import datetime
from subprocess import call
import re#regular expressions

import ranking

feelings = ["Do as I say, or I'll punish you.", \
            "I accept your last proposal.", "I don't accept your proposal.", \
            "That's not fair.", "I don't trust you.",\
            "Excellent!", "Sweet. We are getting rich.", \
            "Give me another chance.", "I forgive you.", "I'm changing my strategy.", \
            "We can both do better than this.", \
            "Curse you.","You betrayed me.", "You will pay for this!", "In your face!" \
            ]
# fix_relationship = ["I am sorry", "Give me another chance.", "I've had a change of heart.","I'm willing to put the past behind us.", "I will let you off this time."]
propose=["Let's alternate between "]
feel=["Let's always play "]
feel2=["This round, let's play "]
feel3=["Don't play "]

##Options =["I trusted you to take "+i for i in [color+" "+shape for color in ["Blue", "Yellow","Red"] for shape in ["Triangle", "Square", "Circle"]]]
##Actions=["A","B"]
def make_ids(groups):
   '''hash IDs to speeches and speeches to IDs, so used for throughout the code'''
   inc=0
   msg2id={}
   id2msg={}
   
   for group in groups:
      for i in group:
##         print i,inc
         msg2id[i]=inc
         id2msg[inc]=i
         inc+=1
   return msg2id,id2msg

# directory,id2msg=make_ids([plans,feelings,fix_relationship,propose,feel])#precompute IDs and speeches
directory,id2msg=make_ids([feelings,feel,feel2,feel3,propose])
##print directory
##opt2id,id2opt=make_ids([Options])#same thing for drop menus
class Progress:
   def __init__(self, parent):

      top = self.top = Toplevel()
      self.top.overrideredirect(1)
      print "Waiting for parter's message ..."

##      Label(top, text="Waiting for your opponent's response...").grid()      
      
class Talk_orders(Frame):
   """ drag'n'drop reordering of speeches, button, motion,key binding """
   def __init__(self, master, r=0,c=0,chk_butts=[],drop_menu=[],talk_buttons=None,**kw):

   
      Frame.__init__(self, master)
      
      self.tb=talk_buttons
      
      mygray = "#%02x%02x%02x" % (100, 100, 100)#styling
      fontH17 = tkFont.Font(family="Helvetica", size=17)
      fontH12 = tkFont.Font(family="Helvetica", size=12)
      
      Label(master,text="Selected Message",font=fontH17,fg=mygray).place(x=790,y=355)
      Label(master,text="Drag to change the order",font=fontH12,fg=mygray).place(x=798,y=380)
      self.chk_butts=chk_butts
      self.drop_menu=drop_menu
      
      scrolly = Scrollbar(master, orient=VERTICAL)
      # scrollx = Scrollbar(master, orient=HORIZONTAL)
      self.dd = Listbox(master, height=14,width=40,yscrollcommand=scrolly.set,selectmode = SINGLE)
      

      horz,vert=700,400
      self.dd.place(x=horz,y=vert)

      scrolly.place(x=horz+self.dd.winfo_reqwidth(),y=vert,height=self.dd.winfo_reqheight())

      scrolly['command'] = self.dd.yview

      self.dd.bind('<Button-1>', self.setCurrent)
      self.dd.bind('<B1-Motion>', self.shiftSelection)
      self.dd.bind('<Delete>',self.deleteCurrent)
      self.update()

      self.curIndex = None
   def setCurrent(self, event):
      self.curIndex = self.dd.nearest(event.y)
        
   def deleteCurrent(self,event):
      selected=self.dd.get(self.curIndex)
      which=directory.get(selected,"NA")
      if selected == "":
         print "No item is selected. Click on the item first and then press delete."
      elif which !="NA":
         self.chk_butts[which].set(0)
         self.dd.delete(self.curIndex)

         if len(self.dd.get(0,END))==0:
            self.tb.submit.configure(text="send no message")
      else:
         found=False
         counter=0
         for i in propose:#this has to be improved when changing is finished
            reset=selected.replace(i,"")
            if len(selected) != len(reset):
               groupID=3#group ID of propose
               indx=counter
               found=True
               break
            counter+=1
         if not found:
            counter=0
            for j in feel:
               reset=selected.replace(j,"")
               if len(selected) != len(reset):
                  groupID=4
                  indx=counter
                  found=True
                  break
               counter+=1
         if not found:
            counter =0
            for k in feel2:
               reset=selected.replace(k,"")
               if len(selected) != len(reset):
                  groupID=5
                  indx=counter
                  break
               counter+=1     

         if not found:
            counter =0
            for l in feel3:
               reset=selected.replace(l,"")
               if len(selected) != len(reset):
                  groupID=6
                  indx=counter
                  break
               counter+=1 
         if groupID == 3:#bad code
            drop_menu=self.drop_menu[1]#now the two drops extended after group 3 thus so
         elif groupID == 4:
            drop_menu=self.drop_menu[0]
         elif groupID == 5:
            drop_menu=self.drop_menu[2]
         elif groupID == 6:
            drop_menu=self.drop_menu[3]
         else:
            print "Error: item in unspecified group"
            
            
         map(lambda child: child.set("..."), drop_menu.vars2[(groupID,indx)])
##         map((lambda child: child.configure(state="disabled")), drop_menu.chk_action[(groupID,indx)])
         
         drop_menu.vars[(groupID,indx)].set(0)#reseting the menu label to 0
         self.dd.delete(self.curIndex)
         if len(self.dd.get(0,END))==0:
            self.tb.submit.configure(text="send no message")         
         
        
   def shiftSelection(self, event):
      i = self.dd.nearest(event.y)
      if i < self.curIndex:
         x = self.dd.get(i)
         self.dd.delete(i)
         self.dd.insert(i+1, x)
         self.curIndex = i
      elif i > self.curIndex:
         x = self.dd.get(i)
         self.dd.delete(i)
         self.dd.insert(i-1, x)
         self.curIndex = i
         
def read_reorders(talk_order):
   '''both checkbuttons and dropmenus read the redoring window'''
   d={}
   idx=0
   for i in talk_order.get(0,END):
      d[i]=[1,idx]
      idx+=1
   return d

class DropMenu(Frame):
   """inputs: master frame,options,locations(row,column,spans),"""
   def __init__(self, parent=None,opts=[],loc=[],talk_order=None,talk_buttons=None,two_drops=[False]):
      Frame.__init__(self,parent)
      self.tb=talk_buttons
      
      self.talk_order=talk_order
      self.vars={}
      self.reseting=[]
      self.labels=[]
      row_inc=loc[0]
      label_indx=1
      self.clicked=-1
      self.groupID=loc[3]
      self.chk_action={}
      self.opt_action={}
      self.vars2={}
      chk_id=0
      
      
      for option in opts:
         col_inc=loc[1]

         varInt=IntVar()
         chk = Checkbutton(self, text=option[1], variable=varInt,command=lambda:self.worker(talk_order))
         chk.grid(row=row_inc, column=col_inc,sticky=W)
         chk.bind('<Button-1>', lambda event, indx=chk_id, groupID=loc[3]: self.on_check(indx,groupID))
         self.vars[(self.groupID,chk_id)]=varInt
         self.labels.append(varInt)
         
         col_inc+=1
         var = StringVar()
         var.set("...") 
         self.w = OptionMenu(self, var,*option[0],command=lambda v=0,indx=chk_id, groupID=loc[3]: self.clickOption(v,indx,groupID,talk_order))#command includes a default arg, the chosen option  
         self.w.grid(row=row_inc,column=col_inc,rowspan=len(option[0]),sticky=W)
##         self.w.configure(state="disabled")
##         self.opt_action[(loc[3],chk_id)]=[option[1]]
         
         self.chk_action[(loc[3],chk_id)]=[self.w]
         self.reseting.append(var)
         self.vars2[(loc[3],chk_id)]=[var]
         
         if two_drops[0]:
            if len(option[0]) == 2:#bad code
               what=["A","B","C","D"]#what is the available actions
##               print option[0]
               [what.remove(i) for i in option[0]]
               option=[what,None]
            elif len(option[0]) == 3:
##               print option[0]
               what=["A","B","C","D","E","F"]
               [what.remove(i) for i in option[0]]
               option=[what,None]
               
               
            
            col_inc+=1
            Label(self,text=two_drops[label_indx]).grid(row=row_inc,column=col_inc,sticky=W)
            self.opt_action[(loc[3],chk_id)]=two_drops[label_indx]
            label_indx+=1
            col_inc+=1
            var = StringVar()
            var.set("...") # default value
            self.w = OptionMenu(self, var,*option[0],command=lambda v=0,indx=chk_id, groupID=loc[3]: self.clickOption(v,indx,groupID,talk_order))#command includes a default arg, the chosen option  
            self.w.grid(row=row_inc,column=col_inc,rowspan=len(option[0]),sticky=W)
##            self.w.configure(state="disabled")
            
            self.chk_action[(loc[3],chk_id)]=self.chk_action[(loc[3],chk_id)]+[self.w]
            self.reseting.append(var)
            self.vars2[(loc[3],chk_id)]=self.vars2[(loc[3],chk_id)]+[var]
         row_inc+=len(option[0])#number of actions is the number of rows a menu spans
         chk_id+=1
         
   def on_check(self,indx,groupID):#ids the checkbutton upon clicking itself
      self.clicked=indx
      self.groupID=groupID

   def clickOption(self,option,indx,groupID,talk_orders):
      if groupID == 3:
         group=propose
      elif groupID == 4:
         group=feel
      elif groupID == 5:
         group=feel2
      else:
         group=feel3
         
      sig=True
      menus=self.vars2[(groupID,indx)]
      for i in menus:
         self.vars[groupID,indx].set(1)#
         if i.get() == "...":
            sig=False
      if sig is True:
         d=read_reorders(talk_orders)
         replace_idx=END
         for i in talk_orders.get(0,END):
            i2=i.replace(group[indx],"")
            if len(i) !=len(i2):
               replace_idx=d.get(i,[0])[1]
               talk_orders.delete(replace_idx)
               
               if len(read_reorders(talk_orders))==0:
                  self.tb.submit.configure(text="send no message")
               break
         
         if groupID ==3:
            message=self.check_now(groupID,indx)
            show=group[indx]+menus[0].get()+message+menus[1].get()+"."#period is proper English by doc
         elif groupID ==4:
            show=group[indx]+menus[0].get()+"."
         elif groupID ==5:
            show=group[indx]+menus[0].get()+"."
         elif groupID ==6:
            show=group[indx]+menus[0].get()+"."
         else: print "This error is not expected."
         
         if len(read_reorders(talk_orders))==0:
            self.tb.submit.configure(text="Send message")
            
         talk_orders.insert(replace_idx,show)

   def check_now(self,group,ind):
      return self.opt_action[group,ind]
   def worker(self, talk_order):
      d=read_reorders(talk_order)
      if self.groupID == 3:
         group=propose
      elif self.groupID == 4:
         group=feel
      elif self.groupID == 5:
         group=feel2
      else:
         group=feel3
              
      if self.state(self.groupID,self.clicked) != 1:
         
##         map((lambda child: child.configure(state="normal")), self.chk_action[(self.groupID,self.clicked)])
##      else:
         
         for i in talk_order.get(0,END):
            i2=i.replace(group[self.clicked],"")
            if len(i) !=len(i2):
               talk_order.delete(d[i][1])
               
               if len(read_reorders(talk_order))==0:
                  self.tb.submit.configure(text="send no message")
                  
               break
         map(lambda child: child.set("..."), self.vars2[(self.groupID,self.clicked)])
##         map((lambda child: child.configure(state="disabled")), self.chk_action[(self.groupID,self.clicked)])

         
   def state(self,group,ind): #for each click on a checkbutton calls this and outputs the updated states globally                   
      return self.vars[(group,ind)].get()
   
    
      
class Checkbar(Frame):
   """factory of class Speechbutton for displaying, interactions between reordering window"""
   def __init__(self, parent=None, picks=[], C_title=[], col_info=[0,0], talk_order=None, master=None, start_x=0, start_y=0):
      Frame.__init__(self, parent,width=625,height=270)

      # self.config(container=700)
      self.tb=master      
      self.chks=[]
      self.vars = [] #state value
      self.clicked=-1#to track which button is clicked
      self.groupID=None #from which speech group
  
      fontH16 = tkFont.Font(family="Helvetica", size=16)

      if A[0] == 2:
         P1_A=["A","B"]
         P2_A=["C","D"]
      else:
         P1_A=["A","B","C"]
         P2_A=["D","E","F"]

      solutions=pairs(P1_A,P2_A)  
      combo1=[[solutions,"Let's alternate between "]]
      combo2=[[solutions,i] for i in feel]
      combo3=[[solutions,i] for i in feel2] 
      if self.tb.player%2 == 0:
         combo4=[[P2_A,i] for i in feel3] 
      else:
         combo4=[[P1_A,i] for i in feel3] 

      self.C2_DM = DropMenu(self,combo2,[0,4,len(solutions),4],talk_order,self.tb)
      # self.C2_DM.grid(row=0,column=0,sticky=W)
      self.C2_DM.place(x=5,y=0)
      self.tb.choise.extend([self.C2_DM])
      self.tb.DM_vars.extend(self.C2_DM.reseting)#for reseting
      self.tb.DM_labels.extend(self.C2_DM.labels)

      self.C1_DM = DropMenu(self,combo1,[len(feelings)+10,0,len(solutions),3], talk_order,self.tb,[True," and "])
      self.C1_DM.place(x=5,y=25)
      # self.C1_DM.grid(row=1,column=0)#row=len(plans)+9,column=0,columnspan=4,sticky=N)
      self.tb.DM_vars.extend(self.C1_DM.reseting)
      self.tb.DM_labels.extend(self.C1_DM.labels)
      self.tb.choise.extend([self.C1_DM])

      self.C3_DM = DropMenu(self,combo3,[0,4,len(solutions),5],talk_order,self.tb)
      self.C3_DM.place(x=5,y=50)
      self.tb.choise.extend([self.C3_DM])
      self.tb.DM_vars.extend(self.C3_DM.reseting)#for reseting
      self.tb.DM_labels.extend(self.C3_DM.labels)   
      
      self.C4_DM = DropMenu(self,combo4,[0,4,len(solutions),6],talk_order,self.tb)
      self.C4_DM.place(x=5,y=75)
      self.tb.choise.extend([self.C4_DM])
      self.tb.DM_vars.extend(self.C4_DM.reseting)#for reseting
      self.tb.DM_labels.extend(self.C4_DM.labels)   
      # if C_title[1] ==1:
      picks,picks2=picks[:len(picks)/2-2],picks[len(picks)/2-2:]#divide feelings into two equal columns
      row_inc = 0
      horz,vert=5,100
      for pick in picks:#this the first column in feeling tab
         var = IntVar()
         chk = Checkbutton(self, text=pick, variable=var,command=lambda:self.show_talk(talk_order))
         chk.place(x=horz,y=vert)
         # chk.grid(row=3+row_inc, column=0,columnspan=col_info[1],sticky=W)
         chk.bind('<Button-1>', lambda event, indx=row_inc, groupID=C_title[1]: self.on_check(indx,groupID))
##         chk.focus_set()
         row_inc+=1
         vert+=24
         self.vars.append(var)
         self.chks.append(chk)#dropdown menu needs this

      row_inc2 = 0   
      # if C_title[1] == 1:
      horz,vert=390,0#bad code, these should be passed in
      for pick in picks2:#this the second column in feeling tab
         var = IntVar()
         chk = Checkbutton(self, text=pick, variable=var,command=lambda:self.show_talk(talk_order))
         # chk.grid(row=row_inc2, column=0+3,columnspan=col_info[1],sticky=NW)
         chk.place(x=horz,y=vert)
         chk.bind('<Button-1>', lambda event, indx=row_inc, groupID=C_title[1]: self.on_check(indx,groupID))
##         chk.focus_set()
         row_inc+=1
         row_inc2+=1
         vert+=24#spacing in vertical
         self.vars.append(var)
         self.chks.append(chk)#dropdown menu needs this
         
   def on_check(self,indx,groupID):#ids the checkbutton upon clicking itself
      self.clicked=indx
      self.groupID=groupID
        
   def show_talk(self,talk_order):##shows in reordering window
      if self.groupID==0:
         group=plans
      elif self.groupID==1:
         group=feelings
      else:
         group=fix_relationship

      d=read_reorders(talk_order)#read the current ordering
         
      values=self.state()
      bundle=d.get(group[self.clicked],[0])

         
      if values[self.clicked] ==1:
         if bundle[0] == 0:
            if len(d)==0:
               self.tb.submit.configure(text="Send message")
            talk_order.insert(END,group[self.clicked])
         else:
            print "this must be an error"
      else:
         if bundle[0]==1:               
            talk_order.delete(bundle[1])##if raises index out of range, reason is in block#**
            if len(read_reorders(talk_order))==0:
               self.tb.submit.configure(text="send no message")
            
   def state(self): #for each click on a checkbutton calls this and outputs the updated states globally                   
      return map((lambda var: var.get()), self.vars)
   

         
      
   
   
class speech_log(Frame):
   '''a changing size canvas for messaging dialog'''
   def __init__(self,parent=0):
      Frame.__init__(self,parent)

      self.game_proxy=None#for talk_button disable actions on game
      

      self.canvas = Canvas(self,width=516,height=306,scrollregion=(0,0,530,500),bd=0)
      self.vscrollbar = Scrollbar(self, orient=VERTICAL,command=self.canvas.yview)
      self.canvas.configure(yscrollcommand=self.vscrollbar.set)

      self.canvas.grid(row=0,column=1,sticky=NSEW)


      self.vscrollbar.grid(row=0,column=2, rowspan=6, sticky=NSEW)

      self.interior = interior = Frame(self.canvas)

      self.interior2 = interior2 = Frame(self.canvas)

      self.canvas.create_window(0,4, window=interior,anchor=NW)
      self.canvas.create_window(258,4, window=interior2,anchor=NW)

##      self.canvas.create_rectangle(1,1,521,308)


      ##mark to the interior height
      self.track_height=interior.winfo_reqheight()

      self.last_text=None#alines two speeches
      self.last_h=None

      self.response=None
      self.response_h=None
      
      ##update the text region as interior grows
      def _configure_interior(event):
         size=(interior.winfo_reqwidth(), interior.winfo_reqheight())
         self.canvas.config(scrollregion="0 0 %s %s" % size)

         ##scroll to the bottom 
         if self.track_height!=interior.winfo_reqheight():#without this, scrolling is confused
            self.canvas.yview_moveto(1)

         self.track_height=interior.winfo_reqheight()

      interior.bind('<Configure>', _configure_interior)

      

      ##text region in canvas
      text=Text(self.interior,height=0,width=37)
      text.config(state='disabled')
      text.grid()

      text2=Text(self.interior2,height=0,width=36)
      text2.config(state='disabled')
      text2.grid()

class Status:#this holds the status text on log so that it is deleted on move
   def __init__(self):
      self.text1=None
      self.text2=None
      self.text3=None#This is for aligning status when waiting on partner.

def write(obj, txt, who_said,h,w,player=None,is_status=False,ur_color=None):
   '''write talks to talk window'''
##   orange = "#%02x%02x%02x" % (185, 127, 33) #"orange"
   orange = "#%02x%02x%02x" % (255, 128, 10) #"orange"
##   blue = "#%02x%02x%02x" % (72, 152, 182) #"blue"
   blue = "#%02x%02x%02x" % (10, 152, 255) #"blue"
   if who_said==0:
      pos='s'
      f_color="green"
   elif who_said==1:
      pos='e'
      window=obj.interior2
      if player ==0:
         f_color=orange
      else:
         f_color=blue
   elif who_said==2:
      pos='w'
      window=obj.interior
      if player ==0:
         f_color=blue
      else:
         f_color=orange
   elif who_said==11:
      window=obj.interior2
      f_color="black"
      pos='e'
   elif who_said==22:
      window=obj.interior
      f_color="black"
      pos='w'
   else:
      print "0==",who_said
      
   if who_said==0:
      txt2,txt1=txt[:len(txt)/2],txt[len(txt)/2:]

      text2=Text(obj.interior,height=1,width=len(txt2),bd=0)
      text1=Text(obj.interior2,height=1,width=len(txt1),bd=0)
      if is_status:
         Status.text1=text1
         Status.text2=text2
         text1.config(fg="red")
         text2.config(fg="red")
      if ur_color != None:
         text1.config(fg=ur_color)
         text2.config(fg=ur_color)         
      text1.insert(END,txt1)
      text2.insert(END,txt2)
      text1.grid(sticky="w")
      text2.grid(sticky="e")
      text1.config(state='disabled',wrap='word')
      text2.config(state='disabled',wrap='word')

   else:
      text=Text(window,height=h,width=w,wrap='word')
   ##         text.config(bg='blue',relief=RAISED)
      text.config(fg=f_color,relief=RAISED)
      text.insert(END,txt)
      text.config(state='disabled')
      text.grid(sticky=pos)
      if is_status:#for aligning the the status on log
         Status.text3=text
   if who_said == 1:
      obj.last_text=text
      obj.last_h=h
   elif who_said == 2:
      obj.response=text
      obj.response_h=h


      
def extract_id():
   replace={}
   extra=[" and "]
   for i in range(len(propose)):
      replace[propose[i]]=extra[i] 
   return replace

def speech2id(speeches,player):
   '''sender converts speeches to ids before sending'''
   ids=''
   for s in speeches:
      if s[-2] in "ABCDEF":#really bad technique
         #do a loop
         for i in propose:
            s2=s.replace(i,"")
            if len(s) !=len(s2):
               more=extract_id()
               s2=s2.replace(more[i],"")
               # if len(s2)==4:
               #    # if player ==0:#perspective is disabled
               #    s2=s2[0]+s2[1]+" "+s2[-2]+s2[-1]#for solution, changing perspective
               #    # else:
               #    #    s2=s2[1]+s2[0]+" "+s2[-1]+s2[-2]
               # if player ==0 and len(s2)==2:
               #    s2=s2[1]+s2[0]
               s2=s2.rstrip(".")
               ids+=str(directory[i])+" "+s2[:2]+" "+ s2[2:]#rstrips proper English by doc

         for j in feel:
            s2=s.replace(j,"")
            if len(s) !=len(s2):
               ids+=str(directory[j])+" "+s2.rstrip(".")

         for k in feel2:
            s2=s.replace(k,"")
            if len(s) !=len(s2):
               ids+=str(directory[k])+" "+s2.rstrip(".")
         for k in feel3:
            s2=s.replace(k,"")
            if len(s) !=len(s2):
               ids+=str(directory[k])+" "+s2.rstrip(".")

      else:
         ids+=str(directory[s])
         
      ids+=";"
   return ids

def id2speech(dosh,player):
   '''receiver converts ids to corresponding speech'''
   speeches=[]

   dosh=dosh.split('$')
   print "This is all together received: ",dosh
   if len(dosh) == 0:#rescue code, very messy
      dosh="$"
   elif len(dosh) == 2:
      dosh=dosh[0]
      dosh = dosh+'$'
   else:
      dosh=dosh[0]
      dosh = dosh+'$'
   print "real speech that to be parsed: ", dosh

   if dosh ==";$":
      speeches=[]
   else:
      id_list = dosh.split(";")
      for i in id_list:
         
         if i != "$":
            if len(i) ==0:
               break
            elif len(i) <= 2:
               pass
            elif len(i) ==4:
               i,first=i.split()
            elif len(i) == 5:
               print "this is to split", i
               i,bundle=i.split()
               first,second=bundle[0],bundle[1]
            else:
               # i,bundle=i.split()
               # first,second=bundle[:2],bundle[2:]
               i,first,second=i.split()

##            print "here is the msg: ",id2msg[int(i)]
            if id2msg[int(i)] in propose:
               more=extract_id()

               if player==1 and len(first) ==1:
                  speeches.append(id2msg[int(i)]+second+more[id2msg[int(i)]]+first+".")#period is proper English by doc
               else:
                  speeches.append(id2msg[int(i)]+first+more[id2msg[int(i)]]+second+".")
            elif id2msg[int(i)] in feel:
               speeches.append(id2msg[int(i)]+first+second+".")
            elif id2msg[int(i)] in feel2:
               speeches.append(id2msg[int(i)]+first+second+".")
            elif id2msg[int(i)] in feel3:
               speeches.append(id2msg[int(i)]+first+".")
            else:
               speeches.append(id2msg[int(i)])
   return speeches

def to_write(speeches):
   '''formating the speeches so that fits in predefined text sizes in canvas'''
   say=""
   widths=[]
   width=0
   height=len(speeches)#heuristic
      
   for s in speeches:

      l=len(s)##1 is for text box size on canvas
      if l < 35:
         widths.append(l)
      else:
         h=ceil(l/35.0)
         height+=h-1 #h is one long string may render in multiple lines, -1 because we considered 1 for each msg in height
         width =35
         
      say+=s##2 is for msgs in separate lines
      say+="\n"
   say=say.rstrip("\n")
   
   if width == 35:##1
      pass
   else:
      if len(widths)!=0:#max an empty list incurs error
         width=max(widths)
      else: pass
   return say,height,width   

def gray_out(list_of_frames,status):
   '''input a list of some frames or one that contains widget/s,
   not like the whole window(didn't work for me, guessing not working recursively),
   not an individual widget either '''
   for i in list_of_frames:
      map((lambda child: child.configure(state=status)), i.winfo_children())
       ##update the text region as interior grows
     

def pairs(a,b):
   collect=[]
   for i in a:
      for j in b:
         collect.append(i+j)
   return collect


    
    
class speech_button(Frame):
   '''displaying lower part of the GUI, submit button events'''

   def __init__(self,master,whole_canv=None,talks=None,player=-1,A=None,connection=None):
      Frame.__init__(self,master)

      self.master=master
      self.talks=talks

      self.player=player
      self.connection=connection
      self.check_buttons=[] #for reseting from reordering box
      self.chks=[]
      self.drop_label=[]
      self.choise=[]
      self.DM_vars=[]
      self.DM_labels=[]

      txt,h,w=to_write(["   Send chat ..."])
      write(self.talks,txt,0,h+1,w,self.player%2,True)
      
      self.action_only=True
      
      self.orders=Talk_orders(master,len(feelings)+8,7,self.check_buttons,self.choise,self)

      speechActsWidth = 660
      speechActsHeight = 300
 
      plans_x = 20;
      speechActsStart_y = 360

      whole_canv.create_rectangle(3,speechActsStart_y,speechActsWidth+3,speechActsStart_y+speechActsHeight+10)
      whole2 = Canvas(master, width=speechActsWidth, height=speechActsHeight, bd=0)
      
 
      self.whole3=whole_canv#instantiate the root canvas
      self.whole3.create_rectangle(675,353,1075,680,outline='red',tags="talk_rect")
      


      if A[0] == 2:
         # if self.player%2==0:
            # Actions=["C","D"]
         P1_A=["A","B"]
         P2_A=["C","D"]
         # else:
         #    # Actions=["A","B"]
         #    P1_A=["C","D"]
         #    P2_A=["A","B"]
      else:
         # if self.player%2==0:
            # Actions=["D","E","F"]
         P1_A=["A","B","C"]
         P2_A=["D","E","F"]
         # else:
         #    # Actions=["A","B","C"]
         #    P1_A=["D","E","F"]
         #    P2_A=["A","B","C"]
            
            
         
      solutions=pairs(P1_A,P2_A)  
      combo1=[[solutions,"Let's alternate between "]]

      
      column_title="Let's Talk"
      self.C2 = Checkbar(master, feelings, [column_title,1],[4,4],self.orders.dd,self)
      self.chks.extend(self.C2.chks)
      self.C2.grid_propagate(0)#customize Frame size
      self.C2.place(x=plans_x,y=speechActsStart_y+20)#self.C2.grid(row=7,column=4, rowspan=len(feelings)+1+13, columnspan=3)
      self.C2.config(relief=GROOVE, bd=2)
      self.check_buttons.extend(self.C2.vars)
 

      self.submit=Button(master, text='Send no message', command=self.allstates)
##      submit.grid(row=len(feelings)+7+1+9+1,column=8)
      # self.submit.place(x=847,y=665)
      self.submit.place(x=800,y=640)
      self.submit_loc=self.submit.place_info()

      self.waiting =True

      self.no_msg=False
      self.rounds=1

      
      
      # self.timestamp1=ctime().split(" ")[3]##for data logging only
      self.timestamp1=datetime.datetime.now()
      self.timestamp2=-1
      self.timestamp3=-1
      self.ur_talk=None
      self.his_talk=None
      
      def _button_click(event):
         if self.submit['state'] == "normal":
            gray_out([self.C2.C1_DM,self.C2.C2_DM,self.C2.C3_DM,self.C2.C4_DM],"disabled")
            map((lambda child: child.configure(state="disabled")), self.chks)
            
            Proxy.canvas.delete('oval')
            Status.text1.destroy()
            Status.text2.destroy()

            rnd_txt="Current Round: %d" %self.rounds##log the round #
            txt,h,w=to_write([rnd_txt])
            write(self.talks,txt,0,h,w)
            
            reordered=self.orders.dd.get(0,END)
            if len(reordered)==0:
               self.no_msg=True
               write(self.talks,"<No message sent>",1,h,20,self.player%2)

            else:
               content,h,w =to_write(reordered)
               write(self.talks,content,1,h,w,self.player%2)

            write(self.talks,"",2,h,1,self.player%2,True)#dummy text widget for aligning



            dish=speech2id(reordered,self.player%2)
            print "+"*20
            print dish
            dish+="$"
            
            self.timestamp2=datetime.datetime.now()#for logging
            dish+=" %.2f"% datetime.timedelta.total_seconds(self.timestamp2-self.timestamp1)#commentout to enable sending duration
            self.ur_talk=dish
            self.connection.send(dish)
            
            for i in reordered:
               self.orders.dd.delete(0)

            txt,h,w=to_write(["    Waiting for your partner's message ..."])
            write(self.talks,txt,0,h+1,w,self.player%2,True)

      self.submit.bind('<Button>', _button_click)

        
   def allstates(self):
      print "before receiving the chat ..............."
      dosh=self.connection.recv(1024)##cheaptalk communications
      print "this is the chat received: "+"*"*15
      print dosh

      self.his_talk=dosh
      
      Status.text1.destroy()
      Status.text2.destroy()
      Status.text3.destroy()
      
      dosh=id2speech(dosh,self.player%2)

      content,h,w =to_write(dosh)


      if len(content)==0:
         print "only response is 0"
         write(self.talks,"<No message sent>",2,self.talks.last_h,20,self.player%2)
         
      elif h>self.talks.last_h:
         self.talks.last_text.configure(height=h)

         write(self.talks,content,2,h,w,self.player%2)

      elif h<self.talks.last_h:
         write(self.talks,content,2,self.talks.last_h,w,self.player%2)
##         self.talks.response.configure(height=self.talks.last_h)
      elif h==self.talks.last_h:
         write(self.talks,content,2,h,w,self.player%2)

      else:
         print "msg length is not normal"

      txt,h,w=to_write(["Choose an action ..."])
      write(self.talks,txt,0,h+1,w,self.player%2,True)      

      self.submit.configure(text="Send no message",state="disabled")
      print "0's msgs are sent**********"

      draw_rect=Proxy.rect_coord
      self.whole3.delete("talk_rect")
      Proxy.game_canv.create_rectangle(*draw_rect,outline='red',tags="game_rect")

      talk=re.split("[\n]",content)
      if len(content)==0:
         pass
      elif len(talk) >5:
         call(['say', "Bla bla bla."])

      else:
         call(['say', content])
      
      self.timestamp3=datetime.datetime.now()#for logging


      map((lambda child: child.configure(state="normal")), Proxy.buttons)#enabling the game buttons
      self.submit.place_forget()
      
      indes=0#making game buttons visible again, stupid Tkinter
      for i in Proxy.buttons:
         i.place(Proxy.buts_places[indes])
         indes+=1



  
class Proxy:
   '''This enables parent class talk_buttons to disable buttons in child class game'''
   def __init__(self):
      self.buttons=None
      self.canvas=None
      self.game_canv=None
      self.rect_coord=None
      self.is_enable=False
      self.buts_places=[]

class CloseEvents():
   def __int__(self):
      self.closeOk=False

class game(Frame):
   '''displaying the matrix game, auto adjustment for 2 actions or 3 and button events'''
   def __init__(self,master=0,M=None,A=None,talk_display=None,talk_buttons=None,player=None,iters=-1,gamename=None,GA=None,sock=None):
      Frame.__init__(self,master)
      self.window=master#to be destroyed when gameover
      self.A=A
      self.talk_buttons=talk_buttons
      self.player=player
      self.iters=iters
      self.gamename=gamename #for ranking only
      self.group_agent=GA #for ranking only
      self.sock=sock
      self.buttons=[]

      self.v = IntVar()
      self.V=9
      CloseEvents.closeOk=False


      # self.p1col = "#%02x%02x%02x" % (185, 127, 33) #"orange"
      # self.p2col = "#%02x%02x%02x" % (72, 152, 182) #"blue"
      # mygray = "#%02x%02x%02x" % (100, 100, 100)
      self.p1col = "#%02x%02x%02x" % (255, 127, 10) #"orange"
      self.p2col = "#%02x%02x%02x" % (72, 152, 255) #"blue"
      mygray = "#%02x%02x%02x" % (100, 100, 100)


      fontH24 = tkFont.Font(family="Helvetica", size=24)
      fontH20 = tkFont.Font(family="Helvetica", size=20)
      fontH16 = tkFont.Font(family="Helvetica", size=16)#never make this for accessing as instance, overided below
      
      gameWidth = 550
      gameHeight = 330
      gameStart_x = 0
      gameStart_y = 0
      matrixCorn_x = 150
      matrixCorn_y = 150
      if (A[0] == 2):
         matrixCorn_x = 165
         matrixCorn_y = 170

      matrixColWidth = 110
      matrixRowHeight = 49
      
      self.whole = Canvas(master, width=gameWidth, height=gameHeight, bd=0)
      self.whole.create_rectangle(3,10,gameWidth-2,gameHeight)
      
      
      self.whole.place(x=0,y=0)
      Proxy.game_canv=self.whole
      
      P1=[]
      P2=[]
      

      self.mine=0.0##accumulative payoff
      self.his=0.0
      self.avg=Label(master,text="0.00",font=fontH16)
      self.earn=Label(master,text="0.00",font=fontH16)
      
      u4log=Label(master,text="You")
      u4log.place(x=920,y=3)#bad code
      ur4log=Label(master,text="Your partner")
      ur4log.place(x=665,y=3)
      if A[0] ==2:
         cx = gameWidth/2 - 50
      

         self.whole.create_text(cx-50, 39, text = "Your avg payout:", anchor="nw", font=fontH16, fill=mygray)
         self.avg.place(x = cx+95, y = 35)
         
         self.whole.create_text(cx-50, 61, text = "Your earnings:", anchor="nw", font=fontH16, fill=mygray)
         self.earn.place(x = cx+95, y = 58)

         self.whole.create_text(cx+155, 62, text = "(AED)", anchor="nw", font=fontH16, fill=mygray)

         P2_L1="C"
         P2_L2="D"


         if (self.player%2 == 0):

            partner=Label(master,text="Your Partner",font=fontH24,fg=self.p2col)
            partner.place(x=matrixCorn_x+42,y=matrixCorn_y-60)
            
            yaall=Label(master,text="You",font=fontH24,fg=self.p1col)
            yaall.place(x=25, y=matrixCorn_y + matrixRowHeight - 17)
            self.ur_color=self.p1col#for your color in ranking
            
            ur4log.config(fg=self.p2col)
            u4log.config(fg=self.p1col)
            
            self.P2_A1=Label(master, text=P2_L1, font=fontH16)
            self.P2_A1.config(fg=self.p2col)
            self.P2_A1.place(x=matrixCorn_x+matrixColWidth/2 - 5, y=matrixCorn_y-25)
            self.P2_A2=Label(master, text=P2_L2, font=fontH16)
            self.P2_A2.config(fg=self.p2col)
            self.P2_A2.place(x=matrixCorn_x+matrixColWidth+matrixColWidth/2 - 10, y=matrixCorn_y-25)
         else:
            partner=Label(master,text="You",font=fontH24,fg=self.p2col)
            partner.place(x=matrixCorn_x+matrixColWidth-25,y=matrixCorn_y-65)
            self.ur_color=self.p2col#for your color in ranking

            yaall=Label(master,text="Your\nPartner",font=fontH24,fg=self.p1col)
            yaall.place(x=35, y=matrixCorn_y + 21)
            
            
            ur4log.config(fg=self.p1col)
            u4log.config(fg=self.p2col)
            
            self.P2_A1=Label(master, text=P2_L1, font=fontH16)#very silly, but when buttons are hidden to show the user what is playing
            self.P2_A1.config(fg=self.p2col)
            self.P2_A1.place(x=matrixCorn_x+matrixColWidth/2 - 5, y=matrixCorn_y-25)
            self.P2_A2=Label(master, text=P2_L2, font=fontH16)
            self.P2_A2.config(fg=self.p2col)
            self.P2_A2.place(x=matrixCorn_x+matrixColWidth+matrixColWidth/2 - 10, y=matrixCorn_y-25)

            self.P2_A1=Button(master, text=P2_L1, command=lambda: self.ShowChoice(0))
            self.P2_A1.place(x=matrixCorn_x+matrixColWidth/2 - 15, y=matrixCorn_y-25)
            self.P2_A2=Button(master, text=P2_L2, command=lambda: self.ShowChoice(1))
            self.P2_A2.place(x=matrixCorn_x+matrixColWidth+matrixColWidth/2 - 23, y=matrixCorn_y-25)
            
            P2.extend([self.P2_A1,self.P2_A2])
      else:
         cx = gameWidth/2
      

         self.whole.create_text(cx-50, 39, text = "Your avg payout:", anchor="nw", font=fontH16, fill=mygray)
         self.avg.place(x = cx+95, y = 35)

         
         self.whole.create_text(cx-50, 61, text = "Your earnings:", anchor="nw", font=fontH16, fill=mygray)
         self.earn.place(x = cx+95, y = 58)
         self.whole.create_text(cx+155, 62, text = "(AED)", anchor="nw", font=fontH16, fill=mygray)

         P2_L1="D"
         P2_L2="E"
         P2_L3="F"
         if (self.player%2 == 0):
            partner=Label(master,text="Your Partner",font=fontH24,fg=self.p2col)
            partner.place(x=matrixCorn_x+94,y=matrixCorn_y-60)

            yaall=Label(master,text="You",font=fontH24,fg=self.p1col)
            yaall.place(x=20, y=matrixCorn_y + matrixRowHeight + 8)
            self.ur_color=self.p1col#for your color in ranking
            
            ur4log.config(fg=self.p2col)
            u4log.config(fg=self.p1col)
            
            self.P2_A1=Label(master, text=P2_L1, font=fontH16)
            self.P2_A1.config(fg=self.p2col)
            self.P2_A1.place(x=matrixCorn_x+matrixColWidth/2-10 , y=matrixCorn_y-25)
            self.P2_A2=Label(master, text=P2_L2, font=fontH16)
            self.P2_A2.config(fg=self.p2col)
            self.P2_A2.place(x=matrixCorn_x+matrixColWidth+matrixColWidth/2-10, y=matrixCorn_y-25)
            self.P2_A3=Label(master, text=P2_L3, font=fontH16)
            self.P2_A3.config(fg=self.p2col)
            self.P2_A3.place(x=matrixCorn_x+matrixColWidth*2+matrixColWidth/2 - 10, y=matrixCorn_y-25)
         else:
            partner=Label(master,text="You",font=fontH24,fg=self.p2col)
            partner.place(x=matrixCorn_x+matrixColWidth+32,y=matrixCorn_y-60)
            self.ur_color=self.p2col#for your color in ranking
            
            yaall=Label(master,text="Your\nPartner",font=fontH24,fg=self.p1col)
            yaall.place(x=20, y=matrixCorn_y + matrixRowHeight - 6)

            ur4log.config(fg=self.p1col)
            u4log.config(fg=self.p2col)
  
            self.P2_A1=Label(master, text=P2_L1, font=fontH16)#when buttons are hidden user see what is playing
            self.P2_A1.config(fg=self.p2col)
            self.P2_A1.place(x=matrixCorn_x+matrixColWidth/2 - 10, y=matrixCorn_y-25)
            self.P2_A2=Label(master, text=P2_L2, font=fontH16)
            self.P2_A2.config(fg=self.p2col)
            self.P2_A2.place(x=matrixCorn_x+matrixColWidth+matrixColWidth/2 - 10, y=matrixCorn_y-25)
            self.P2_A3=Label(master, text=P2_L3, font=fontH16)
            self.P2_A3.config(fg=self.p2col)
            self.P2_A3.place(x=matrixCorn_x+matrixColWidth*2+matrixColWidth/2 - 10, y=matrixCorn_y-25)

            self.P2_A1=Button(master, text=P2_L1,command=lambda: self.ShowChoice(0))
            self.P2_A1.place(x=matrixCorn_x+matrixColWidth/2 - 20, y=matrixCorn_y-25)
            self.P2_A2=Button(master, text=P2_L2,command=lambda: self.ShowChoice(1))
            self.P2_A2.place(x=matrixCorn_x+matrixColWidth+matrixColWidth/2 - 20, y=matrixCorn_y-25)
            self.P2_A3=Button(master,text=P2_L3,command=lambda: self.ShowChoice(2))
            self.P2_A3.place(x=matrixCorn_x+matrixColWidth*2+matrixColWidth/2 - 20, y=matrixCorn_y-25)
         
            P2.extend([self.P2_A1,self.P2_A2,self.P2_A3])


      if A[0] == 2:
         P1_L1="A"
         P1_L2="B"
         if self.player%2 == 0:
            self.P1_A1=Label(master, text=P1_L1, font=fontH16)#when buttons are hidden
            self.P1_A1.config(fg=self.p1col)
            self.P1_A2=Label(master, text=P1_L2, font=fontH16)
            self.P1_A2.config(fg=self.p1col)
            self.P1_A1.place(x=matrixCorn_x - matrixColWidth/2 +10, y=matrixCorn_y + 13)
            self.P1_A2.place(x=matrixCorn_x - matrixColWidth/2 +10, y=matrixCorn_y + matrixRowHeight + 11)
   
                    
            self.P1_A1=Button(master, text=P1_L1,command=lambda: self.ShowChoice(0))
            self.P1_A2=Button(master, text=P1_L2,command=lambda: self.ShowChoice(1))
            self.P1_A1.place(x=matrixCorn_x - matrixColWidth/2 +10, y=matrixCorn_y + 13)
            self.P1_A2.place(x=matrixCorn_x - matrixColWidth/2 +10, y=matrixCorn_y + matrixRowHeight + 11)


            P1.extend([self.P1_A1,self.P1_A2])
         else:
            self.P1_A1=Label(master, text=P1_L1, font=fontH16)
            self.P1_A1.config(fg=self.p1col)
            self.P1_A2=Label(master, text=P1_L2, font=fontH16)
            self.P1_A2.config(fg=self.p1col)
            self.P1_A1.place(x=matrixCorn_x - 19, y=matrixCorn_y + 18)
            self.P1_A2.place(x=matrixCorn_x - 19, y=matrixCorn_y + matrixRowHeight + 18)
         
      else:
         P1_L1="A"
         P1_L2="B"
         P1_L3="C"
         if self.player%2 == 0:
            self.P1_A1=Label(master, text=P1_L1, font=fontH16)
            self.P1_A1.config(fg=self.p1col)

            self.P1_A2=Label(master, text=P1_L2, font=fontH16)
            self.P1_A2.config(fg=self.p1col)

            self.P1_A3=Label(master, text=P1_L3, font=fontH16)
            self.P1_A3.config(fg=self.p1col)
            self.P1_A1.place(x=matrixCorn_x - matrixColWidth/2 +10, y=matrixCorn_y + 13)
            self.P1_A2.place(x=matrixCorn_x - matrixColWidth/2 +10, y=matrixCorn_y + matrixRowHeight + 11)
            self.P1_A3.place(x=matrixCorn_x - matrixColWidth/2 +10, y=matrixCorn_y + 2*matrixRowHeight + 10)#
            self.P1_A1=Button(master,text=P1_L1, command=lambda: self.ShowChoice(0))
            self.P1_A2=Button(master,text=P1_L2, command=lambda: self.ShowChoice(1))
            self.P1_A3=Button(master,text=P1_L3, command=lambda: self.ShowChoice(2))
            self.P1_A1.place(x=matrixCorn_x - matrixColWidth/2 +10, y=matrixCorn_y + 13)
            self.P1_A2.place(x=matrixCorn_x - matrixColWidth/2 +10, y=matrixCorn_y + matrixRowHeight + 11)
            self.P1_A3.place(x=matrixCorn_x - matrixColWidth/2 +10, y=matrixCorn_y + 2*matrixRowHeight + 10)
            
            P1.extend([self.P1_A1,self.P1_A2,self.P1_A3])
         else:
            self.P1_A1=Label(master, text=P1_L1, font=fontH16)
            self.P1_A1.config(fg=self.p1col)

            self.P1_A2=Label(master, text=P1_L2, font=fontH16)
            self.P1_A2.config(fg=self.p1col)

            self.P1_A3=Label(master, text=P1_L3, font=fontH16)
            self.P1_A3.config(fg=self.p1col)
         
            self.P1_A1.place(x=matrixCorn_x - 19, y=matrixCorn_y + 17)
            self.P1_A2.place(x=matrixCorn_x - 19, y=matrixCorn_y + matrixRowHeight + 15)
            self.P1_A3.place(x=matrixCorn_x - 19, y=matrixCorn_y + 2*matrixRowHeight + 14)
         
      if self.player%2==0:#for reactivating the buttons for next round
         self.buttons.extend(P1)
      else:
         self.buttons.extend(P2)
      if self.talk_buttons==None:
         map((lambda child: child.configure(state="normal")), self.buttons)
      else:
         map((lambda child: child.configure(state="disabled")), self.buttons)
      
      Proxy.buttons=self.buttons#bridges talk_buttons to game
      Proxy.buts_places=[i.place_info() for i in self.buttons]

      
      wh={}
      wh[2]=[matrixColWidth*2,matrixRowHeight*2]
      wh[3]=[matrixColWidth*3,matrixRowHeight*3]
      x=wh[A[0]][0]
      y=wh[A[0]][1]
      self.w = Canvas(master, width=x, height=y,bd=0, relief="sunken")
      
      Proxy.canvas=self.w #clear out oval after viewing
      
      ovsz=3#refers to oval size, the bigger number == smaller oval,lower limit==0,upper==?


      if A[0] == 2:
         self.w.create_rectangle(3,4,x,y)
         self.w.create_line(3, y/2.0+2, x, y/2.0+2, fill="black")
         self.w.create_line(x/2.0+1,4,x/2.0+1,y,fill="black")

         self.oval_coord={'AC':[6,9,x/2.0-3,y/2.0-3],'AD':[x/2.0+3,9,x-3,y/2.0-3],
                 'BC':[6,y/2.0+5,x/2.0-3,y-3],'BD':[x/2.0+3,y/2.0+5,x-3,y-3]}
         self.rect_coord=[20,matrixCorn_y-75,450,300]
         Proxy.rect_coord=self.rect_coord


      else:
         self.w.create_rectangle(3,4,x,y)
         self.w.create_line(3,y/3.0,x,y/3.0,fill="black")

         
         self.w.create_line(x/3.0,4,x/3.0,y,fill="black")
         self.w.create_line(x*(2/3.0),4,x*(2/3.0),y,fill="black")
         self.w.create_line(3,y*(2/3.0),x,y*(2/3.0),fill="black")
         # self.w.create_line(x,0,x,y,fill="black")
         self.oval_coord={'AD':[3+ovsz,6+ovsz,x/3.0-ovsz,y/3.0-ovsz],'AE':[x/3.0+ovsz,6+ovsz,x*(2.0/3.0)-ovsz,y/3.0-ovsz],
                          'AF':[x*(2.0/3.0)+ovsz,6+ovsz,x-ovsz,y/3.0-ovsz],'BD':[3+ovsz,y/3.0+ovsz,x/3.0-ovsz,y*2.0/3.0-ovsz],
                          'BE':[x/3.0+ovsz,y/3.0+ovsz,x*2.0/3.0-ovsz,y*2.0/3.0-ovsz],'BF':[x*2.0/3.0+ovsz,y/3.0+ovsz,x-ovsz,y*2.0/3.0-ovsz],
                          'CD':[3+ovsz,y*2.0/3.0+ovsz,x/3.0-ovsz,y-ovsz],'CE':[x/3.0+ovsz,y*2.0/3.0+ovsz,x*2.0/3.0-ovsz,y-ovsz],
                          'CF':[x*2.0/3.0+ovsz,y*2.0/3.0+ovsz,x-ovsz,y-ovsz]}
         self.rect_coord=[15,matrixCorn_y-65,510,310]
         Proxy.rect_coord=self.rect_coord

      lens={}#length of payoff digits for aligning horizontally
      if A[0] == 2:
         UL_0 = "%d" % M[0][0][0]
         DL_0 = "%d" % M[0][1][0]
         UR_0 = "%d" % M[1][0][0]
         DR_0 = "%d" % M[1][1][0]
         UL_1 = "%d" % M[0][0][1]
         DL_1 = "%d" % M[0][1][1]
         UR_1 = "%d" % M[1][0][1]
         DR_1 = "%d" % M[1][1][1]

         for i in [UL_0,DL_0,UR_0,DR_0,UL_1,DL_1,UR_1,DR_1]:
            lens[i]=len(i)
      else:
         UL_0 = "%d" % M[0][0][0]
         ML_0 = "%d" % M[0][1][0]
         DL_0 = "%d" % M[0][2][0]
         UM_0 = "%d" % M[1][0][0]
         MM_0 = "%d" % M[1][1][0]
         DM_0 = "%d" % M[1][2][0]
         UR_0 = "%d" % M[2][0][0]
         MR_0 = "%d" % M[2][1][0]
         DR_0 = "%d" % M[2][2][0]
         UL_1 = "%d" % M[0][0][1]
         ML_1 = "%d" % M[0][1][1]
         DL_1 = "%d" % M[0][2][1]
         UM_1 = "%d" % M[1][0][1]
         MM_1 = "%d" % M[1][1][1]
         DM_1 = "%d" % M[1][2][1]
         UR_1 = "%d" % M[2][0][1]
         MR_1 = "%d" % M[2][1][1]
         DR_1 = "%d" % M[2][2][1]

         for j in [UL_0,ML_0,DL_0,UM_0,MM_0,DM_0,UR_0,MR_0,DR_0,UL_1,ML_1,DL_1,UM_1,MM_1,DM_1,UR_1,MR_1,DR_1]:
            lens[j]=len(j)

      if A[0] ==2:

         if self.player%2 ==0:#lazy code + bad code
            fontH16 = tkFont.Font(family="Helvetica", size=24,weight='bold')
            tune_x1=75#1 additive,change this move player 0's payoffs inward(with less) and outward with more
            tune_x2=30
            rate=7#2 multiplicative,each digits takes up this much pixels
            tune_y=13
         else:
            tune_x1=80
            tune_x2=25
            rate=5
            tune_y=9

         self.w.create_text(x/2.0- tune_x1- rate*lens[UL_0], (y/2.0)/2-tune_y+3,text = UL_0,anchor="nw", font=fontH16, fill=self.p1col)
         self.w.create_text(x/2.0- tune_x1- rate*lens[DL_0], (y*(1/2.0)+y)/2.0 - tune_y ,text = DL_0,anchor="nw", font=fontH16, fill=self.p1col)
         self.w.create_text(x/2.0+ tune_x2- rate*lens[UR_0] ,(y/2.0)/2- tune_y+3 ,text = UR_0,anchor="nw", font=fontH16, fill=self.p1col)
         self.w.create_text(x/2.0+ tune_x2- rate*lens[DR_0] ,(y*(1/2.0)+y)/2.0-tune_y ,text = DR_0,anchor="nw", font=fontH16, fill=self.p1col)

         if self.player%2 != 0:
            fontH160 = tkFont.Font(family="Helvetica", size=24,weight='bold')
            tune_x1=25
            tune_x2=70
            rate=7
            tune_y=13 
         else:
            fontH160 = tkFont.Font(family="Helvetica", size=16,weight='normal')
            tune_x1=25
            tune_x2=85
            rate=5
            tune_y=9

         self.w.create_text(x/2.0- tune_x1- rate*lens[UL_1] ,(y/2.0)/2-tune_y+3,text = UL_1,anchor="nw", font=fontH160, fill=self.p2col)
         self.w.create_text(x/2.0- tune_x1- rate*lens[DL_1] ,(y*(1/2.0)+y)/2.0 - tune_y ,text = DL_1,anchor="nw", font=fontH160, fill=self.p2col)
         self.w.create_text(x/2.0+ tune_x2- rate*lens[UR_1] ,(y/2.0)/2- tune_y+3 ,text = UR_1,anchor="nw", font=fontH160, fill=self.p2col)
         self.w.create_text(x/2.0+ tune_x2- rate*lens[DR_1] ,(y*(1/2.0)+y)/2.0- tune_y ,text = DR_1,anchor="nw", font=fontH160, fill=self.p2col)

      else:
         if self.player%2 ==0:#lazy code + bad code
            fontH16 = tkFont.Font(family="Helvetica", size=24,weight='bold')
            tune_x1=75#1 additive,change this move player 0's payoffs inward(with less) and outward with more
            rate=7#2 multiplicative,each digits takes up this much pixels
            tune_y=13
         else:
            tune_x1=80#the same effect as #1
            rate=5#the same as #2
            tune_y=9


         self.w.create_text(x/3.0-tune_x1-rate*lens[UL_0] ,(y/3.0)/2- tune_y+3 ,text = UL_0,anchor="nw", font=fontH16, fill=self.p1col)
         self.w.create_text(x/3.0- tune_x1-rate*lens[ML_0] ,(y*(2/3.0)+y/3.0)/2.0- tune_y ,text = ML_0,anchor="nw", font=fontH16, fill=self.p1col)
         self.w.create_text(x/3.0- tune_x1-rate*lens[DL_0] ,(y*(2/3.0)+y)/2.0- tune_y ,text = DL_0,anchor="nw", font=fontH16, fill=self.p1col)
         self.w.create_text(x*(2/3.0)- tune_x1-rate*lens[UM_0] ,(y/3.0)/2- tune_y +3,text = UM_0,anchor="nw", font=fontH16, fill=self.p1col)
         self.w.create_text(x*(2/3.0)- tune_x1-rate*lens[MM_0] ,(y*(2/3.0)+y/3.0)/2.0- tune_y ,text = MM_0,anchor="nw", font=fontH16, fill=self.p1col)
         self.w.create_text(x*(2/3.0)- tune_x1-rate*lens[DM_0] ,(y*(2/3.0)+y)/2.0- tune_y ,text = DM_0,anchor="nw", font=fontH16, fill=self.p1col)
         self.w.create_text(x- tune_x1-rate*lens[UR_0] ,(y/3.0)/2- tune_y +3,text = UR_0,anchor="nw", font=fontH16, fill=self.p1col)
         self.w.create_text(x- tune_x1-rate*lens[MR_0] ,(y*(2/3.0)+y/3.0)/2.0- tune_y ,text = MR_0,anchor="nw", font=fontH16, fill=self.p1col)
         self.w.create_text(x- tune_x1-rate*lens[DR_0] ,(y*(2/3.0)+y)/2.0- tune_y ,text = DR_0,anchor="nw", font=fontH16, fill=self.p1col)

         if self.player%2 != 0:#lazy code + bad code
            fontH161 = tkFont.Font(family="Helvetica", size=24,weight='bold')
            tune_x1=30#the same effect as #1
            rate=7#the same as #2
            tune_y=13
         else:
            fontH161 = tkFont.Font(family="Helvetica", size=16,weight='normal')
            tune_x1=25#the same effect as #1
            rate=5#the same as #2
            tune_y=9



         self.w.create_text(x/3.0-tune_x1-rate*lens[UL_1],(y/3.0)/2-tune_y+3,text = UL_1,anchor="nw", font=fontH161, fill=self.p2col)
         self.w.create_text(x/3.0-tune_x1-rate*lens[ML_1],(y*(2/3.0)+y/3.0)/2.0-tune_y,text = ML_1,anchor="nw", font=fontH161, fill=self.p2col)
         self.w.create_text(x/3.0-tune_x1-rate*lens[DL_1],(y*(2/3.0)+y)/2.0-tune_y,text = DL_1,anchor="nw", font=fontH161, fill=self.p2col)
         self.w.create_text(x*(2/3.0)-tune_x1-rate*lens[UM_1],(y/3.0)/2-tune_y+3,text = UM_1,anchor="nw", font=fontH161, fill=self.p2col)
         self.w.create_text(x*(2/3.0)-tune_x1-rate*lens[MM_1],(y*(2/3.0)+y/3.0)/2.0-tune_y,text = MM_1,anchor="nw", font=fontH161, fill=self.p2col)
         self.w.create_text(x*(2/3.0)-tune_x1-rate*lens[DM_1],(y*(2/3.0)+y)/2.0-tune_y,text = DM_1,anchor="nw", font=fontH161, fill=self.p2col)
         self.w.create_text(x-tune_x1-rate*lens[UR_1],(y/3.0)/2-tune_y+3,text = UR_1,anchor="nw", font=fontH161, fill=self.p2col)
         self.w.create_text(x-tune_x1-rate*lens[MR_1],(y*(2/3.0)+y/3.0)/2.0-tune_y,text = MR_1,anchor="nw", font=fontH161, fill=self.p2col)
         self.w.create_text(x-tune_x1-rate*lens[DR_1],(y*(2/3.0)+y)/2.0-tune_y,text = DR_1,anchor="nw", font=fontH161, fill=self.p2col)

      fontH16 = tkFont.Font(family="Helvetica", size=16,weight='normal')#reseting the font so doesn't affect if used anywhere below

      if A[0] == 2:

         self.w.place(x=matrixCorn_x,y=matrixCorn_y)
      else:

         self.w.place(x=matrixCorn_x,y=matrixCorn_y)
         
      if self.talk_buttons ==None:
         ##status and rounds
         txt,h,w=to_write(["Choose an action ..."])
         write(talk_display,txt,0,h+1,w,self.player%2,True) 

         self.rounds=1
         
         self.timestamp1=datetime.datetime.now() #all this block is for data logging only
         log_name=self.timestamp1.strftime("%Y-%m-%d %H:%M:%S")
         header=['round','game','ur_ID','player',"round init",'your action',"action sent",'your pay','your avg',"your earning",'his action',"action received",
                 "his pay","his_avg"]

      else:
         map((lambda but: but.place_forget()), self.buttons)#default set buttons to invisible

         log_name=talk_buttons.timestamp1.strftime("%Y-%m-%d %H:%M:%S")
         header=['round','game','ur_ID','player',"round init","your talk","talk sent",'his talk',
                 'talk received','your action',"action sent",'your pay','your avg',"your earning",'his action',"action received",
                 "his pay","his_avg"]
      self.timestamp4=-1
      self.timestamp5=-1

      self.log=open(log_name+'.csv', 'w')
      self.logger=csv.writer(self.log)
      self.logger.writerow(header)#until here

      self.is_enable=False


      if A[0] == 2:
         if self.player%2==0:
            self.P1_A1.bind('<Button-1>', lambda event,x="A": self._button_click(x))
            self.P1_A2.bind('<Button-1>', lambda event,x="B": self._button_click(x))
         else:
            self.P2_A1.bind('<Button-1>', lambda event,x="C": self._button_click(x))
            self.P2_A2.bind('<Button-1>', lambda event,x="D": self._button_click(x))
      else:
         if self.player%2==0:
            self.P1_A1.bind('<Button-1>', lambda event,x="A": self._button_click(x))
            self.P1_A2.bind('<Button-1>', lambda event,x="B": self._button_click(x))
            self.P1_A3.bind('<Button-1>', lambda event,x="C": self._button_click(x))
         else: 
            self.P2_A1.bind('<Button-1>', lambda event,x="D": self._button_click(x))
            self.P2_A2.bind('<Button-1>', lambda event,x="E": self._button_click(x))
            self.P2_A3.bind('<Button-1>', lambda event,x="F": self._button_click(x))



   def binding(self,buts):
      for i in buts:
         if i['state'] == "disabled":
            return False
      return True
      
   def _button_click(self,mark):
      if self.binding(self.buttons):
         self.w.delete('oval')#this is for without cheaptalk, not a redundant
         if A[0] == 2:
            if self.player%2 == 0:
               if mark =="A":
                  self.P1_A2.configure(state="disabled")
                  V=0
               else:
                  self.P1_A1.configure(state="disabled")
                  V=1   
            else:
               if mark =="C":
                  V=0
                  self.P2_A2.configure(state="disabled")
               else:
                  V=1
                  self.P2_A1.configure(state="disabled")

         else:
            if self.player%2 == 0:
               if mark =="A":
                  V=0
                  map((lambda child: child.configure(state="disabled")), [self.P1_A2,self.P1_A3])
                  
               elif mark =="B":
                  V=1
                  map((lambda child: child.configure(state="disabled")), [self.P1_A1,self.P1_A3])
               else:
                  V=2
                  map((lambda child: child.configure(state="disabled")), [self.P1_A1,self.P1_A2])
            else:
               if mark == "D":
                  V=0
                  map((lambda child: child.configure(state="disabled")), [self.P2_A2,self.P2_A3])
               elif mark=="E":
                  V=1
                  map((lambda child: child.configure(state="disabled")), [self.P2_A1,self.P2_A3])
               else:
                  V=2
                  map((lambda child: child.configure(state="disabled")), [self.P2_A1,self.P2_A2])
         # if self.talk_buttons == None:
         #    txt,h,w=to_write(["   Waiting for your partner's action ..."])
         #    write(talk_display,txt,0,h+1,w,self.player%2,True) 
            # self.status.config(text="Waiting for your opponent's action ...")

         Status.text1.destroy()
         Status.text2.destroy()
         txt,h,w=to_write(["   Waiting for your partner's action ..."])
         write(talk_display,txt,0,h+1,w,self.player%2,True) 
            # gray_out([self.talk_buttons.C2.C1_DM,self.talk_buttons.C2.C2_DM,self.talk_buttons.C2.C3_DM,self.talk_buttons.C2.C4_DM],"disabled")
            # map((lambda child: child.configure(state="disabled")), self.talk_buttons.chks)
            # self.talk_buttons.status.config(text="Waiting for your opponent's action ...")
         print "I should run first"

         if self.talk_buttons ==None:
            stamp=self.timestamp1
         else:
            obj=self.talk_buttons
            stamp=self.talk_buttons.timestamp3
         print "I made it"  
         self.timestamp4=datetime.datetime.now() 

         dish=str(V)+" $"     
         dish+=" %.2f"% datetime.timedelta.total_seconds(self.timestamp4-stamp)#commentout to enable        
         self.sock.send(dish)
         print "sending: ", V
         

   def action(self,V):


      if self.talk_buttons ==None:#which timestamp1 to use, of talk_button or game
         obj=self
      else:
         obj=self.talk_buttons
      print "before receiving the action ......."
      observation=self.sock.recv(1024)
      print "action received: "+"$"*15
      print observation

      Status.text1.destroy()
      Status.text2.destroy()      

      self.timestamp5=datetime.datetime.now()
      #resetting the timestamp1      
      obj.timestamp1=self.timestamp5 
      
      if self.talk_buttons == None:#without cheaptalk, logging and status are different
         analyze_action(observation,M,talk_display,self.player,obj.rounds,self,A,self.w,self.oval_coord,False)

         txt,h,w=to_write(["Choose an action ..."])
         write(talk_display,txt,0,h+1,w,self.player%2,True)  
      else:
         analyze_action(observation,M,talk_display,self.player,obj.rounds,self,A,self.w,self.oval_coord)

         txt,h,w=to_write(["   Send chat ..."])
         write(talk_display,txt,0,h,w,self.player%2,True)       
      

      if self.talk_buttons!=None:#w/o resetting speech buttons and graying out them
         map((lambda var: var.set(0)), self.talk_buttons.C2.vars)
         map((lambda var: var.set(0)), self.talk_buttons.DM_labels)

         gray_out([self.talk_buttons.C2.C1_DM,self.talk_buttons.C2.C2_DM,self.talk_buttons.C2.C3_DM,self.talk_buttons.C2.C4_DM],"normal")
         map((lambda child: child.configure(state="normal")), self.talk_buttons.chks)
         map((lambda var: var.set("...")), self.talk_buttons.DM_vars)


         if self.talk_buttons.rounds == self.iters:#if it reaches game# disable send button close services, not window
            #send group_agent and avg to server
            CloseEvents.closeOk=True

            self.talk_buttons.submit.configure(state="disabled")
            self.talk_buttons.submit.place_forget()
            
            Status.text1.destroy()
            Status.text2.destroy()
            self.whole.delete("game_rect")
            
            txt,h,w=to_write(["Game over!"])
            write(talk_display,txt,0,h+1,w,self.player%2,True)
            
            txt,h,w=to_write(["     "])#sapce after "Game over"
            write(talk_display,txt,0,3,w,self.player%2,True)

            txt,h,w=to_write(["Ranking         ID         Score"])#header
            write(talk_display,txt,0,h+1,w,self.player%2)

            reports=self.sock.recv(1024)#receiving rankings from server.
            len_dosh=len(reports)
            if len_dosh == len(reports.rstrip('$')):
               print "Warning: score reports from server don't match the format."
            else:
               reports=reports.rstrip('$')
            items=reports.split(';')
            rows=[]
            for i in items:
               ID_score=i.split()
               if len(ID_score) != 0:
                  rows.append(ID_score)       
            print "woohoo, you are on the high list: ", rows
            for i in ranking.rank(rows):#rows ranked and preapred for showing
               if i.split()[1] == self.group_agent:#your own highlighted with your theme color
                  i="You   "+i+" "*6
                  txt,h,w=to_write([i])
                  write(talk_display,txt,0,h,w,self.player%2,False,self.ur_color)  
               else:             
                  txt,h,w=to_write([i])
                  write(talk_display,txt,0,h,w,self.player%2)

            self.log.close()
            self.sock.close()
            # t1=Thread(target=self.sleeper)#in case of need for self shut down
            # t1.start()

         else:#moving the rects and counting roujnds
            self.talk_buttons.rounds+=1
            # self.talk_buttons.written=False
            self.talk_buttons.submit.place(self.talk_buttons.submit_loc)
            self.talk_buttons.submit.configure(state="normal")
            self.whole.delete("game_rect")
            self.talk_buttons.whole3.create_rectangle(665,353,1070,680,outline='red',tags="talk_rect")
         
      else:#without talk, do the same thing
         if obj.rounds == self.iters:
            CloseEvents.closeOk=True
            Status.text1.destroy()
            Status.text2.destroy()
            txt,h,w=to_write(["Game over!"])
            write(talk_display,txt,0,h+1,w,self.player%2,True)

            map((lambda child: child.configure(state="disabled")), self.buttons)

            txt,h,w=to_write(["     "])#sapce after "Game over"
            write(talk_display,txt,0,3,w,self.player%2,True)

            txt,h,w=to_write(["Ranking         ID         Score"])#header
            write(talk_display,txt,0,h+1,w,self.player%2)

            reports=self.sock.recv(1024)#receiving rankings from server.
            len_dosh=len(reports)
            if len_dosh == len(reports.rstrip('$')):
               print "Warning: score reports from server don't match the format."
            else:
               reports=reports.rstrip('$')
            items=reports.split(';')
            rows=[]
            for i in items:
               ID_score=i.split()
               if len(ID_score) != 0:
                  rows.append(ID_score)       
            print "woohoo, you are on the high list: ", rows
            for i in ranking.rank(rows):#rows ranked and preapred for showing
               if i.split()[1] == self.group_agent:#your own highlighted with your theme color
                  i="You   "+i+" "*6
                  txt,h,w=to_write([i])
                  write(talk_display,txt,0,h,w,self.player%2,False,self.ur_color)  
               else:             
                  txt,h,w=to_write([i])
                  write(talk_display,txt,0,h,w,self.player%2)
                  
            self.log.close()
            self.sock.close()
         else:
            obj.rounds+=1
            map((lambda child: child.configure(state="normal")), self.buttons)
            
      obj.timestamp1=datetime.datetime.now()#round initiation time stamp           
   
      
   def ShowChoice(self,V):
      # if self.binding(self.buttons):
      # # if self.binding(self.buttons):
      self.is_enable=True
      if self.talk_buttons == None:
         pass
      else:
         print "I should run second"
         map((lambda child: child.configure(state="disabled")), self.buttons)
         for i in self.buttons:
            i.place_forget()
      self.V=V
      self.action(V)

# def leaderBoard():
#    call(['python', "Bla bla bla."])


   def sleeper(self):
      sleep(3)
      self.window.quit()

         # self.remaining-=1
         # self.after(1000, self.countdown)

        
      
def analyze_action(observation,M,display,player,rounds,obj,A,canvas,oval_coord,cheaptalk=True):
   '''analyzing actions and displaying payoffs on screen'''

   if not cheaptalk:
      rnd_txt="Current Round: %d" %rounds##log the round #
      txt,h,w=to_write([rnd_txt])
      write(display,txt,0,h,w)
   
   actos = observation.split(" ")

   a1 = int(actos[0])
   a2 = int(actos[1])
   if A[0] == 3:
      acts={(0,0):"A",(0,1):"B",(0,2):"C",(1,0):"D",(1,1):"E",(1,2):"F"}
   else:
      acts={(0,0):"A",(0,1):"B",(1,0):"C",(1,1):"D"}
   if player%2 ==0:
      act1=acts[(0,a1)]
      act2=acts[(1,a2)]

      ur_action="%s" % act1
      his_action="%s" % act2

      canvas.create_oval(*oval_coord[act1+act2],tags='oval')#circling the payouts
      
   elif player%2 ==1:
      act1=acts[(1,a2)]
      act2=acts[(0,a1)]

      ur_action="%s" % act1
      his_action="%s" % act2
      
      canvas.create_oval(*oval_coord[act2+act1],tags='oval')
      
   urs,h,w=to_write(["You chose: "+ur_action+" "])#extra space makes not attached to the scrollbar
   write(display,urs,11,h,w)
   his,h,w=to_write(["Your partner chose: "+his_action])
   write(display,his,22,h,w)
   if player%2==0:

      ur_pay="%d"  % M[a2][a1][0]
      his_pay="%d" % M[a2][a1][1]

      obj.mine+=M[a2][a1][0]
      obj.his+=M[a2][a1][1]

   elif player%2 ==1:

      ur_pay="%d" % M[a2][a1][1]
      his_pay="%d"  % M[a2][a1][0]
      obj.mine+=M[a2][a1][1]
      obj.his+=M[a2][a1][0]
   else:
      print "Error: unknown player ID"
      
   ur_p,h,w=to_write(["Your payout: "+ur_pay+" "])#extra space makes not attached to the scrollbar
   write(display,ur_p,11,h+1,w)
   his_p,h,w=to_write(["Your partner's payout: "+his_pay])
   write(display,his_p,22,h+1,w)
   
   write(display,"-"*37,11,1,37)##separator lines
   write(display,"-"*37,22,1,37)
   

   
   # obj.avg.config(state="normal")   
   # obj.avg.delete(1.0, END)

   ur_avg="%.2f" %(obj.mine/rounds)
   his_avg="%.2f" %(obj.his/rounds)

   obj.avg.config(text=ur_avg)
   # obj.avg['text']="5.5555"
   # obj.avg.insert(END,ur_avg)
   # obj.avg.config(state="disabled")

   # obj.earn.config(state="normal")   
   # obj.earn.delete(1.0, END)
   if obj.gamename == "chicken2":
      e_rate = 0.139
   elif obj.gamename == "blocks2":
      e_rate = 0.167
   elif obj.gamename == "prisoners":
      e_rate = 0.194
   else:
      print "You are playing game: ", obj.gamename,"the default rate is used: ", 3.5
      # print "*"*20,"-"*20, "the default rate is used: ", 3.5
      e_rate = 3.5


   # ern="%.2f" % (float(obj.avg["text"])*e_rate)
   print "this is what you have: ",obj.earn['text']
   print "now i'm earning: ", (int(ur_pay)*e_rate)/obj.iters
   ern="%.2f" % (float(obj.earn['text'])+ (int(ur_pay)*e_rate)/obj.iters)
   obj.earn.config(text=ern)
   # his_earn="%.2f" % float(his_avg)*rounds*0.4
   # obj.earn.insert(END,"%.2f" % ern)
   # obj.earn.config(state="disabled")

   ##this block is for logging only
   if not cheaptalk:
      row=[str(rounds),obj.gamename,obj.group_agent,str(player),obj.timestamp1.strftime("%H:%M:%S.%f"),ur_action,obj.timestamp4.strftime("%H:%M:%S.%f"),
            ur_pay,ur_avg,ern+" AED",his_action,obj.timestamp5.strftime("%H:%M:%S.%f"),his_pay,his_avg]
   else:
      row=[str(rounds),obj.gamename,obj.group_agent,str(player),obj.talk_buttons.timestamp1.strftime("%H:%M:%S.%f"),obj.talk_buttons.ur_talk,
           obj.talk_buttons.timestamp2.strftime("%H:%M:%S.%f"),obj.talk_buttons.his_talk,obj.talk_buttons.timestamp3.strftime("%H:%M:%S.%f"),
           ur_action,obj.timestamp4.strftime("%H:%M:%S.%f"),ur_pay,ur_avg,ern+" AED",his_action,obj.timestamp5.strftime("%H:%M:%S.%f"),his_pay,his_avg]
   obj.logger.writerow(row)
      
   

   
def readPayoffMatrixFromFile(gamename):
   '''Class game is auto configured according to the reading from specification here.
   This outputs M as matrix payoff, A as actions'''
   
   filename = "games/"+gamename+".txt"
   f = open(filename, 'r')
   whole = f.read()
   f.close()
   #print whole

   mylist = whole.split("\n")
   numAgents = int(mylist[0])
   num1 = int(mylist[1])
   num2 = int(mylist[2])
   A = [num1, num2]

   M = []##*Only the Prof knows what this does, haha
   count = 3
   for i in range(0, A[0]):
      row = []
      for j in range(0, A[1]):
         entry = mylist[count].split("\t")

         row.append([float(entry[0])*100,float(entry[1])*100])
         #row.append((float('%.2f' % float(entry[0])),float('%.2f' % float(entry[1]))))
         count = count + 1
    
      M.append(row)


   return M, A
   
def handler():
   if CloseEvents().closeOk:
      window.quit()
   else:
      if tkMessageBox.askokcancel("Quit?", "You haven't finished the game, are you sure you want to quit?"):
         window.quit()
      
if __name__ == '__main__':

##   if (len(sys.argv) < 5):
##      print "Not enough arguments"
##      exit(1)

   gamename = sys.argv[1]
##   gamename = "rcg_2x3_0"
   iters = int(sys.argv[2])
   GAP=sys.argv[3].split()#G=group,A=agent,P=port
   if len(GAP)>1:
      GA,port=GAP
   else:
      GA=None
      port=GAP[0]
   me = int(port)
   if sys.argv[4] =='0':
      cheaptalk=False
   else:
      cheaptalk=True

   if len(sys.argv) >5:
      hostname=sys.argv[5]
      if hostname == 'localhost':
         pass
      elif len(hostname.split('.'))!=4:
         print "You entered an invalid IP address."
         print hostname
         sys.exit()
   else:
      hostname = "localhost"#sys.argv[4]

   ##socket connection (the following lines are active when we want a socket)
   sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   server_address = (hostname, 3000+me)
   sock.connect(server_address)
   sock.send(GA)
   goMessage = sock.recv(1024)
   print "first msg: ", goMessage

   M, A = readPayoffMatrixFromFile(gamename)

   ##creating a window, plain window
   window = Tk()
   # window.attributes("-alpha",0.5)
   window.resizable(width=FALSE, height=FALSE)
   x=1100
   if cheaptalk:
      y=690
   else:
      y=355
   window.geometry("%dx%d" %(x,y))

   window.protocol("WM_DELETE_WINDOW", handler)#catches the closes and reminding if rounds not met

   root_canv=Canvas(window,width=x,height=y)
   root_canv.place(x=0,y=0)
   root_canv.create_rectangle(556,15,1095,330)
   
   
   talk_display=speech_log(window)
##   talk_display.grid(row=0,column=7,rowspan=8,columnspan=2,sticky=NSEW)
   talk_display.place(x=557,y=16)

   speech_frame=Frame(window)


   if cheaptalk:
      talk_buttons=speech_button(window,root_canv,talk_display,me,A,sock)
      game(window,M,A,talk_display,talk_buttons,me,iters,gamename,GA,sock)
   else:
      game(window,M,A,talk_display,None,me,iters,gamename,GA,sock)

   window.mainloop()



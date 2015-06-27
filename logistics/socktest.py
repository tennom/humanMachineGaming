
'''
    Simple socket server using threads
'''
 
import socket
import sys
from thread import *
from time import sleep
import os

from logistics import logistics as lg



if os.path.exists(os.environ["HOME"]+"/Desktop/logs/servers"):
    pass
else:
    os.makedirs(os.environ["HOME"]+"/Desktop/logs/servers")

 
HOST = '0.0.0.0'   # Symbolic name meaning all available interfaces
PORT = 1234 # Arbitrary non-privileged port
# group = 'R'
 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'
 
#Bind socket to local host and port
try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
     
print 'Socket bind complete'
 
#Start listening on socket
s.listen(10)
print 'Socket now listening'
game_human,register=lg()               
# print game_human
C_msgs={"c1":"is WAITING for partner ...","c2":"is WAITING for server ..."}
#following 3 lines is for testing 2 players on on two servers.
# game_human={'1 1': '1 0','1 2':'1 1','2 1': '2 3','2 2':'2 2','3 1':'1 4','3 2':'1 5','4 1':'2 7','4 2':'2 6'}
# register={"1 0":{"1 0":False,"2 1":False},"2 1":{"1 0":False,"2 1":False},"1 3":{"1 3":False,"2 2":False},"2 2":{"1 3":False,"2 2":False},
#           "1 4":{'1 4':False,'2 5':False},"2 5":{'1 4':False,'2 5':False},"1 7":{"1 7":False,"2 6":False},"2 6":{"1 7":False,"2 6":False}}


def check_server(serverID):
    if not os.access(os.environ["HOME"]+"/Desktop/logs/servers/%s.txt" % serverID,os.R_OK):
        creat_f=open(os.environ["HOME"]+"/Desktop/logs/servers/%s.txt" % serverID,'w')#creating one
        creat_f.write("no")#so that first line is readable, otherwise it raises error and crashes
        creat_f.close()

    s_file=os.environ['HOME']+"/Desktop/logs/servers/%s.txt" % serverID
    with open(s_file,'r') as f:
        first_line=f.readline()
    return first_line[0]
def stop_server(serverID,h,game):
    '''this is only for crash recovery
    1. upon receiving traping signals, unregister the clients so they can resume the game.
    2. it makes server to rerun the crashed game
    3. this feature is not for my user study, so I comment out.'''

    change=True#server is reseted only once

    # sp=game_human[game+' '+h]#unregister from the logistics
    # s,p=sp.split()
    # for i in register[h+' '+p].keys():#bad code
    #     if register[h+' '+p][i]==False:
    #         change=False
    #         break
    #     else:
    #         register[h+' '+p][i]=False
    #         if i != h+' '+p:
    #             other=i
    # if change:
    #     for j in register[other].keys():
    #         register[other][j]=False
        #crash recovery, initial effort
        # s_file=os.environ['HOME']+"/Desktop/logs/servers/%s.txt" % serverID#restoring the server to the last playing game
        # f1=open(s_file,'r')
        # first_line=f1.readline()
        # print "this is first line +++++++++++++++++++++++++++++++++++++++++++++++++++++",first_line
        # f1.close()
        # f2=open(s_file,'w')
        # f2.write(str(int(first_line[0])-1))
        # f2.close()
        # crash_file=os.environ['HOME']+"/Desktop/logs/servers/crash%s.txt" % serverID
        # f3=open(crash_file,'w')
        # f3.write("100")
        # f3.close()


#Function for handling connections. This will be used to create threads
def clientthread(conn,addr):
    #Sending message to connected client
    conn.send('welcome') #send only takes string
    
    g_h=conn.recv(1024)

    if not g_h:
    	print addr,"dead, closing the socket ..."
    	conn.close()
    else:
        bundle=g_h.split()
        if len(bundle) == 1:
            dish=read_rows(bundle[0]) #read server report log 
            conn.send(str(dish))

            conn.close()
            return
        else:
            pass

        if len(bundle) ==3:
            g,h,s=g_h.split()
            stop_server(s,h,g)
            conn.close()
            return
        elif len(bundle) == 4: #updates the rankings, not implemented
            pass

        else:
            g,h=g_h.split()

            print "You are %s and playing game %s." %(h,g)
            conn.send(game_human[g_h])#allocating a server and a port

            h_p_s = conn.recv(1024)
            if not h_p_s:
                print "You failed to send me h,p,s"
                conn.close()
                return
            else:

                h,p,s=h_p_s.split()#
                register[h+' '+p][h+' '+p]=True
                for i in register[h+' '+p].keys():#not a good method due to register is bad practice.
                    if i != h+' '+p:
                        register[i][h+' '+p]=True

                print h_p_s,"is registered."

                conn.send("s1")
                s1_r=conn.recv(1024)
                if not s1_r:
                    print h,"failed to send back OK for waiting partner."
                    conn.close()
                    return 
                if s1_r == "c1":
                    print h, C_msgs[s1_r]
                else:
                    print "Error: ",s1_r
                    if conn:
                        conn.close()
                    return
           
                pair=register[h+' '+p].keys()
                reply=False
                while not reply:
                    if register[h+' '+p][pair[0]] and register[h+' '+p][pair[1]]:
                        reply=True
                    else:
                        sleep(1.5)

                fail_ok2=False
                #Checking the server status
                if g != check_server(s):
                    ready = False
                    conn.sendall("s2")
                    s_c2=conn.recv(1024)
                    if not s_c2:
                        print h,"failed to send ok for waiting server"
                        fail_ok2=True
                        conn.close()
                        return
                    if s_c2 == 'c2':
                        print h,C_msgs['c2']
                    else:
                        print "Error: OK 2"
                        if conn:
                            conn.close()
                        return
                else:
                    ready=True

                if fail_ok2:#if the client failed to send Ok2, then stop continuing, else error propgates
                    return

                while not ready:
                    if g == check_server(s):#see if the game you want to play is available on the server
                        ready=True
                    else:
                        sleep(1.5)

                if int(p) %2 != 0 :#because even port connects first to game server
                    print "odd port ***************"
                    sleep(1.5)

                conn.sendall("go")
                conn.close()
 
#now keep talking with the client
while 1:
    #wait to accept a connection - blocking call
    conn, addr = s.accept()
    print 'Connected with ' + addr[0] + ':' + str(addr[1])
     
    #start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
    start_new_thread(clientthread ,(conn,addr))
 
s.close()

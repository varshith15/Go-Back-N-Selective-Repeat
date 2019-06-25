#!/usr/bin/python -tt
from socket import *
import argparse
import threading
import time

parser = argparse.ArgumentParser()
parser.add_argument("-d",type=bool)
parser.add_argument("-s",type=str)
parser.add_argument("-p",type=int)
parser.add_argument("-l",type=int)
parser.add_argument("-r",type=int)
parser.add_argument("-n",type=int)
parser.add_argument("-w",type=int)
parser.add_argument("-b",type=int)
    
args = parser.parse_args()

clientSocket = socket(AF_INET, SOCK_DGRAM)
serverName = args.s
serverPort = args.p
paclen = args.l
pacrate = args.r
maxpac = args.n
winsize = args.w
bufsize = args.b
boolwin = [False]*winsize
windata = [""]*winsize
bufferstr = []
pactime = [0]*winsize
numresend = [0]*winsize
buff = 0
seqno = 0
seqno1 = 0
exp = 0
succ = 0
total=0
timeout = 1
terminate = 1
avgrtt = 0
start = 0
debug = args.d
pactimelock = threading.Lock()
buflock = threading.Lock()
bufflock = threading.Lock()




def pacgen():
	global seqno
	global buff
	global bufferstr
	while terminate:	
		for j in range(pacrate):
			s = ""
			for  i in range(paclen):
				s = s + 'a'
			s = s + ' ' + str(seqno)
			buflock.acquire()
			if buff<bufsize:
				seqno = seqno + 1
				bufferstr.append(s)
				buff = buff + 1
			buflock.release()
		time.sleep(1)
		
		
		
def resend():
	global terminate
	global numresend
	global timeout
	global total
	#time.sleep(2)
	while terminate:
		while start and terminate:	
			pactimelock.acquire()
			if exp<10:
				timeout=2
			else:
				#timeout = 2*avgrtt/succ
				timeout=2
			#print(timeout)
			if (not boolwin[exp%winsize]) and (time.time() - pactime[exp%winsize]>timeout):
				#print(exp, boolwin[exp%winsize], time.time() - pactime[exp%winsize], timeout)
				for i in range(exp,exp+winsize):
					numresend[(i)%winsize] = numresend[(i)%winsize]+1
					if numresend[(i)%winsize]==5:
						print("resending", i+exp ,"more than 5 times so terminating")
						terminate = 0
					message = windata[(i)%winsize]
					clientSocket.sendto(message.encode(),(serverName, serverPort))
					total = total+1
					a,b = message.split(" ")
					#print("resend", b,time.time())
					pactime[(i)%winsize]=time.time()
				pactimelock.release()
			else:
				pactimelock.release()
		
				
				
def rec():
	global terminate
	global timeout
	global seqno1
	global exp
	global succ
	global avgrtt
	global numresend
	global boolwin
	while terminate:
		ack, serverAddress = clientSocket.recvfrom(2048)
		ack = int(ack)
		if ack == exp:
			succ = succ +1
			if succ==maxpac:
				terminate = 0
			if debug:
				print("Seq No:",ack, "Time Recieved:", time.time(), "RTT:", time.time()-pactime[ack%winsize], "Number of attempts:", numresend[ack%winsize]+1)
			numresend[ack%winsize]=0
			boolwin[ack%winsize]=True
			#print("ack" , ack,boolwin[ack%winsize],time.time()-pactime[ack%winsize])
			avgrtt = avgrtt + time.time()-pactime[ack%winsize]
			#print(avgrtt)
			exp = exp+1
			



pacgent = threading.Thread(target=pacgen,args=())
pacgent.setDaemon(True)
resendt = threading.Thread(target=resend,args=())
resendt.setDaemon(True)
rect = threading.Thread(target=rec,args=())
rect.setDaemon(True)

			
pacgent.start()
resendt.start()
rect.start()


while terminate:
	while seqno1<exp+winsize and terminate:
		if buff>0:	
			bufflock.acquire()
			data = bufferstr[0]
			buff = buff-1
			del bufferstr[0]
			bufflock.release()
			windata[seqno1%winsize]=data
			clientSocket.sendto(data.encode(),(serverName, serverPort))
			total = total+1
			a,b = data.split(" ")
			#print("send",b,time.time())
			pactimelock.acquire()
			pactime[seqno1%winsize]=time.time()
			pactimelock.release()
			boolwin[seqno1%winsize]=False
			seqno1 = seqno1 + 1
	start = 1
		
		
print("Packet Gen rate:", pacrate, "Packet Length:", paclen, "Retrasmission ratio:", total/succ, total,succ,"Average RTT:", avgrtt/succ)		
time.sleep(3)		
clientSocket.close()
		

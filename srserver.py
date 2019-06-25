"""from socket import *
serverPort = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))
print ('The server is ready to receive')
while 1:
	message, clientAddress = serverSocket.recvfrom(2048)
	modifiedMessage = message.upper()
	serverSocket.sendto(modifiedMessage, clientAddress)"""

#!/usr/bin/python -tt

from socket import *
import argparse
import threading
import time
import random

parser = argparse.ArgumentParser()
parser.add_argument("-d",type=bool)
parser.add_argument("-p",type=int)
parser.add_argument("-N",type=int)
parser.add_argument("-n",type=int)
parser.add_argument("-W",type=int)
parser.add_argument("-B",type=int)
parser.add_argument("-e",type=float)
    
args = parser.parse_args()

serverPort = args.p
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))
dp = args.e
maxpac=args.N
seqb = args.n	
debug = args.d
winsize = args.W
buffsize = args.B
srbuf=[]
buff=0

exp = 0

while 1:
	message, clientAddress = serverSocket.recvfrom(2048)
	t = time.time()
	a,b = message.decode().split(" ")
	b = int(b)
	if exp == b:
		if random.random()>=dp:
			#print("rec",exp)
			serverSocket.sendto(str(b).encode(), clientAddress)
			print("Seq No:", b, "Time recived:", t, "Packet Dropped: false")
			srbuf.append(b)
			for i in range(winsize):
				if (i+b) in srbuf:
					exp = exp+1
					srbuf.remove(i+b)
				else:
					break
			#print("accept", b,exp)
		else:
			#pass	
			print("Seq No:", b, "Time recived:", t, "Packet Dropped: true")
			#print(b)
	elif b>exp and b<exp+winsize:
		if random.random()>=dp:
			#print("rec",b)
			if buff<buffsize:
				buff = buff + 1
				srbuf.append(b)
				serverSocket.sendto(str(b).encode(),clientAddress)
				print("Seq No:", b, "Time recived:", t, "Packet Dropped: false")
			else:
				print("Seq No:", b, "Time recived:", t, "Packet Dropped: true")
				#print("dropped")
		else:
			print("Seq No:", b, "Time recived:", t, "Packet Dropped: true")
			#print("dropped")
				
	else:
		#pass
		print("Seq No:", b, "Time recived:", t, "Packet Dropped: true")
		#print("drop", b)

severSocket.close()

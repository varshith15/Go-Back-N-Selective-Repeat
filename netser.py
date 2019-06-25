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
parser.add_argument("-n",type=int)
parser.add_argument("-e",type=float)
    
args = parser.parse_args()

serverPort = args.p
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))
dp = args.e
maxpac=args.n
debug = args.d


exp = 0

while 1:
	message, clientAddress = serverSocket.recvfrom(2048)
	t = time.time()
	a,b = message.decode().split(" ")
	if exp == int(b):
		if random.random()>=dp:
			serverSocket.sendto(b.encode(), clientAddress)
			exp = exp + 1
			#print("accept", b,exp)
			print("Seq No:", b, "Time recived:", t, "Packet Dropped: false")
		else:	
			print("Seq No:", b, "Time recived:", t, "Packet Dropped: true1")
			#print(b)
	else:
		print("Seq No:", b, "Time recived:", t, "Packet Dropped: true2")
		#print("drop", b)

severSocket.close()

import math
import socket, select, string, sys
sys.path.insert(0, '../Find_IP/')
sys.path.insert(0, '../Trie/')
import netifaces as ni
import socket                   # Import socket module                     # module to calculate system IP
import time
from thread import *
from threading import Thread
import hashlib
import difflib
import bisect
import Queue
import threading


class Server :
	def __init__(self,peer_port,kdc_port) :

		self.MY_IP = '172.26.35.81'
		self.kdc_ip = '172.26.35.81'

		connection_type = 1
		print ("GOING TO INITIALIZE IP ADDRESSSSSSSS")
		while True :
			try :
				if connection_type == 1 :
					self.ip = ni.ifaddresses('enp1s0')[2][0]['addr']
				else :
					self.ip = ni.ifaddresses('eth0')[2][0]['addr']
				if self.ip == "" :
					continue				
			except :
				self.ip = ni.ifaddresses('eth0')[2][0]['addr']
			finally :
				break

		self.socket_obj = {}

		self.HOST = self.MY_IP
		self.peer_port = int(peer_port)
		self.kdc_port = int(kdc_port)

		self.bind_and_serve()           # communication with peers and clients after server creation

		print 'Super Outside'
		

	def peer_thread(self,buff):
		global BUFFER, count
		conn = buff[0]
		msg = conn.recv(1024)
		msg = msg.decode()
		print (msg)
		inp = "Hii peer"
		inp = inp.encode()
		conn.send(inp)
		print ("Two clients chatting")
		conn.close()


	def checking(self):
		while(True):
			print ("Want to talk to someone??")
			inp = raw_input("yes/no???\n")
			print inp
			if(inp=="yes"):
				self.talk_to_someone(self.kdc_port)
	
	def talk_to_someone(self,kdc_port):
		host = self.kdc_ip
		port = self.kdc_port 
		s = socket.socket()             # Create a socket object
		s.connect((host, port))
		message = "Hi KDC"
		message = message.encode()
		s.send(message)
		msg = s.recv(1024)
		msg = msg.decode()
		print (msg)
		s.close()
		print('connection closed')

	def bind_and_serve(self):
		print ("Client Module Started...")

		Thread(target=self.checking, args=()).start()     
		self.socket_obj.update({'s' : socket.socket(socket.AF_INET, socket.SOCK_STREAM)})  
																						
		print ("Listening to other peers:")
		self.socket_obj['s'].bind((self.HOST, self.peer_port))
		self.socket_obj['s'].listen(10)          
		while True:
			conn, addr = self.socket_obj['s'].accept()
			print ('Connected with ' + addr[0] + ':' + str(addr[1]))
			buff = [conn, self]
			start_new_thread(self.peer_thread ,(buff,))       # separate thread for each client
        	

def main() :
	server_obj = Server(sys.argv[1],sys.argv[2])


if __name__ == "__main__" :
	main()

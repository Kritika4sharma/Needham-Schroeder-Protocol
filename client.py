import math
import socket, select, string, sys
sys.path.insert(0, '../Find_IP/')
sys.path.insert(0, '../Trie/')
import netifaces as ni
import socket                   # Import socket module                  # module to calculate system IP
import time
from thread import *
from threading import Thread
import hashlib
import difflib
import bisect
import Queue
import threading

persist_port = 9993                 # set port where persistence is listening
persist_ip = '172.21.21.101'             # set ip of persistence


class Server :
	def __init__(self) :

		#create id of server using the hash of IP address and MAC
		self.HOST = ''   # Symbolic name meaning all available interfaces
		#self.PORT = 9167 # All servers will listen on this port -- to listen to CLIENTS
		#self.PEER_PORT = 9570 # to listen to PEERS
		#self.MASTER_PORT = 11500
		
		self.ip = ""
		self.nodeid = ""
		self.A_server = ""

		connection_type = 1
		print "GOING TO INITIALIZE IP ADDRESSSSSSSS"
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


		self.register_to_persistence()

		
	def register_to_persistence(self):
		s = socket.socket()             # Create a socket object
		
		host = persist_ip
		port = persist_port                # Reserve a port for your service.

		s.connect((host, port))

		message = raw_input()
		s.send(message)
		msg = s.recv(1024)
		print msg
		s.close()
		print('connection closed')


		s2 = socket.socket() 
		s2.connect((host, 9992))
		message = raw_input()
		s2.send(message)
		msg = s2.recv(1024)
		print msg

		s2.close()
		print('connection closed')


def main() :
	server_obj = Server()


if __name__ == "__main__" :
	main()

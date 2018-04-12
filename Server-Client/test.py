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

		connection_type = 1
		print "GOING TO INITIALIZE IP ADDRESSSSSSSS"
		print "hheh"
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
		

	def talk_to_client(self) :
		print "Hiiii peer"

	def peer_back_thread(self):
		print "Accepting to peer clients"
		self.socket_obj.update({'port_for_client' : socket.socket(socket.AF_INET, socket.SOCK_STREAM)})
		self.socket_obj['port_for_client'].bind((self.MY_IP,self.kdc_port))
		self.socket_obj['port_for_client'].listen(10)
		while True:
			conn, addr = self.socket_obj['port_for_client'].accept()
			print 'Connected @ peerclient ... with ' + addr[0] + ':' + str(addr[1])
			bundle = [conn, self, addr[0]]			
			start_new_thread(self.talk_to_client() ,(bundle,))


	def client_back_thread(self):
		print "Accepting to query from servers for client"
		self.socket_obj.update({'client_port_for_back' : socket.socket(socket.AF_INET, socket.SOCK_STREAM)})
		print "Back client port created"
		self.socket_obj['client_port_for_back'].bind((self.HOST, 1346))
		self.socket_obj['client_port_for_back'].listen(10)
		global BUFFER

		while True:
			conn, addr = self.socket_obj['client_port_for_back'].accept()
			print 'Connected @ peer for client-query ... with ' + addr[0] + ':' + str(addr[1])
			
			bundle = [conn, self, addr[0]]			
			data = conn.recv(BUFFER)

			start_new_thread(client_back_process ,(self,bundle[0],data))

	def bind_and_serve(self):
		print "Client Module Started..."

		Thread(target=self.peer_back_thread, args=()).start()     
		self.socket_obj.update({'s' : socket.socket(socket.AF_INET, socket.SOCK_STREAM)})  
																						
		print "Listening to other peers"
		self.socket_obj['s'].bind((self.HOST, self.peer_port))
		self.socket_obj['s'].listen(10)          

		'''try:
			Thread(target=self.client_back_thread, args=()).start()     # Separate thread to accept the incoming connections from tier 2 peers
		except Exception, errtxt:
			print errtxt
        '''
		while True:
			conn, addr = self.socket_obj['s'].accept()
			print 'Connected with ' + addr[0] + ':' + str(addr[1])
			 
			#start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
			buff = [conn, self]
			start_new_thread(client_thread ,(buff,))       # separate thread for each client
        

def main() :
	server_obj = Server(sys.argv[1],sys.argv[2])


if __name__ == "__main__" :
	main()

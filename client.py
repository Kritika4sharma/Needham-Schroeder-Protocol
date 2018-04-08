import math
import socket, select, string, sys
sys.path.insert(0, '../Find_IP/')
sys.path.insert(0, '../Trie/')
import socket                   # Import socket module                  # module to calculate system IP
import time
import hashlib
import difflib
import bisect

persist_port = 9993                 # set port where persistence is listening
persist_ip = '172.21.21.103'             # set ip of persistence


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
		print ("GOING TO INITIALIZE IP ADDRESSSSSSSS")

		self.socket_obj = {}


		self.register_to_persistence()

		
	def register_to_persistence(self):
		s = socket.socket()             # Create a socket object
		
		host = persist_ip
		port = persist_port                # Reserve a port for your service.

		s.connect((host, port))

		message = input()
		message = message.encode()
		s.send(message)
		msg = s.recv(1024)
		msg = msg.decode()
		print (msg)
		s.close()
		print('connection closed')


		s2 = socket.socket() 
		s2.connect((host, 9992))
		message = input()
		message = message.encode()
		s2.send(message)
		msg = s2.recv(1024)
		msg = msg.decode()
		print (msg)

		s2.close()
		print('connection closed')


def main() :
	server_obj = Server()


if __name__ == "__main__" :
	main()

import math
import socket, select, string, sys
sys.path.insert(0, '../Find_IP/')
sys.path.insert(0, '../Trie/')
import socket                   # Import socket module                  # module to calculate system IP
import time
import hashlib
import difflib
import bisect

persist_ip = '172.21.21.105'             # set ip of persistence


class Server :
	def __init__(self,kdc_port) :

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


		self.register_to_persistence(int(kdc_port))

		
	def register_to_persistence(self,kdc_port):
		s = socket.socket()             # Create a socket object
		
		host = persist_ip
		port = kdc_port                # Reserve a port for your service.

		s.connect((host, port))

		message = input()
		message = message.encode()
		s.send(message)
		msg = s.recv(1024)
		msg = msg.decode()
		print (msg)
		message = input()
		message = message.encode()
		s.send(message)
		#s.close()
		#print('connection closed')


def main() :
	server_obj = Server(sys.argv[1])


if __name__ == "__main__" :
	main()

import math
import socket, select, string, sys
sys.path.insert(0, '../Find_IP/')
sys.path.insert(0, '../Trie/')
import socket                   # Import socket module                  # module to calculate system IP
import time
import hashlib
import difflib
import bisect
from Crypto.Cipher import AES
from Crypto.Cipher import ARC4
from Crypto import Random
import random

print("Please Enter Port Number")
persist_port = input() 
persist_port = int(persist_port)               # set port where persistence is listening
persist_ip = '172.19.18.84'             # set ip of persistence
key = 'This is a key123'
def pad(s):
    return s + b"\0" * (AES.block_size - len(s) % AES.block_size)
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

		initiator = 'Alice';
		responder = input()
		nonceA = str(random.randint(1,1000000000))
		message =  initiator + '-' + responder  + '-' + nonceA
		message = message.encode()
		print("Message Sent")
		print(message)
		s.send(message) 



		complete_ticket = s.recv(4096)
		print("Complete Ticket Received to Alice")
		print(complete_ticket)
		key = 'Alice@123'
		obj1 = ARC4.new(key)
		alice_ticket = obj1.decrypt(complete_ticket)
		tickets = alice_ticket.split(b'$$@@')
		print("Decrypted Ticket by Alice")
		print(tickets)
		alice_ticket = tickets[0]
		print("Alice Ticket")
		print(alice_ticket)
		bob_ticket = tickets[1]
		key = 'Bob@123'
		obj2 = ARC4.new(key)
		bob_ticket = obj2.decrypt(bob_ticket)
		print("Bob Ticket")
		print(bob_ticket)


		'''
		obj = AES.new(key, AES.MODE_CBC, 'This is an IV456')

		msg = msg.split(b'$$@@')
		alice_ticket = msg[0]
		print("Ticket Received by Alice")
		print(alice_ticket)
		print("Ticket Decrypted by Alice")
		print (obj.decrypt(alice_ticket))

		bob_ticket = msg[1]
		print("Ticket Received by Bob")
		print(bob_ticket)
		key = 'This is a key456'
		obj = AES.new(key, AES.MODE_CBC, 'This is an IV456')
		print (obj.decrypt(bob_ticket))
		'''
		s.close()
		print('connection closed')

		'''
		s2 = socket.socket() 
		s2.connect((host, 7777))
		message = input()
		message = message.encode()
		s2.send(message)
		msg = s2.recv(1024)
		msg = msg.decode()

		s2.close()
		print('connection closed')
		'''


def main() :
	server_obj = Server()


if __name__ == "__main__" :
	main()

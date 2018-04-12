import math
import socket, select, string, sys
import socket                   # Import socket module                     # module to calculate system IP
import time
from threading import Thread
import hashlib
import difflib
from Crypto.Cipher import AES
from Crypto.Cipher import ARC4
import bisect
import threading
import random


class Server :
	def __init__(self,kdc_port,c1_port,c2_port) :

		self.MY_IP = '172.21.21.105'
		self.kdc_ip = '172.21.21.105'

		self.socket_obj = {}

		self.HOST = self.MY_IP
		self.peer_port = int(c1_port)
		self.kdc_port = int(kdc_port)
		self.c2_port = int(c2_port)

		self.bind_and_serve()           # communication with peers and clients after server creation

		print ('Super Outside')
		

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
			inp = input("yes/no???\n")
			if(inp=="yes"):
				self.talk_to_someone(self.kdc_port)

	def chatting(self,bob_ticket,session_key):
		host = self.MY_IP
		port = self.c2_port
		s = socket.socket()             # Create a socket object
		s.connect((host, port))
		s.send(bob_ticket) 		
		msg = s.recv(1024)
		obj1 = ARC4.new(session_key)
		msg = obj1.decrypt(msg)
		print("Decrypted Nonce")
		msg = msg.decode()
		msg = int(msg)
		msg = msg -1
		msg = str(msg)
		msg = msg.encode()
		nonceA = obj1.encrypt(msg)
		s.send(nonceA)


	
	def talk_to_someone(self,kdc_port):
		host = self.kdc_ip
		port = self.kdc_port 
		s = socket.socket()             # Create a socket object
		s.connect((host, port))
		inp = input()
		inp = inp.split('-')
		initiator = inp[0]
		responder = inp[1]
		nonceA = str(random.randint(1,1000000000))
		message =  initiator + '-' + responder  + '-' + nonceA
		message = message.encode()
		print("Message Sent")
		print(message)
		s.send(message) 

		complete_ticket = s.recv(4096)
		print("Complete Ticket Received to Alice")
		print(complete_ticket)
		key = input("Enter your key for decryption of ticket :")
		obj1 = ARC4.new(key)
		alice_ticket = obj1.decrypt(complete_ticket)
		tickets = alice_ticket.split(b'$$@@')
		print("Decrypted Ticket by Alice")
		print(tickets)
		alice_ticket = tickets[0]
		print("Alice Ticket")
		print(alice_ticket)
		alice_ticket = alice_ticket.split(b'-')
		session_key = alice_ticket[2]
		bob_ticket_original = tickets[1]
		key = 'Bob@123'
		obj2 = ARC4.new(key)
		bob_ticket = obj2.decrypt(bob_ticket_original)
		print("Bob Ticket")
		print(bob_ticket)
		s.close()
		print('connection closed')

		self.chatting(bob_ticket_original,session_key)

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
			Thread(target=self.peer_thread, args=(buff,)).start()    
        	

def main() :
	server_obj = Server(sys.argv[1],sys.argv[2],sys.argv[3])


if __name__ == "__main__" :
	main()
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

NAME = input("Enter your name :\n")

class Server :
	def __init__(self,kdc_port,client_port,Alice_ip,Bob_ip,Cherry_ip) :
		self.MY_IP = '127.0.0.1'
		self.kdc_ip = '127.0.0.1'
		self.socket_obj = {}
		self.HOST = self.MY_IP
		self.kdc_port = int(kdc_port)
		self.Alice_port = client_port
		self.Bob_port = client_port
		self.Cherry_port = client_port
		self.peer_port = int(client_port)
		self.Cherry_ip = Cherry_ip
		self.Alice_ip = Alice_ip
		self.Bob_ip = Bob_ip
		if(NAME=="Bob"):
			self.peer_port = int(client_port)
		if(NAME=="Cherry"):
			self.peer_port = int(client_port)
		self.bind_and_serve()           
		print ('Super Outside')
		

	def peer_thread(self,buff):
		global BUFFER, count
		conn = buff[0]
		msg = conn.recv(1024)
		print ("Ticket received from initiator :",msg)
		key = input("Enter Your key for Decryption:\n")
		obj1 = ARC4.new(key)
		msg = obj1.decrypt(msg)
		print("Your Decrypted Ticket : ",msg.decode())
		
		keys = msg.split(b'-')
		session_key = keys[1]
		nonceB = random.randint(1,10000000)
		nonceB = str(nonceB)
		nonceB = nonceB.encode()
		print("Number sent to initiator = ",nonceB.decode())
		obj2 = ARC4.new(session_key)
		nonceB = obj2.encrypt(nonceB)
		conn.send(nonceB)
		msg = conn.recv(1024)
		nonceB = obj2.decrypt(msg)
		print ("Number received from initiator = ",nonceB.decode())
		print ("Two clients chatting...")
		conn.close()

	def checking(self):
		while(True):
			inp = input("Want to talk to someone?? - yes/no\n")
			if(inp=="yes"):
				self.talk_to_someone(self.kdc_port)

	def chatting(self,bob_ticket,session_key,responder_ip):
		host = self.responder_ip
		port = self.c2_port
		s = socket.socket()             # Create a socket object
		s.connect((host, port))
		s.send(bob_ticket) 		
		msg = s.recv(1024)
		obj1 = ARC4.new(session_key)
		msg = obj1.decrypt(msg)
		print("Decrypted Nonce : ",msg.decode())
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
		initiator = NAME
		responder = input("To whom you want to communicate?\n")
		self.c2_port = int(self.Alice_port)
		if(responder=="Bob"):
			self.c2_port = int(self.Bob_port)
		if(responder=="Cherry"):
			self.c2_port = int(self.Cherry_port)
		nonceA = str(random.randint(1,1000000000))
		message =  initiator + '-' + responder  + '-' + nonceA
		print("Sending ",initiator," ",responder," ",nonceA," to kdc")
		message = message.encode()
		s.send(message) 

		complete_ticket = s.recv(4096)
		print("Complete Ticket Received to ",initiator," :")
		print(complete_ticket)
		key = input("Enter your key for decryption of ticket :\n")
		obj1 = ARC4.new(key)
		alice_ticket = obj1.decrypt(complete_ticket)
		tickets = alice_ticket.split(b'$$@@')
		print("Decrypted Ticket by ",initiator)
		print(tickets)
		alice_ticket = tickets[0]
		print("Ticket of ",initiator," = ",alice_ticket.decode())
		alice_ticket = alice_ticket.split(b'-')
		session_key = alice_ticket[2]
		bob_ticket_original = tickets[1]
		print("Ticket of ",responder," = ",bob_ticket_original)
		s.close()
		print('connection closed')

		responder_ip = self.Alice_ip
		if(responder=="Cherry"):
			responder_ip = self.Cherry_ip
		if(responder=="Bob"):
			responder_ip = self.Bob_ip
		self.chatting(bob_ticket_original,session_key,responder_ip)

	def bind_and_serve(self):
		Thread(target=self.checking, args=()).start()     
		self.socket_obj.update({'s' : socket.socket(socket.AF_INET, socket.SOCK_STREAM)})  
																						
		# print ("Listening to other peers...")
		self.socket_obj['s'].bind((self.HOST, self.peer_port))
		self.socket_obj['s'].listen(10)          
		while True:
			conn, addr = self.socket_obj['s'].accept()
			print ('Connected with ' + addr[0] + ':' + str(addr[1]))
			buff = [conn, self]
			Thread(target=self.peer_thread, args=(buff,)).start()    
        	

def main() :
	server_obj = Server(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])


if __name__ == "__main__" :
	main()

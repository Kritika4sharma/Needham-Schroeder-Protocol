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
import timeit

print('''
#   #                    #  #                            ###          #                               #               
#   #                    #  #                           #   #         #                               #               
##  #   ###    ###    ## #  # ##    ###   ## #          #       ###   # ##   # ##    ###    ###    ## #   ###   # ##  
# # #  #   #  #   #  #  ##  ##  #      #  # # #  #####   ###   #   #  ##  #  ##  #  #   #  #   #  #  ##  #   #  ##  # 
#  ##  #####  #####  #   #  #   #   ####  # # #             #  #      #   #  #      #   #  #####  #   #  #####  #     
#   #  #      #      #  ##  #   #  #   #  # # #         #   #  #   #  #   #  #      #   #  #      #  ##  #      #     
#   #   ###    ###    ## #  #   #   ####  #   #          ###    ###   #   #  #       ###    ###    ## #   ###   #     
''')

print(''' 
				 ####                  #                           ##   
				 #   #                 #                            #   
				 #   #  # ##    ###   ####    ###    ###    ###     #   
				 ####   ##  #  #   #   #     #   #  #   #  #   #    #   
				 #      #      #   #   #     #   #  #      #   #    #   
				 #      #      #   #   #  #  #   #  #   #  #   #    #   
				 #      #       ###     ##    ###    ###    ###    ###  
''')
start = 0
end = 0
NAME = input("Enter your name\n")


class Server :
	def __init__(self,kdc_port,Alice_port,Bob_port,Cherry_port) :

		self.MY_IP = '172.21.21.101'
		self.kdc_ip = '172.21.21.101'
		self.socket_obj = {}
		self.HOST = self.MY_IP
		self.kdc_port = int(kdc_port)
		self.Alice_port = Alice_port
		self.Bob_port = Bob_port
		self.Cherry_port = Cherry_port
		self.peer_port = int(Alice_port)
		if(NAME=="Bob"):
			self.peer_port = int(Bob_port)
		if(NAME=="Cherry"):
			self.peer_port = int(Cherry_port)
		self.bind_and_serve()           
		print ('Super Outside')
		

	def peer_thread(self,buff):
		global BUFFER, count
		conn = buff[0]
		msg = conn.recv(1024)
		print (msg)

		key = input("Enter Your key for Decryption")
		obj1 = ARC4.new(key)
		msg = obj1.decrypt(msg)
		print("Your Decrypted Ticket")
		print(msg)
		
		keys = msg.split(b'-')
		session_key = keys[1]
		nonceB = random.randint(1,10000000)
		nonceB = str(nonceB)
		nonceB = nonceB.encode()
		print(nonceB)
		obj2 = ARC4.new(session_key)
		nonceB = obj2.encrypt(nonceB)
		conn.send(nonceB)
		msg = conn.recv(1024)
		nonceB = obj2.decrypt(msg)
		print ("Number is : ",nonceB)
		print ("Two clients chatting")
		conn.close()

	def checking(self):
		while(True):
			print ("Want to talk to someone??")
			inp = input("yes/no??")
			if(inp=="yes"):
				global start
				start = timeit.default_timer()
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
		print("Decrypted Nonce : ",msg)
		msg = msg.decode()
		msg = int(msg)
		msg = msg -1
		msg = str(msg)
		msg = msg.encode()
		nonceA = obj1.encrypt(msg)
		global end
		end = timeit.default_timer()
		print("Latency b/w Clients")
		print(end - start)
		s.send(nonceA)

	def talk_to_someone(self,kdc_port):
		host = self.kdc_ip
		port = self.kdc_port 
		s = socket.socket()             # Create a socket object
		s.connect((host, port))
		print ("Give input in format : Initiator-Responder")
		inp = input()
		inp = inp.split('-')
		initiator = inp[0]
		responder = inp[1]
		self.c2_port = int(self.Alice_port)
		if(responder=="Bob"):
			self.c2_port = int(self.Bob_port)
		if(responder=="Cherry"):
			self.c2_port = int(self.Cherry_port)
		nonceA = str(random.randint(1,1000000000))
		message =  initiator + '-' + responder  + '-' + nonceA
		message = message.encode()
		print("Message Sent to kdc")
		print(message)
		s.send(message) 

		complete_ticket = s.recv(4096)
		print("Complete Ticket Received to ",initiator)
		print(complete_ticket)
		global end
		end = timeit.default_timer()
		print("Latency b/w " + initiator + "and KDC" )
		print(end - start)
		key = input("Enter your key for decryption of ticket :")
		obj1 = ARC4.new(key)
		alice_ticket = obj1.decrypt(complete_ticket)
		tickets = alice_ticket.split(b'$$@@')
		print("Decrypted Ticket by ",initiator)
		print(tickets)
		alice_ticket = tickets[0]
		print("Ticket of ",initiator)
		print(alice_ticket)
		alice_ticket = alice_ticket.split(b'-')
		session_key = alice_ticket[2]
		bob_ticket_original = tickets[1]
		print("Ticket of ",responder)
		print(bob_ticket_original)
		s.close()
		print('connection closed')
		global start 
		start = timeit.default_timer()
		self.chatting(bob_ticket_original,session_key)

	def bind_and_serve(self):
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
	server_obj = Server(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])


if __name__ == "__main__" :
	main()

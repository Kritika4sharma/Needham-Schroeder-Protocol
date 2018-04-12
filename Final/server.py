import socket
import sqlite3 as db
import hashlib     
import sys
from threading import Thread
import threading
import random
from Crypto.Cipher import AES  
from Crypto.Cipher import ARC4

my_ip = '172.21.21.105'

users = []
UserA = {'id': 'A' , 'name' : 'Alice','key':'Alice@123'}
UserB = {'id': 'B' , 'name' : 'Bob','key':'Bob@123'}
UserC = {'id': 'C' , 'name' : 'Cherry','key':'Cherry@123'}

users.append(UserA)
users.append(UserB)
users.append(UserC)

def client_thread(buff):
	global BUFFER, count
	conn = buff[0]
	msg = conn.recv(1024)
	print("Initiator Want to Communicate through KDC")
	msg = msg.decode()
	print (msg)
	msg = msg.split('-')
	initiator = msg[0]
	responder = msg[1]
	nonceA = msg[2]
	print("Ticket Sent to !!" , initiator)
	session_key = str(random.randint(1,1000000000))
	ticket_responder =  initiator + '-' + session_key
	ticket_responder = ticket_responder.encode()
	obj1 = ARC4.new(UserB['key'])
	ticket_responder = obj1.encrypt(ticket_responder)
	final_ticket = (nonceA + '-' + responder + '-' + session_key )
	final_ticket = final_ticket.encode()
	final_ticket = final_ticket +  b'$$@@' + ticket_responder
	obj2 = ARC4.new(UserA['key'])
	final_ticket = obj2.encrypt(final_ticket)
	conn.send(final_ticket)

class Server :
	def __init__(self, server_port) :
		self.HOST = my_ip
		self.PORT = int(server_port)
		print ("I am the KDC server : ",my_ip)		
		self.bind_and_serve()       # to listen to clients for establishing the secret key

	def bind_and_serve(self):
		print ("Serving the clients now...")
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.bind((self.HOST,self.PORT)) 
		s.listen(10)

		while True:
			conn, addr = s.accept()
			print ('Connected with client = ' + addr[0] + ':' + str(addr[1]))
			buff = [conn, self]
			thread = threading.Thread(target=client_thread, args=(buff,))
			thread.start()    

def main() :
	server_obj = Server(sys.argv[1])


if __name__ == "__main__" :
	main()
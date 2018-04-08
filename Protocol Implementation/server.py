import socket
import sqlite3 as db
import hashlib 
import random
from Crypto.Cipher import AES    

print("Please Enter Port Number")
curr_port = input()
curr_port = int(curr_port)
users = []
UserA = {'id': 'A' , 'name' : 'Alice','key':'This is a key123'}
UserB = {'id': 'B' , 'name' : 'Bob','key':'This is a key456'}
UserC = {'id': 'C' , 'name' : 'Cherry','key':'This is a key123'}

users.append(UserA)
users.append(UserB)
users.append(UserC)
def pad(s):
    return s + b"\0" * (AES.block_size - len(s) % AES.block_size)
def start_listening():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	host = socket.gethostname()               
	my_ip = '172.21.21.103'
	s.bind((my_ip,curr_port))                      
	s.listen(10)

	print ("Ip of persistence is : ",my_ip)

	'''
	for user in users:
		print(user['id'] , user['name'],user['key'])
	'''

	while True:

		conn, addr = s.accept()
		msg = conn.recv(1024)
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
		ticket_responder = pad(ticket_responder)
		obj1 = AES.new(UserB['key'], AES.MODE_CBC, 'This is an IV456')
		ciphertext = obj1.encrypt(ticket_responder)
		message = (nonceA + '-' + responder + '-' + session_key )
		message = message.encode() 
		message = message + b'-' + ciphertext
		message = pad(message)
		obj2  = AES.new(UserA['key'], AES.MODE_CBC, 'This is an IV456')
		message = obj2.encrypt(message)
		conn.send(message)

if __name__ == "__main__":

	start_listening()

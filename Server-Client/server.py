import socket
import sqlite3 as db
import hashlib     
import sys
from threading import Thread
import threading

my_ip = '172.21.21.105'

def client_thread(buff):
	global BUFFER, count
	print ("entereed here-----")

	conn = buff[0]
	self = buff[1]

	msg = conn.recv(1024)
	msg = msg.decode()
	print (msg,"*************")
	inp = input()
	inp = inp.encode()
	conn.send(inp)
	conn.close()

class Server :
	def __init__(self, server_port) :
		self.socket_obj = {}
		self.ip = my_ip
		self.PORT = int(server_port)
		print ("Ip of KDC server : ",my_ip)		
		
		server_port = int(server_port)
		self.bind_and_serve()    

	def bind_and_serve(self):
		print ("Inside server serve ..")
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.bind((my_ip,self.PORT)) 
		s.listen(10)

		while True:
			conn, addr = s.accept()
			print ('Connected with ' + addr[0] + ':' + str(addr[1]))
			buff = [conn, self]
			thread = threading.Thread(target=client_thread, args=(buff,))
			thread.start()    

def main() :
	server_obj = Server(sys.argv[1])


if __name__ == "__main__" :
	main()

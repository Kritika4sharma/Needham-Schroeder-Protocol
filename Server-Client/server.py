import socket
import sqlite3 as db
import hashlib     
import sys
from threading import Thread
import threading

my_ip = '172.26.35.81'

def client_thread(buff):
	global BUFFER, count
	conn = buff[0]
	msg = conn.recv(1024)
	msg = msg.decode()
	print (msg)
	inp = "Hii client"
	inp = inp.encode()
	conn.send(inp)
	print ("Secret key established for above client!")
	conn.close()

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

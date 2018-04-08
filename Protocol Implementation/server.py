import socket
import sqlite3 as db
import hashlib     

curr_port = 7777

def start_listening():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	host = socket.gethostname()               
	my_ip = '172.21.21.103'
	s.bind((my_ip,curr_port))                      
	s.listen(10)

	print ("Ip of persistence is : ",my_ip)

	while True:

		conn, addr = s.accept()
		msg = conn.recv(1024)
		msg = msg.decode()
		print (msg)
		inp = input()
		inp = inp.encode()
		conn.send(inp)	

if __name__ == "__main__":

	start_listening()

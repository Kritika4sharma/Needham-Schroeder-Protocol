import math
import socket, select, string, sys
import socket                   # Import socket module                  # module to calculate system IP


kdc_ip = '172.21.21.105'             # set ip of persistence

class Client :
	def __init__(self,kdc_port) :
		connection_type = 1
		self.checking(int(kdc_port))

		
	def checking(self,kdc_port):
		while(True):
			print ("Want to talk to someone??")
			inp = input("yes/no???\n")
			if(inp=="yes"):
				self.talk_to_someone(kdc_port)
	
	def talk_to_someone(self,kdc_port):
		host = kdc_ip
		port = kdc_port 
		s = socket.socket()             # Create a socket object
		s.connect((host, port))
		message = "Hi KDC"
		message = message.encode()
		s.send(message)
		msg = s.recv(1024)
		msg = msg.decode()
		print (msg)
		s.close()
		print('connection closed')


def main() :
	client_obj = Client(sys.argv[1])


if __name__ == "__main__" :
	main()

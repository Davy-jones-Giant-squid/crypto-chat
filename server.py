from socket import *
from thread import *


class MessageDB:
	def __init__(self):
		self.message_database = {}

	def add_message(self, to_user, message):
		if to_user not in self.message_database:
			raise Exception("Error, name does not exist")
		else:
			self.message_database[name].append(message)

	def get_message(self, to_user):
		if to_user not in self.message_database:
			raise Exception("Error, name does not exist")
		else:
			return self.message_database[name].pop(0)

	def add_user(self, name):
		if name in self.message_database:
			raise Exception("Error, name already exist")
		else:
			self.message_database[name] = []

	def remove_user(self, name):
		if name not in self.message_database:
			raise Exception("Error, name does not exist")
		else:
			del self.message_database[name]


def client_thread(conn):
	conn.send("HI Client!")
	conn.recv()


#instantiate MessageDB
message_db = MessageDB()


HOST = ""
PORT = 8080
reuse_time = 1

socket_fd = socket(AF_INET, SOCK_STREAM)
socket_fd.setsockopt(SOL_SOCKET, SO_REUSEADDR, reuse_time)

socket_fd.bind((HOST, PORT))
socket_fd.listen(10)

while True:
	connfd, addr = socket_fd.accept()
	start_new_thread(client_thread, (connfd,))


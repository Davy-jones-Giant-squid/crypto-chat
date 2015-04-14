'''
------------------- server.py ----------------------
 By: Chris Schultz, Sabine Ye

 MCS 425 Project - Secure Communications System

 This is server code portion of project.

 ToDo: -Add 'CLOSE' client request functionality
       -Add 'USERLIST' client request functionality
       -All Security Features (PGP, etc.)
'''



from socket import *
import thread
import threading

OK = 0
BAD = 1
CLOSE = 2

VALID_CLIENT_REQUESTS = ['IAM', 'GETMSG', 'SENDMSG', 'CLOSE', 'USERLIST']

'''
      ---MessageDB Class---

Manages active users and associated messages

'''
class MessageDB:
        ''' 
		---Class constructor---
	Paremeters: *None*
	Return: *None*

	Sets up database and lock fields
        '''
	def __init__(self):
		self.message_database = {}
                self.lock = threading.Lock()


	''' 
              ---add_message(...)---
        Parameters: to_user - user message is for
                    message - message
        Return: *None*
	Throws: Exception if to_user does not exist in system

        Adds message to database for to_user
        '''
	def add_message(self, to_user, message):
		if to_user not in self.message_database:
			raise Exception("Error, name does not exist")
		else:
 			concat = ''
			for string in message:
				concat += string + ' '
 
			self.message_database[to_user].append(concat)

	''' 
              ---get_message(...)---
        Parameters: to_user - messages for this user
        Return: str  
	Throws: Exception if to_user does not exist in system
                Exception if no messages currently for to_user

        Retrieves oldest message for to_user
        '''
	def get_message(self, to_user):
		if to_user not in self.message_database:
			raise Exception("Error, name does not exist")
		elif not self.message_database[to_user]:
			return Exception("Error, no message")
		else:
			return self.message_database[to_user].pop(0)

	''' 
              ---add_user(...)---
        Parameters: name - user to add to system
        Return: *None*
	Throws: Exception if name already in system

        Adds an inbox for name in the database
        '''
	def add_user(self, name):
		if name in self.message_database:
			raise Exception("Error, name already exist")
		else:
			self.message_database[name] = []

	''' 
              ---remove_user(...)---
        Parameters: name - username
        Return: *None*  
	Throws: Exception if name does not exist in system

        Removes name inbox from database
        '''
	def remove_user(self, name):
		if name not in self.message_database:
			raise Exception("Error, name does not exist")
		else:
			del self.message_database[name]

	''' 
              ---get_user_list(...)---
        Parameters: *None*
        Return: str

        Retreives a str of all active users
        '''
	def get_user_list(self):
		user_list = ''
		#empty check, should never run
		if not self.message_database:
			return '*None*'

		for key in self.message_database:
			user_list += '%s, ' % (key)

		return user_list


''' 
      ---send_response(...)---
Parameters: conn - connection socket to client
            msg_type - OK, BAD, etc.
            msg - associated message
Return: *None*  

Sends server response to client
'''
def send_response(conn, msg_type, msg = None):
	send_msg = ''

	if msg_type == OK:
		send_msg += 'OK '
	elif msg_type == CLOSE:
		send_msg += 'CLOSE '
	else:
		send_msg += 'BAD '

	if (not msg is None) and isinstance(msg, basestring):
		send_msg += msg
	else:
		send_msg += '*None*'

	conn.send(send_msg)


''' 
      ---close_connection(...)---
Parameters: username - name of user thread is associated with
            conn - connection socker to client
            message_db - reference to database manager
Return: *None*  

Closes connection with client and terminates connection thread
'''
def close_connection(username, conn, message_db):
	if not username == '*None*':
		try:
			message_db.remove_user(username)
		except Exception:
			pass
	send_response(conn, CLOSE)
	conn.close()
	thread.exit()


''' 
      ---register_client(...)---
Parameters: conn - connection socket to client
            message_db - reference to database manager
Return: Returns clientname of client  

Registers client with database so database can maintain a
message inbox for the client
'''
def register_client(conn, message_db):
	user_input = conn.recv(1024)
	
	inputs = user_input.split()
	
	if len(inputs) == 2 and inputs[0] == 'IAM':
		try:
			message_db.add_user(inputs[1])
			send_response(conn, OK)
		except Exception:
			close_connection('*None*', conn, message_db)
	else:
		close_connection('*None*', conn, message_db)

	return inputs[1]


''' 
      ---get_client_request(...)---
Parameters: conn - connection socket to client
Return: str list

Retrieves a client request. Returns the client request as a delimited list
of strs
'''
def get_client_request(conn):
	client_request = conn.recv(1024)
	return  client_request.split()


''' 
      ---serve_request(...)---
Parameters: user_request -  client's request
            username - client's name associated with this thread   
            conn - connection socket to client
            message_db - associated message
Return: *None*  

Processes client's request
'''
def serve_request(user_request, username, conn, message_db):
	if not user_request[0] in VALID_CLIENT_REQUESTS:
		send_response(conn, BAD)

	elif user_request[0] == 'GETMSG':
		try:
			msg = message_db.get_message(username)
		except Exception:
			msg = '*None*'

		send_response(conn, OK, msg)
		 
	elif user_request[0] == 'SENDMSG':
		try:
			message_db.add_message(user_request[1], user_request[2:])
			send_response(conn, OK)
		except:
			send_response(conn, BAD)
	elif user_request[0] == 'USERLIST':
		try:
			user_list = message_db.get_user_list()
			send_response(conn, OK, user_list)
		except:
			send_response(conn, BAD)
''' 
      ---client_thread(...)---
Parameters: conn - connection socket to client
            message_db: reference to database manager
Return: *None*  

Jumping off point for a thread once a client connection is established
'''
def client_thread(conn, message_db):
	clientname = register_client(conn, message_db)
	while True:
		client_request = get_client_request(conn)
		if len(client_request) == 0:
			break
		else:
			serve_request(client_request, clientname, conn, message_db)

	close_connection(clientname, conn, message_db)


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
	thread.start_new_thread(client_thread, (connfd,message_db,))


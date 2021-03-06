'''
------------------- server.py ----------------------
 By: Chris Schultz, Sabine Ye

 MCS 425 Project - Secure Communications System

 This is server code portion of project.

 ToDo: *Done*
'''


from socket import *
import thread
import threading
import pdb
import sys
import os

OK = 0
BAD = 1
CLOSE = 2

VALID_CLIENT_REQUESTS = ['IAM', 'WHO',  'GETMSG', 'SENDMSG', 'CLOSE', 'USERLIST']

'''
      ---MessageDB Class---

Manages active users and associated messages

'''
class MessageDB:
        ''' 
		---Class constructor---
	Paremeters: *None*
	Return: *None*

	Sets up database, rsa public key storage, and lock fields
        '''
	def __init__(self):
		self.message_database = {}
		self.rsa_public_keys = {}
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
		self.lock.acquire(True)
		#print message
		if to_user not in self.message_database:
			self.lock.release()
			raise Exception("Error, name does not exist")
		else:
			self.message_database[to_user].append(message)
		self.lock.release()

	''' 
              ---get_message(...)---
        Parameters: to_user - messages for this user
        Return: str  
	Throws: Exception if to_user does not exist in system
                Exception if no messages currently for to_user

        Retrieves oldest message for to_user
        '''
	def get_message(self, to_user):
		self.lock.acquire(True)
		if to_user not in self.message_database:
			self.lock.release()
			raise Exception("Error, name does not exist")
		elif not self.message_database[to_user]:
			self.lock.release()
			return Exception("Error, no message")
		else:
			returnValue =  self.message_database[to_user].pop(0)
			self.lock.release()
			return returnValue
		
	''' 
              ---add_user(...)---
        Parameters: name - user to add to system
                    rsa_public_key - rsa public key associated with user
        Return: *None*
	Throws: Exception if name already in system

        Adds an inbox for name in the database
        '''
	def add_user(self, name, rsa_public_key):
		self.lock.acquire(True)
		if name in self.message_database:
			self.lock.release()
			raise Exception("Error, name already exist")
		else:
			self.message_database[name] = []
			self.rsa_public_keys[name] = rsa_public_key
			self.lock.release()

	''' 
              ---remove_user(...)---
        Parameters: name - username
        Return: *None*  
	Throws: Exception if name does not exist in system

        Removes name inbox from database
        '''
	def remove_user(self, name):
		self.lock.acquire(True)
		if name not in self.message_database:
			self.lock.release()
			raise Exception("Error, name does not exist")
		else:
			del self.message_database[name]
			del self.rsa_public_keys[name]
			self.lock.release()

	''' 
              ---get_user_list(...)---
        Parameters: *None*
        Return: str

        Retreives a str of all active users
        '''
	def get_user_list(self):
		self.lock.acquire(True)
		user_list = ''
		#empty check, should never run
		if not self.message_database:
			self.lock.release()
			return '*None*'

		for key in self.message_database:
			user_list += '%s, ' % (key)

		self.lock.release()
		return user_list

	'''
         ---get_user_rsa(...)---
        Parameters: user - username
        Return: *None*  
	Throws: Exception if user does not exist in system

        Retrieves public rsa key of user
	'''
	def get_user_rsa(self, user):
		self.lock.acquire(True) 
		if user not in self.rsa_public_keys:
			self.lock.release()
			raise Exception("Error, name does not exist")
		else:
			returnValue =  self.rsa_public_keys[user]
			self.lock.release()
			return returnValue


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
	try:
		send_response(conn, CLOSE)
		conn.close()
	except:
		pass

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
	user_input = conn.recv(2500)
	
	inputs = user_input.split(' ', 2)	
	if len(inputs) == 3 and inputs[0] == 'IAM':
		try:
			message_db.add_user(inputs[1], inputs[2])
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
	client_request = conn.recv(5000)
	return  client_request.split(' ', 2)


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
	#pdb.set_trace()
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
			message_db.add_message(user_request[1], user_request[2])
			send_response(conn, OK)
		except:
			send_response(conn, BAD)
	elif user_request[0] == 'USERLIST':
		try:
			user_list = message_db.get_user_list()
			send_response(conn, OK, user_list)
		except:
			send_response(conn, BAD)
	elif user_request[0] == 'WHO':
		try:
			user_public_rsa = message_db.get_user_rsa(user_request[1])
			send_response(conn, OK, user_public_rsa)
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
	try:
		while True:
			client_request = get_client_request(conn)
			if len(client_request) == 0:
				break
			else:
				serve_request(client_request, clientname, conn, message_db)
	except:
		pass
	finally:
		close_connection(clientname, conn, message_db)


''' 
      ---commands_available(...)---
Parameters: *None*
Return: *None*  

Displays commands available to user 
'''
def commands_available():
	print 'Commands Available: '
	print "  - 'get' or 'g' <user>: show messages stored on server for user "
  	print "  - 'help' or 'h': displays this menu"
	print "  - 'online' or 'o': returns list of all online users"
	print "  - 'quit' or 'q': quits server"
	print "  - 'who' or 'w' <user>: returns public key of user"


''' 
      ---server_monitor(...)---
Parameters: message_db - reference to message database
Return: *None*  

Server monitor thread
'''
def server_monitor(message_db):
	print 'MCS 425 - Crypto Chat Server Program'
	print 'by: Chris Schultz and Sabine Ye\n'
	print '***Disclaimer: This program is for educational purposes. Authors make'
	print 'no guarantee on absolute secrecy of a message sent between users'
	print 'of this program. Also, Authors take no responsibilities for any'
	print 'actions taken by users of this program.\n' 

	print 'Server is running!!!\n'
        commands_available()

    	while True:
		try:
      			print 'Input Command >> '
      			msg = sys.stdin.readline().strip().lower()
      			if msg == 'help' or msg == 'h':
        			commands_available()
      			elif 'get' in msg or 'g' in msg:
				split = msg.split()
				it = iter(message_db.message_database[split[1]])
				for msg in it:
					print msg
					print '\n'
      			elif msg == 'online' or msg == 'o':
				for user in  message_db.message_database:
					print user, ', ',
				print '' 
      			elif msg == 'quit' or msg == 'q':
        			os._exit(1)
			elif 'who'in msg or 'w' in msg:
				split = msg.split()
				print message_db.rsa_public_keys[split[1]]
      			else:
        			print '*Error: input was not a recognized command*'
        			commands_available()
			print ''
  		except Exception:
			print '*Error: error with input*\n'
        		commands_available()

''' 
      ---main(...)---
Parameters: *None*
Return: *None*  

Starting point of Program
'''
def main():
	message_db = MessageDB()


	HOST = ""
	PORT = 8080
	reuse_time = 1

	socket_fd = socket(AF_INET, SOCK_STREAM)
	socket_fd.setsockopt(SOL_SOCKET, SO_REUSEADDR, reuse_time)

	socket_fd.bind((HOST, PORT))
	socket_fd.listen(10)

	thread.start_new_thread(server_monitor, (message_db,))

	while True:
		connfd, addr = socket_fd.accept()
		thread.start_new_thread(client_thread, (connfd,message_db,))

if __name__ == '__main__':
  main()

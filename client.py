import socket
import sys
from Crypto.PublicKey import RSA

def RSA_key_generation():
  """
  Generate RSA Keys 
  """
  key = RSA.generate(2048)
  private_key = key.exportKey('PEM')
  public_key= key.publickey().exportKey('PEM')

  return private_key, public_key
  #print key.publickey().exportKey('PEM')
  

def establish_socket_connection(ip, port = 8080):
  try:
    print '\nEstablishing Socket and Connection with Server......',
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, port))
    print '*Done*'  
  except socket.error, msg:
    print '*Failed*'
    print 'Error code: ' + str(msg[0]) + ' . Error message: ' + msg[1]
    sys.exit(-1)
  except socket.gaierror, msg:
    print '*Failed*'
    print 'Error code: ' + str(msg[0]) + ' . Error message: ' + msg[1]
    sys.exit(-1)
  return s


def claim_username(conn, username):
  try:
    print 'Claiming Username with Server......',
    conn.send('IAM ' + username)
    msg = conn.recv(1024)
    if msg.split()[0] == 'OK':
      print '*Done*'
    else:
      print '*Failure*'
      print 'Restart program with a new username'
      sys.exit(-1)
  except socket.gaierror, msg:
    print '*Connection Failure*'
    print 'Error code: ' + str(msg[0]) + ' . Error message: ' + msg[1]
    sys.exit(-1)
  except Exception:
    print '*Communcation Error*'
    sys.exit(-1)


def commands_available():
  print 'Commands Available: '
  print "  - 'get' or 'g': gets all messages "
  print "  - 'help' or 'h': displays this menu"
  print "  - 'online' or 'o': returns list of all online users"
  print "  - 'quit' or 'q': quits program"
  print "  - 'send' or 's': send message request"
 

def send_message(conn):
  print "-to whom(must be online)?: "
  to_whom = sys.stdin.readline().strip().lower() 
  print "-message: "
  message = sys.stdin.readline().strip()

  conn.send("SENDMSG " + to_whom + ' ' + message)

  return_message = conn.recv(1024).split()[0]
  if return_message == 'OK':
    print 'Success!'
  else:
    print 'Failed... Make sure recipient is online and spelling is correct'

def get_messages(conn):
   while True:
    conn.send("GETMSG")
    msg = conn.recv(1024)
    if not '*None*' in msg:
      print msg[2:], '\n'
    else:
      break

def chat_service(conn, username):
  print "\n*Chat Service Active*\n"
  commands_available()

  try:
    while True:
      print ('\n<%s>' % (username)),
      msg = sys.stdin.readline().strip().lower()
      if msg == 'help' or msg == 'h':
        commands_available()
      elif msg == 'send' or msg == 's':
        send_message(conn)
      elif msg == 'get' or msg == 'g':
        get_messages(conn)
      elif msg == 'online' or msg == 'o':
        continue #temp
        #get_whoose_online()
      elif msg == 'quit' or msg == 'q':
        conn.close()
        sys.exit()
      else:
        print '*Error: input was not a recognized command*'
        commands_available()
  except socket.gaierror, msg:
    print '*Connection Failure*'
    print 'Error code: ' + str(msg[0]) + ' . Error message: ' + msg[1]
    sys.exit(-1)
  except Exception:
    print '*Communcation Error*'
    sys.exit(-1)

def main():
  print 'MCS 425 - Crypto Chat Program'
  print 'by: Chris Schultz and Sabine Ye\n'
  print '***Disclaimer: This program is for educational purposes. Authors make'
  print 'no guarantee on absolute secrecy of a message sent between users'
  print 'of this program. Also, Authors take no responsibilities for any'
  print 'actions taken by users of this program.\n' 

  print 'Enter username: '
  username = sys.stdin.readline().strip()
  print 'Enter server ip: '
  ip = sys.stdin.readline().strip()
  
  conn = establish_socket_connection(ip)
  private, public = RSA_key_generation()
  claim_username(conn, username)
  chat_service(conn, username)
   
if __name__ == '__main__':
  main()

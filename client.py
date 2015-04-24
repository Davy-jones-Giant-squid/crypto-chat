import socket
import sys
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from Crypto import Random
from Crypto.Hash import MD5
from cypari.gen import pari as pari
from EZ425ES import *
import pdb

#Population is used to generate random session key
POPULATION = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
E = 65537
TAG = "<spacing>" #Used to delimit the string sent

def who_is_online(conn):
  conn.send('USERLIST')
  userlist = conn.recv(2000)
  print userlist[3:]
 
def RSA_key_generation():
  """
  Generate RSA Keys 
  """
  key_obj = RSA.generate(2048)
  private_key = key_obj.exportKey('PEM')
  public_key= key_obj.publickey().exportKey('PEM')

  return private_key, public_key
  

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


def claim_username(conn, username, rsa_public_key):
  try:
    print 'Claiming Username with Server......',
    conn.send('IAM ' + username + " " + rsa_public_key)
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

def request_public_rsa(conn, whom):
  conn.send('WHO ' + whom);
  whom_rsa = conn.recv(2500) #requesting the RSA key
  whom_rsa = whom_rsa[3:] #RSA public key of the person you're sending the message to
  return whom_rsa

def commands_available():
  print 'Commands Available: '
  print "  - 'get' or 'g': gets all messages "
  print "  - 'help' or 'h': displays this menu"
  print "  - 'online' or 'o': returns list of all online users"
  print "  - 'quit' or 'q': quits program"
  print "  - 'send' or 's': send message request"


def test_send_message(private_key, public_key):
  message = "Hello there"
  ####### encrypt message ###########

  key = "".join(Random.random.sample(POPULATION, 16))

  iv = Random.new().read(AES.block_size)
  #print "iv ", iv
  cipher = AES.new(key, AES.MODE_CFB, iv)
  print "cipher: ", cipher
  encrypted_message = cipher.encrypt(message)
  print "encrypted_message: ", encrypted_message

  h = MD5.new()
  h.update(message)

  #print "Digest: ", h.hexdigest()
  
  #convert digest into integers
  H = s2n(h.hexdigest())
  d = RSA.generate(2048)
  d = RSA.importKey(private_key)
  H_raised_to_d = d.decrypt(H)
  #print integer_d
  #H = H**private_key #H is the digest raised to the private key
  #print "H**d: ",H_raised_to_d

  d = RSA.importKey(public_key)
  
  #print "(H**d)**e: ", d.encrypt(H_raised_to_d, '121239')[0]
  #print "original hash: ", H

  

  
  #########################################



def send_message(conn, private_key, username):
  print "-to whom(must be online)?: "
  to_whom = sys.stdin.readline().strip().lower() 
  print "-message: "
  message = sys.stdin.readline().strip()

  ####### encrypt message ###########
  key = "".join(Random.random.sample(POPULATION, 16)) #Generate a random key word
  key_num = s2n(key)
  to_whom_rsa = request_public_rsa(conn, to_whom)
  n = RSA.importKey(to_whom_rsa)

  #encrypt key with destination RSA
  encrypted_key = (n.encrypt(key_num, None))[0]
  iv = Random.new().read(AES.block_size)
  cipher = AES.new(key, AES.MODE_CFB, iv)
  encrypted_message = cipher.encrypt(message)

  #Create digest from MD5 hash of message
  h = MD5.new()
  h.update(message)
  H = s2n(h.hexdigest()) #convert into integers

  #H is then raised to the private key (d)
  d = RSA.importKey(private_key)
  H_raised_to_d = d.decrypt(H)
  
  encrypted_pack = str(H_raised_to_d)+TAG+str(encrypted_key)+TAG+iv+TAG+encrypted_message+TAG+username
  #########################################

  conn.send("SENDMSG " + to_whom + ' ' + encrypted_pack)

  return_message = conn.recv(1024).split()[0]
  if return_message == 'OK':
    print 'Success!'
  else:
    print 'Failed... Make sure recipient is online and spelling is correct'

def get_messages(conn, private_key):
  while True:
    conn.send("GETMSG")
    #pdb.set_trace()
    msg = conn.recv(4000)
    if not '*None*' in msg:
      ####### Decrypt message ###########
      encrypted_message = msg[3:].split(TAG)
      extracted_H = int(encrypted_message[0])
      extracted_encrypted_key = int(encrypted_message[1])
      extracted_iv = encrypted_message[2]
      extracted_encrypted_message = encrypted_message[3]
      from_user = encrypted_message[4]

      #Decrypt session key
      d = RSA.importKey(private_key)
      key_num = d.decrypt(extracted_encrypted_key)

      key_str = n2s(key_num)

      #Decrypt message
      cipher = AES.new(key_str, AES.MODE_CFB, extracted_iv)
      decrypted_message = cipher.decrypt(extracted_encrypted_message)

      #Hash the message
      h_prime = MD5.new()
      h_prime.update(decrypted_message) #the original message is hashed

      #Verify the authenticity of the digest H
      from_whom_rsa = request_public_rsa(conn, from_user) #Get sender's public key
      n = RSA.importKey(from_whom_rsa)
      H_prime = (n.encrypt(extracted_H, None))[0]
      verify_H = n2s(H_prime)

      #print "h_prime digest: ", h_prime.hexdigest()
      #print "verify_H: ", verify_H

      if verify_H == h_prime.hexdigest():
        print "from ", from_user, ": ", decrypted_message
      else:
        print "Authentication failure"

      ####################################
    else:
      break

def chat_service(conn, username, private_key):
  print "\n*Chat Service Active*\n"
  commands_available()

  try:
    while True:
      print ('\n<%s>' % (username)),
      msg = sys.stdin.readline().strip().lower()
      if msg == 'help' or msg == 'h':
        commands_available()
      elif msg == 'send' or msg == 's':
        send_message(conn, private_key, username)
      elif msg == 'get' or msg == 'g':
        get_messages(conn, private_key)
      elif msg == 'online' or msg == 'o':
        who_is_online(conn)
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
    print '*Communication Error*'
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

  #test_send_message(private, public)
  
  claim_username(conn, username, public)

  chat_service(conn, username, private)
   
if __name__ == '__main__':
  main()

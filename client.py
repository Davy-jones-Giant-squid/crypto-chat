import socket
import sys

def run():
  try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   
  except socket.error, msg:
    print 'Failed to create socket. Error code: ' + str(msg[0]) + ' . Error message: ' + msg[1]
    sys.exit()


  #host = 'www.google.com'
  ip = '127.0.0.1'
  port = 8080

  '''
  try:
    remote_ip = socket.gethostbyname(host)
  except socket.gaierror:
    print 'Hostname could not be resolved'
    sys.exit()
  '''
  try:
    s.connect((ip, port))
    hi = s.recv(1024)
    print hi
  except socket.gaierror, msg:
    print 'Failed to create socket. Error code: ' + str(msg[0]) + ' . Error message: ' + msg[1]
    sys.exit()

run()
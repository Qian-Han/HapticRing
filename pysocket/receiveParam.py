#!/usr/bin/python
import os
os.environ['PYTHON_EGG_CACHE'] = '/tmp'
import socket
import struct
import sys
import time
import argparse

profile_data = []

def interprate(data):
	global profile_data
	del profile_data[:]
	profile_data = data.split(',')
	#count = int(profile_data[0])

	print(profile_data[0])


parser = argparse.ArgumentParser(description='Sending --message string via socket')

parser.add_argument('--message', action='store', dest='message', default='<Int 8>' ,help='Message to send[default:<Int 8>]')
parser.add_argument('--host', action='store', dest='host', default='localhost' ,help='Host name[default:localhost]')
parser.add_argument('--port', action='store', dest='port', default=9999, type=int, help='Port number [default: 9090]')

args = parser.parse_args()

HOST = args.host    
PORT = args.port

print 'HOST = %s, PORT = %d' % (HOST, PORT)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))
#sock.send(message)

#wait for messsage
try:
    while True:
    	data = sock.recv(1024)
    	if data:
    		interprate(data)

    		#save it back to list
except KeyboardInterrupt:
	sock.close()
	pass

print("sock closed")

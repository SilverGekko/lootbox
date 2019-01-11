#/bin/python3

import socket
import sys

TCP_IP = '127.0.0.1'
TCP_PORT = 5003
BUFFER_SIZE = 1024
MESSAGE = b"Message in a bottle"



s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))

f = open("files/file.txt", "rb") #r - open for reading, b - binary mode
l = f.read(1024)
while l:
    s.send(l)
    l = f.read(1024)
    print("Sending:", l)
    print(type(l))
    print(not not l)
s.close()



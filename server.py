#/bin/python3

import socket
import sys
import rsa

TCP_IP = '127.0.0.1'
TCP_PORT = 5003
BUFFER_SIZE = 1024 # make 1024 or larger later

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

i = 0

while True:
    conn, addr = s.accept()
    print("Connection address", addr)
    filename = conn.recv(64).rstrip(b'\0').decode('utf-8') # get the filename from the client and convert it to string
    f = open('dest/' + filename, 'wb') # w - open file for writing (truncates), b = binary mode
    i += 1
    data = conn.recv(BUFFER_SIZE)
    while data:
        print("Received:\nFilename: ", filename)
        print("Received:\nData: ", data)
        f.write(data)
        data = conn.recv(1024)
    f.close()
conn.close()

#/bin/python3

import socket
import utils
import json
import sys
import rsa
import os

TCP_IP = '127.0.0.1'
TCP_PORT = 5003
BUFFER_SIZE = 1024
DIR = "dest/"

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((TCP_IP, TCP_PORT))
    s.listen(1)

    # main loop
    while True:
        conn, addr = s.accept()
        print("Connection address", addr)
        json_file_data = json.loads(conn.recv(BUFFER_SIZE).rstrip(b'\0').decode('utf-8')) # get the json file data from the client and convert it to string
        print(json_file_data)

        if not os.path.isdir(DIR):
            os.mkdir(DIR)

        if (os.path.isfile(DIR + json_file_data["filename"]) and json_file_data["md5checksum"] != utils.md5(DIR + json_file_data["filename"])) or not os.path.isfile(DIR + json_file_data["filename"]):
            # TODO: send the 'go ahead' signal to the client to send the file
            conn.send(b'y')
            with open('dest/' + json_file_data["filename"], 'wb') as f: # w - open file for writing (truncates), b = binary mode
                data = conn.recv(BUFFER_SIZE)
                while data:
                    print("Received:\nFilename: ", json_file_data["filename"])
                    print("Received:\nData: ", data)
                    f.write(data)
                    data = conn.recv(BUFFER_SIZE)
        else:
            # file with that name exists and has the same checksum, no need to send
            # TODO: create a list of error codes to send to the client
            conn.send(b'n')
            print("[SERVER]: Client tried to send duplicate filename \"%s\" with identical checksum \"%s\"" % (str(json_file_data["filename"]), str(json_file_data["md5checksum"])) )
        conn.close()

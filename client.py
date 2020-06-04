# /bin/python3

import tkinter as tk
from tkinter import ttk
import json
import utils
import rsa
import socket
import sys
import os

TCP_IP = '127.0.0.1'
TCP_PORT = 5003
BUFFER_SIZE = 1024
MESSAGE = b"Message in a bottle"
DIR = "src_files/"


def list_dir_files(path):
  for file in os.listdir(path):
    if os.path.isfile(os.path.join(path, file)):
      yield file


class ClientApp(tk.Tk):
  def __init__(self):
    super().__init__()

    if not os.path.isdir(DIR):
      os.mkdir(DIR)

    self.connection_data = self.load_connection_data()

    self.active_socket = None

    self.title("Lootbox Client")

    self.resizable(False, False)

    # center the window
    # assuming you have a symmetrical setup of monitors...
    window_width = self.winfo_reqwidth()
    window_height = self.winfo_reqwidth()

    position_right = int(self.winfo_screenwidth() / 2 - window_width / 2)
    position_down = int(self.winfo_screenheight() / 3 - window_height / 2)

    self.geometry("+{}+{}".format(position_right, position_down))
    ###########################################################################################
    # buttons
    ###########################################################################################

    self.file_list = tk.Listbox(self, selectmode='extended')
    self.file_list.pack()
    # for file in files("./src_files"):
    #   self.file_list.insert(tk.END, file)
    self.refresh_list(self.file_list)

    self.send_file_button = tk.Button(
      text="Send File",
      command=lambda: self.send_file(
        self.file_list.get(self.file_list.curselection()), self.connection_data
      )
    )
    self.send_file_button.pack()

    self.refresh_button = tk.Button(
      text="Refresh List",
      command=lambda: self.refresh_list(self.file_list)
    )
    self.refresh_button.pack()

    self.server_connection_light = tk.Label(background='green3')
    self.server_connection_light.pack(fill=tk.X)

    self.init_funcs()

  def ping_server(self, connection_data):
    # big massive TODO:
    # think about what makes sense:
    #   - having the client connected to the server all the time
    #   - having a connection be made for each file sent (current implementation)
    #   - having the client connect and stay connected until a timeout happens, then diconnect regardless (good)
    #   - having the client connect and stay connected until a timeout happens, then diconnect if no activity (good)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
      try:
        s.connect((connection_data["host"], connection_data["port"]))
      except ConnectionRefusedError:
        print("Could not establish a connection to the server at", connection_data)
        return 1
      return 0

  def connection_light(self, light):
    color = 'green3' if self.active_socket else 'firebrick3'
    light.config(background=color)
    # print(color)
    # print(self.active_socket.fd)
    self.after(2000, self.connection_light, light)

  def load_connection_data(self):
    """
    Returns a dict full of the connection data from the parsed json config file.

    If no file named 'connection.json' exists, it will be initialized with default values and created.
    """
    try:
      json_data = open('connection.json', 'r')
    except FileNotFoundError:
      json_data = open('connection.json', 'w+')
      data_dict = {
          "name": "local server",
          "host": "127.0.0.1",
          "port": 5003,
      }
      json.dump(data_dict, json_data)
      # go back to the beginning since we just wrote a bunch of data
      json_data.seek(0)
    connection_data = json.loads(json_data.read())
    return connection_data

  def refresh_list(self, listbox):
    listbox.delete(0, tk.END)
    for file in list_dir_files("./src_files"):
      listbox.insert(tk.END, file)

  def send_file(self, filename, connection_data):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
      try:
        s.connect((connection_data["host"], connection_data["port"]))
      except ConnectionRefusedError:
        print("Could not establish a connection to the server at", connection_data)
        return

      self.active_socket = s

      print (self.active_socket)

      # os.listdir("files")
      #filename = input()

      # r - open for reading, b - binary mode
      f = open(DIR + filename, "rb")
      # s.send(bytes(filename, 'utf-8') + (b'\0' *  (64 - len(filename) ))) # send over the filename json so the server knows what we want to send
      json_to_send = utils.jsonify(DIR + filename)
      # max json data size of 1024 bytes
      # send the server the json data of the file(s) to be sent
      s.send(bytes(json_to_send, 'utf-8') + (b'\0' * (BUFFER_SIZE - len(json_to_send))))

      # receive the server "yes send" or "no, already have the file" message
      go_ahead = s.recv(1)
      print(go_ahead)

      if go_ahead == b'y':  # yes send
        print("inside yes")
        # send the file
        l = f.read(BUFFER_SIZE)
        while l:
          s.send(l)
          l = f.read(BUFFER_SIZE)
          print("Sending:", l)
          print(type(l))
          print(not not l)
      else:
        print("[CLIENT]: Server said destination already contains a file with that name and checksum")
        # else don't send the file
        pass
      
      # self.active_socket = None

  def init_funcs(self):
    self.connection_light(self.server_connection_light)


if __name__ == "__main__":
  program = ClientApp()
  program.mainloop()

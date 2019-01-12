#/bin/python3

import tkinter as tk
from tkinter import ttk
import socket
import sys
import os

TCP_IP = '127.0.0.1'
TCP_PORT = 5003
BUFFER_SIZE = 1024
MESSAGE = b"Message in a bottle"

def files(path):  
    for file in os.listdir(path):
        if os.path.isfile(os.path.join(path, file)):
            yield file

class ClientApp(tk.Tk):
    def __init__(self):
        super().__init__()

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
        for file in files("./src_files"):
            self.file_list.insert(tk.END, file)
        
        self.send_file_button = tk.Button(text="Send File", command = lambda: self.send_file(self.file_list.get(self.file_list.curselection())) )
        self.send_file_button.pack()

    def send_file(self, filename):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((TCP_IP, TCP_PORT))

            #os.listdir("files")
            #filename = input()

            f = open("src_files/" + filename, "rb") #r - open for reading, b - binary mode
            s.send(bytes(filename, 'utf-8') + (b'\0' *  (64 - len(filename) ))) # send over the file name so the server knows what file to save
            l = f.read(1024)
            while l:
                s.send(l)
                l = f.read(1024)
                print("Sending:", l)
                print(type(l))
                print(not not l)

if __name__ == "__main__":
    program = ClientApp()
    program.mainloop()
#Client
#Michael Brown

#Sources: https://www.w3schools.com/python/python_try_except.asp
#https://www.geeksforgeeks.org/command-line-arguments-in-python/
#https://stackoverflow.com/questions/6380057/python-binding-socket-address-already-in-use


import sys
import socket
import threading
import time

import http.server
import socketserver

port = 5087 #random port above 5000
#num = sys.argv[1] #due to instruction about server receiving out of range num, i will not check here it if is in range
#name = "Client of Michael J. Brown"
my_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create socket with ipv4 and tcp protocol

try:

    #Now connect the client to the socket
    my_sock.connect(("127.0.0.1", port)) #local host on port 5087

    #ISSUE A GET REQUEST FOR FILE FROM CLI ARGS
    #IN FORMAT HTTP/1.1
    msg = "Hello Server, send me that file. TODO"
    my_sock.sendall(msg.encode())


    server_data = my_sock.recv(1024).decode()

    if str(server_data) == "b''":
        pass

    else:

        server_data = server_data.strip().split()
        print(server_data)

except:
    print("Client error in making my socket")


my_sock.close()


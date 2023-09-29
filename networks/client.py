#Client
#Michael Brown

#Sources: https://www.w3schools.com/python/python_try_except.asp
#https://www.geeksforgeeks.org/command-line-arguments-in-python/
#https://stackoverflow.com/questions/6380057/python-binding-socket-address-already-in-use


import sys
import socket
import threading
import time

port = 5087 #random port above 5000
num = sys.argv[1] #due to instruction about server receiving out of range num, i will not check here it if is in range
name = "Client of Michael J. Brown"
my_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create socket with ipv4 and tcp protocol

try:

    #Now connect the client to the socket
    my_sock.connect(("127.0.0.1", port)) #local host on port 5087
    msg = name + " " + str(num)
    my_sock.sendall(msg.encode())

    server_data = my_sock.recv(1024).decode()

    if str(server_data) == "b''":
        pass

    else:

        server_data = server_data.strip().split()

        items_length = len(server_data)
        server_name = ""
        server_num = 0
        for i in range(0, items_length):

            if items_length - i > 1:
                # append string name
                server_name += server_data[i] + " "
            else:
                server_num = int(server_data[i])
        server_name.strip()

        print(name, "is communicating with the", server_name)
        print("Client number:", num)
        print("Server number:", server_num)
        print("Sum of values:", int(num) + int(server_num))

except:
    print("Client error in making my socket")


my_sock.close()


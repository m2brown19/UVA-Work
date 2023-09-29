#Michael Brown

#Sources: https://www.w3schools.com/python/python_try_except.asp
#https://www.google.com/search?q=socket+accept+function&oq=socket+accept+function&aqs=chrome..69i57j0i22i30l2j0i15i22i30i625j0i15i22i30j0i22i30l2j0i15i22i30i625j0i22i30j0i15i22i30.3309j0j1&sourceid=chrome&ie=UTF-8
#https://www.knowledgehut.com/tutorials/python-tutorial/python-socket-module
#Note, I realize this source has a lot of code on it and avoided looking at it and made it myself. It has a lot of good documentation
#though that helped teach me how a socket works b/w a client and server

#Similarly, I found a site with a helpful diagram on the order of how it should work
#https://realpython.com/python-sockets/
#it has a bunch of code on it too but i avoided looking at it. I didn't just look at the solution and copy it. I studied
#the diagram and researched functions about what they did and why

#https://eurion.net/python-snippets/snippet/Threaded%20Server.html


import sys
import socket
import threading
import time

port = 5087 #random port above 5000
name = "Server of Michael J. Brown"
server_num = 50
my_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create socket with ipv4 and tcp protocol

try:
    #bind the socket to port 5087 and the local host 127.0.0.1
    my_sock.bind(("127.0.0.1", port))

    # need the server to be listening on
    my_sock.listen(6)

    #ACCEPT UNTIL RECEIVE BAD INT
    accepting = True
    while (accepting == True):

        #Accept connections
        #first object reutnred is a socket object --- for new connection
        #2nd object is a tuple with  host and port?
        client, address = my_sock.accept() #Question -- what is the 2nd object returned?
        client_data = client.recv(1024).decode().strip().split() #must receive from client

        items_length = len(client_data)
        client_name = ""
        client_num = 0
        for i in range(0, items_length):

            if items_length - i > 1:
                #append string name
                client_name += client_data[i] + " "
            else:
                client_num = int(client_data[i])
        client_name.strip()

        #NOTE: II am assuming exclusive bounds b/w 1 and 100
        #1 and 100 are out therefore
        if client_num <= 1 or client_num >=100:
            #ASK IF OK TO SEND BAD
            client.send(("b''").encode())
            accepting = False #Bad int sent


        else:

            print("The", name, "is communicating with the", client_name)
            print("Client number:", client_num)
            print("Server number:", server_num)
            print("Sum of values", client_num + server_num)

            client.sendall((name + " " + str(server_num)).encode()) #send name and num to client


except:
    print("Server error in making my socket")

my_sock.close()
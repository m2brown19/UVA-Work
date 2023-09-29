#Michael Brown

#Sources: https://www.w3schools.com/python/python_try_except.asp
#https://www.google.com/search?q=socket+accept+function&oq=socket+accept+function&aqs=chrome..69i57j0i22i30l2j0i15i22i30i625j0i15i22i30j0i22i30l2j0i15i22i30i625j0i22i30j0i15i22i30.3309j0j1&sourceid=chrome&ie=UTF-8
#https://www.knowledgehut.com/tutorials/python-tutorial/python-socket-module
#https://www.freecodecamp.org/news/how-to-check-if-a-file-exists-in-python/#:~:text=The%20is_file()%20method%20checks,the%20file%20doesn't%20exist.&text=Since%20the%20example.,is_file()%20method%20returns%20True%20.
#Note, I realize this source has a lot of code on it and avoided looking at it and made it myself. It has a lot of good documentation
#though that helped teach me how a socket works b/w a client and server

#Similarly, I found a site with a helpful diagram on the order of how it should work
#https://realpython.com/python-sockets/
#it has a bunch of code on it too but i avoided looking at it. I didn't just look at the solution and copy it. I studied
#the diagram and researched functions about what they did and why

#https://eurion.net/python-snippets/snippet/Threaded%20Server.html
#https://docs.python.org/3/library/http.server.html


from os.path import exists
import sys
import socket
import threading
import time
import http.server
import socketserver


port = 6789 #random port above 5000
#name = "Server of Michael J. Brown"
#server_num = 50

#TODO ---- ensure output of server format is good enough...

#found snippet of code to start http server in documentation
#https://docs.python.org/3/library/http.server.html
#Handler = http.server.SimpleHTTPRequestHandler
#Handler.protocol_version = "HTTP/1.1"
#Handler.send_error(BaseHTTPRequestHandler, 404, "<html><head></head><body><h1>404 Not Found</h1></body></html>")
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:  # Create socket with ipv4 and tcp protocol

    # bind the socket to port 5087 and the local host 127.0.0.1
    sock.bind(("127.0.0.1", port))

    # need the server to be listening on
    sock.listen(6)
    while True:
        connection, address = sock.accept()
        try:
        ## get file request
            request = connection.recv(1024).decode()
            print(request)
            file_name = request.split(" ")[1][1:]
            print(file_name)
            with open(file_name) as f:
                file_content = f.readlines()
                connection.sendall(("HTTP/1.1 200 OK\r\n\r\n" + " ".join(file_content)).encode() )



        #If some exception
        except:
            # Through 404
            connection.sendall("HTTP/1.1 404 Not Found\r\n\r\n<html><head></head><body><h1>404 Not Found</h1></body></html>".encode())

        connection.close()

#
#     client_data = client.recv(1024).decode().strip().split()
#
#     if (exists("UVA.html")):
#         #GIVE TO CLIENT
#         #How to send to client
#         client.sendall(r'''HTTP/1.0 200 OK
# Content-Type: text/html
#
# '''.encode())
#         client.sendall("UVA.html")
#         pass
#     else:
#         #DO BNOT GIVE TO CLIENT. GIVE 404
#         client.sendall("<html><head></head><body><h1>404 Not Found</h1></body></html>".encode())
#         pass
#
#
#         #httpd.serve_forever()
#
#
#

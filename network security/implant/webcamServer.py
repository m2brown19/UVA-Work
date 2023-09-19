import socket
import ssl
from array import array
from select import select

import cv2
import numpy as np

client_cert = 'client.crt'
server_key = 'server.key'
server_cert = 'server.crt'
port = 8080

context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.verify_mode = ssl.CERT_REQUIRED

context.load_verify_locations(cafile=client_cert)
context.load_cert_chain(certfile=server_cert, keyfile=server_key)
context.options |= ssl.OP_SINGLE_ECDH_USE
context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1 | ssl.OP_NO_TLSv1_2


def recv_all(socket, length):
    response = b''
    total_bytes_remaining = length
    while total_bytes_remaining > 0:
        readable, writeable, error = select([socket], [], [])
        if socket in readable:
            data = socket.recv(total_bytes_remaining)
            response += data
            total_bytes_remaining -= len(data)
    return response

with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
    sock.bind(('', port))
    sock.listen(1)
    with context.wrap_socket(sock, server_side=True) as ssock:
        conn, addr = ssock.accept()
        while True:
            message = recv_all(conn, 921600)
            frame = np.frombuffer(message, dtype=np.uint8).reshape((480, 640, 3))
            cv2.imshow("WebCamServer", frame)
            cv2.waitKey(20)


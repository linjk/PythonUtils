# --*- coding: utf-8 -*-

import socket
import threading

bind_ip   = "0.0.0.0"
bind_port = 3333

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((bind_ip, bind_port))
#maximum connection
server.listen(5)

print "[*]Listening on %s:%d" % (bind_ip, bind_port)

#客户处理线程
def handle_client(client_socket):
    request = client_socket.recv(1024)
    #print "[*]Received: %s" % request
    print "[*]Received length: %d" % len(request)

    #if "{:02X}".format(ord(c) for c in request) == 16:
    print "[*]Recv Data:"
    print " ".join("{:02X}".format(ord(c)) for c in request)

    print "[*]Send <ACK!> to client."
    client_socket.send("ACK!")
    print "[*]Connection close."
    print "---------------------------------"
    client_socket.close()


while True:
    client, addr = server.accept()
    print "[*]Accepted connection from: %s:%d" % (addr[0], addr[1])

    client_handler = threading.Thread(target=handle_client, args=(client,))
    client_handler.start()

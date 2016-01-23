# -*- coding: utf-8 -*-
import socket

target_host = "127.0.0.1"
target_port = 3333

#建立一个socker对象
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect((target_host, target_port))

client.send("GET / HTTP/1.1\r\n Host:127.0.0.1\r\n\r\nHELLO")

response = client.recv(4096)

print response

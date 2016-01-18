# -*- coding: utf-8 -*-
# Test env: Mac OS X 10.11.1
# run in server mode: python2.7 jimNetcat -l -p 1234 -c
# run in client mode: python2.7 -t localhost -p 1234
# 模拟了SSH远程登录!
import sys
import socket
import getopt
import threading
import subprocess

# Global vars
listen             = False
command            = False
upload             = False
execute            = ""
target             = ""
upload_destination = ""
port               = 0

def run_command(command):
    #换行
    command = command.rstrip()
    #运行命令并将输出返回
    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
    except:
        output = "Failed to execute command.\r\n"

    return output

def client_handler(clisnt_socket):
    global upload
    global execute
    global command

    #检测上传文件
    if len(upload_destination):
        file_buffer = ""

        while True:
            data = clisnt_socket.recv(1024)

            if not data:
                break
            else:
                file_buffer += data

        #接收数据并写出来
        try:
            file_descriptor = open(upload_destination, "wb")
            file_descriptor.write(file_buffer)
            file_descriptor.close()

            clisnt_socket.send("Successfully saved file to %s\r\n" % upload_destination)
        except:
            clisnt_socket.send("Failed to save file to %s\r\n" % upload_destination)

    #检测命令执行
    if len(execute):
        output = run_command(execute)
        clisnt_socket.send(output)

    #如果需要一个命令行shell
    if command:
        while True:
            clisnt_socket.send("<JIM:#> ")

            cmd_buffer = ""
            while "\n" not in cmd_buffer:
                cmd_buffer += clisnt_socket.recv(1024)

            response = run_command(cmd_buffer)
            clisnt_socket.send(response)

def server_loop():
    global target
    global port

    #如果没有定义目标,则监听所有接口
    if not len(target):
        target = "0.0.0.0"

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((target, port))

    server.listen(5)

    while(True):
        client_socket, addr = server.accept()

        client_thread = threading.Thread(target=client_handler, args=(client_socket,))
        client_thread.start()

def client_sender(buffer):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect((target, port))

        if len(buffer):
            client.send(buffer)

        while True:
            #等待数据回传
            recv_len = 1
            response = ""

            while recv_len:
                data = client.recv(4096)
                recv_len = len(data)
                response += data

                if recv_len < 4096:
                    break
            print response,

            #等待更多输入
            buffer = raw_input("")
            buffer += "\n"

            client.send(buffer)

    except:
        print "[*]Ecxeption! Exiting."
    client.close()

def usage():
    print "JIM Net Tool"
    print
    print "Usage: jimNetcat.py -t target_host -p port"
    print "-l --listen                - listen on [host]:[port] for incoming connections"
    print "-e --execute=file_to_run   - execute the given file upon receiving a connection"
    print "-c --command               - initialize a command shell"
    print "-u --upload=destination    - upon receiving connection upload a file and write to [destination]"
    print
    print
    print "Examples:"
    print "jimNetcat.py -t 192.168.0.1 -p 5555 -l -c"
    print "jimNetcat.py -t 192.168.0.1 -p 5555 -l -u=C:\\target..exe"
    print "jimNetcat.py -t 192.168.0.1 -p 5555 -l -e=\"cat /etc/passwd\""
    print "echo 'ABCDDEFGHI' | ./jimNetcat.py -t 192.168.0.1 -p 135"
    sys.exit(0)

def main():
    global listen
    global port
    global execute
    global command
    global upload_destination
    global target

    if not len(sys.argv[1:]):
        usage()

    #读取命令行选项
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hle:t:p:cu:",
                                   ["help", "listen", "execute", "target", "port", "command", "upload"])
    except getopt.GetoptError as err:
        print str(err)
        usage()

    for o,a in opts:
        if o in ("-h", "--help"):
            usage()
        elif o in ("-l", "--listen"):
            listen = True
        elif o in ("-e", "--execute"):
            execute = a
        elif o in ("-c", "--commandshell"):
            command = True
        elif o in ("-u", "--upload"):
            upload_destination = a
        elif o in ("-t", "--target"):
            target = a
        elif o in ("-p", "--port"):
            port = int(a)
        else:
            assert False, "Unhandled Option"

    if not listen and len(target) and port > 0:
        #这里阻塞,在不向标准输入发送数据时发送CTRL - D
        buffer = sys.stdin.read()
        client_sender(buffer)

    if listen:
        server_loop()

main()
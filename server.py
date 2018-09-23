import socket
from threading import Thread
import time

clients = {}
addresses = {}

HOST = ''
PORT = 16540
BUFSIZE = 2048
ADDR = (HOST, PORT)
serverSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serverSock.bind(ADDR)

serverSock.listen()

def acceptConnections():
    """Sets up handling for incoming connections"""
    print("accepting connections")
    while True:
        client, client_address = serverSock.accept()
        print("{} has connectied.".format(client_address))
        client.send(bytes("Hello there!"+"Now type your name and press enter!", "utf8"))
        addresses[client] = client_address
        Thread(target=handleClient, args=(client,)).start()
        time.sleep(0.5)

def handleClient(clientSock):
    """Handles a single client"""
    name = clientSock.recv(BUFSIZE).decode("utf8")
    welcome = 'Welcome {}! If you ever want to quit, type \quit to exit'.format(name)
    clientSock.send(bytes(welcome, "utf8"))
    msg = "{} has joined the chat!".format(name)
    broadcast(bytes(msg, "utf8"))
    clients[clientSock] = name
    while True:
        msg = clientSock.recv(BUFSIZE)
        if msg != bytes("\quit", "utf8"):
            broadcast(msg, name+": ")
        else:
            clientSock.send(bytes("\quit", "utf8"))
            clientSock.close()
            del addresses[clientSock]
            del clients[clientSock]
            broadcast(bytes("{} has left.".format(name), "utf8"))
            break

def broadcast(msg, prefix=""):
    """Broadcasts a message to all other chat participants"""
    print(prefix + msg.decode("utf8"))
    for sock in clients:
        sock.send(bytes(prefix, "utf8")+msg)

if __name__ == "__main__":
    serverSock.listen(5)
    print("Waiting for connections")
    acceptThread = Thread(target=acceptConnections)
    acceptThread.start()
    try:
        acceptThread.join()
    except KeyboardInterrupt:
        serverSock.close()

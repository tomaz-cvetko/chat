import socket
from threading import Thread, Event, Lock
import time

msgList = []
mutex = Lock()
shutdownEvent = Event()

HOST = ''
PORT = 16540
BUFSIZE = 2048
ADDR = (HOST, PORT)
clientSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSock.connect(ADDR)

def receiveFromServer():
    while not shutdownEvent.is_set():
        try:
            mutex.acquire()
            serverMsg = clientSock.recv(BUFSIZE).decode("utf8")
            print(serverMsg)
            msgList.append(serverMsg)
            mutex.release()
            time.sleep(1)
        except socket.timeout:
            # no problem
            mutex.release()
            time.sleep(1)


def sendInput():
    while not shutdownEvent.is_set():
        my_msg = input(">$ ")
        mutex.acquire()
        print("sending")
        msgList.append(my_msg)
        clientSock.send(bytes(my_msg, "utf8"))
        mutex.release()
        
        if my_msg == "\quit":
            shutdownEvent.set()
        else:
            time.sleep(0.1)


def startCommunication():
    serverMsg = clientSock.recv(BUFSIZE).decode("utf8")
    print(serverMsg)
    msgList.append(serverMsg)
    
    msg = input(">$ ")
    msgList.append(msg)
    clientSock.send(bytes(msg, "utf8"))
    
    serverMsg = clientSock.recv(BUFSIZE).decode("utf8")
    print(serverMsg)
    msgList.append(serverMsg)
    
    clientSock.settimeout(0.1)
    
    receiveThread = Thread(target=receiveFromServer)
    receiveThread.start()
    
    sendInput()

startCommunication()

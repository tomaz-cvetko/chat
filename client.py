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
            # this blocks for timeout period, so it takes some time
            serverMsg = clientSock.recv(BUFSIZE).decode("utf8")
            print("\r"+serverMsg+"\n>$", end='')
            msgList.append(serverMsg)
            mutex.release()
            time.sleep(1)
        except socket.timeout:
            # no problem
            mutex.release()
            time.sleep(1)


def sendInput():
    while not shutdownEvent.is_set():
        # this blocks in one thread. if input is received,
        # message is sent quickly -> socket is used for a short time
        my_msg = input(">$ ")
        mutex.acquire()
        msgList.append(my_msg)
        clientSock.send(bytes(my_msg, "utf8"))
        mutex.release()
        
        if my_msg == "\quit":
            shutdownEvent.set()
        else:
            #time.sleep(0.1)
            continue


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
    
    clientSock.settimeout(0.05)
    
    receiveThread = Thread(target=receiveFromServer)
    receiveThread.start()
    
    sendInput()

startCommunication()

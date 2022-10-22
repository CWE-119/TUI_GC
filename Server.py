import socket

import threading

from matplotlib import pyplot as plt
import numpy as np

host = "26.105.253.103"
# do not take any reserved or well known ports
port = 6969

# server = socket.gethostbyname(socket.gethostname())
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# socket.AF_INET = this tells us what type of socket or address we are looking for the specific connection
#  socket.SOCK_STREAM = this means we are streaming data to the socket
server.bind((host, port))
server.listen()

clients = []
nicknames = []
nicknames2 = []


# broadcasting messages from the server to all the clients
def broadcast(message):

    for client in clients:
        client.send(message)


# saves the nicknames of the server
def clientCount(n):
    if len(nicknames) == 0:
        # print(nicknames2)
        with open('userList.txt', 'w') as filehandle:
            for f in nicknames2:
                filehandle.write(f'{f}\n')
    else:
        print("Nothing!")


# brand names collection
brandName = {"bmw": 0, "toyota": 0}
xLevel = []
yLevel = []


def handle(client):
    # blacklist of words
    blacklist = ["male", "female", "Hindu", " Muslim", "Christian", "BMP", "Awami league"]
    # brand names
    y = xLevel
    x = yLevel
    while True:
        try:
            # receiving 1024 bytes
            message = client.recv(1024)
            message1 = message.decode('ascii')
            message1 = message1.split(" ")
            # print(message1)  # to check the list
            for i in message1:
                if i in blacklist:
                    index = message1.index(i)
                    message1[index] = "*" * len(i)
                for brand in brandName:
                    if brand in message1:
                        brandName[brand] += 1
                        x.append(brandName[brand])
                        y.append(brand)
                # call of the brand
                if i == "/sd":
                    brandNamesDataDisplay()
            message = " ".join(message1)

            # data needs to be in bytes
            message = message.encode("ascii")

            broadcast(message)  # broadcast takes bytes to broadcast

        except:
            # find out the index of the failed client frm the clients list
            index = clients.index(client)
            clients.remove(client)
            client.close()
            # we also remove the nickname of the removed client
            nickname = nicknames[index]
            broadcast(f"{nickname} left the chat!".encode('ascii'))
            nicknames.remove(nickname)
            break


# data graph show of brand names  (currently off)
def brandNamesDataDisplay():
    x = np.array(xLevel)
    y = np.array(yLevel)
    plt.bar(x, y)
    plt.show()
    print(brandName)


def receive():
    while True:
        print("receive function is running on the server!")
        # returns a tuple
        client, address = server.accept()

        # you have cut down the address str type casting
        print(f"Connected with {str(address)}")

        # we need to ask the client for the nickname
        # made change here
        name = "NICK"
        client.send(name.encode('ascii'))

        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        nicknames2.append(nickname)
        clients.append(client)

        print(f"Nickname of the client is {nickname}")

        broadcast(f"[NEW CONNECTION] {nickname} connected".encode('ascii'))
        # letting know the specific client that it has connected to the server
        client.send("Connected to the server".encode('ascii'))

        # define and run a thread
        # because we want to be able to handle multi clients same time

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()
        # this shows hom many threads are active , each thread represent each client
        # 2 thread are constantly running so, I have to subtract 2 thread
        threadCount = threading.active_count()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 2}")
        if threadCount == 0:
            print("there is no-one in the server")

# main method
print("[STARTING]  is listening..........")
# receiving on another thread because matplotlib need to run on main thread or it crashes
t = threading.Thread(target=receive)
t.start()

# brandNamesDataDisplay()

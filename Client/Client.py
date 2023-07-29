import socket
import threading

from matplotlib import pyplot as plt
import numpy as np

# serverIp = str(input("Enter the server IP: "))
serverIp = "127.0.0.1"
print(serverIp)
# serverPort = int(input("Enter the server port: "))
serverPort = 6969
nickname = input("Choose your nickname before joining server: ")
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# this is the ip of the server that we want to connect to
client.connect((serverIp, serverPort))


def receive():
    while True:
        try:
            # receiving from the server
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send(nickname.encode('ascii'))

            else:
                print(message)

        except:
            (print("An error Occurred!"))
            client.close()
            break


# brand names collection
brandName = {"bmw": 0, "toyota": 0}
xLevel = []
yLevel = []


def write():
    yl = xLevel
    xl = yLevel
    while True:
        message = f'{nickname}: {input("")}'
        cMessage1 = message.split(" ")
        for i in cMessage1:
            for brand in brandName:
                if brand in cMessage1:
                    brandName[brand] += 1
                    xl.append(brandName[brand])
                    yl.append(brand)
            # call of the brand
            if i == "/csd":
                cBrandNamesDataDisplay()
        client.send(message.encode('ascii'))


def cBrandNamesDataDisplay():
    # sleep(20)
    xl = np.array(xLevel)
    yl = np.array(yLevel)
    plt.bar(xl, yl)
    plt.show()
    print(brandName)


# we are running 2 threads receive thread and to write thread


# the thread for receiving
receive_thread = threading.Thread(target=receive)
receive_thread.start()

# the thread for writing
write_thread = threading.Thread(target=write)
write_thread.start()

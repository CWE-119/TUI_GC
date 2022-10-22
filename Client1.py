import socket
import threading


# serverIp = str(input("Enter the server IP: "))
serverIp = "26.105.253.103"
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


def write():
    while True:
        message = f'{nickname}: {input("")}'
        client.send(message.encode('ascii'))


# we are running 2 threads receive thread and to write thread


# the thread for receiving
receive_thread = threading.Thread(target=receive)
receive_thread.start()

# the thread for writing
write_thread = threading.Thread(target=write)
write_thread.start()

import socket
from client_options import OPTION
from _thread import *

ServerSideSocket = socket.socket()
host = '127.0.0.1'
port = 2005
ThreadCount = -1
UTF8 = 'utf-8'

users = []

ServerSideSocket.bind((host, port))
print('Socket is listening..')
ServerSideSocket.listen(5)

online_clients = dict()


def multi_threaded_client(connection, add):
    # send to client Server is working
    connection.send(str.encode('Server is working:'))
    # wait for client to send his id
    client_name = connection.recv(1024).decode(UTF8)
    users.append([ThreadCount,client_name,connection])
    connection.send(str.encode(str(ThreadCount))) #send id to client

    # start chatting
    while True:
        data = connection.recv(2048)
        if not data:
            continue
        response = ''
        arr = data.decode(UTF8).split('|')
        # split the request from the client
        # structure is [0] client id | [1] option asked
        print(data.decode(UTF8))
        if arr[1] == OPTION.LIST_ONLINE_USERS.value:
            print('sending online users to client')
            array_of_keys = []
            listOfUsers = ''
            for user in users:
                listOfUsers +=  'name: ' + user[1] +'    '+ 'id: ' + str(user[0]) + '\n'
            connection.sendall(str.encode(listOfUsers))

        elif arr[1] == OPTION.SEND_MESSAGE_TO_USER.value:
            # client has chosen to send message to other client, so we have to get the other client connection from
            # the dictionary and send the message to it
            # structure is [0] client id | [1] option asked | [2] id of the receiver client  | [3] message
            reciverCon = users[int(arr[2])][2]
            message = 'Message from: ' + users[int(arr[0])][1] +'\nMessage content: '+ arr[3];
            reciverCon.sendall(str.encode(message))

        elif arr[1] == OPTION.CLOSE_CONNECTION.value:
            print('client is asking to close the connection')
            break
        elif arr[1] == OPTION.SHOW_MESSAGES.value:
            Client.send(str.encode('  '))

        # connection.sendall(str.encode(response))
    del online_clients[client_id]
    connection.close()


while True:
    Client, address = ServerSideSocket.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    # start new thread
    start_new_thread(multi_threaded_client, (Client, address))
    ThreadCount += 1
    print('Thread Number: ' + str(ThreadCount))
ServerSideSocket.close()

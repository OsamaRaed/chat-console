import socket
from client_options import OPTION
from _thread import *

ServerSideSocket = socket.socket()
host = '127.0.0.1'
port = 2004
ThreadCount = 0
UTF8 = 'utf-8'

ServerSideSocket.bind((host, port))
print('Socket is listening..')
ServerSideSocket.listen(5)

online_clients = dict()


def multi_threaded_client(connection, add):
    # send to client Server is working
    connection.send(str.encode('Server is working:'))
    # wait for client to send his id
    client_id = Client.recv(1024).decode(UTF8)
    online_clients[client_id] = Client
    # print('client id:', client_id)
    # print here the online clients on the server each new connection
    array_of_keys_in_server = []
    online = ''
    for k in online_clients.keys():
        array_of_keys_in_server.append(k)
    for i in range(len(array_of_keys_in_server)):
        online = online + '\nonline id: ' + str(array_of_keys_in_server[i])
    print(online)

    # start chatting
    while True:
        data = connection.recv(2048)
        if not data:
            continue
        response = ''
        arr = data.decode(UTF8).split('|')
        # split the request from the client
        # structure is [0] client id | [1] option asked
        print(arr)
        if arr[1] == OPTION.LIST_ONLINE_USERS.value:
            print('sending online users to client')
            array_of_keys = []
            for k in online_clients.keys():
                array_of_keys.append(k)
            for i in range(len(array_of_keys)):
                if array_of_keys[i] != arr[0]:
                    response = response + '\nclient id: ' + str(array_of_keys[i])
                else:
                    response = response + '\nYOU!!'
            connection.sendall(str.encode(response))

        elif arr[1] == OPTION.SEND_MESSAGE_TO_USER.value:
            # client has chosen to send message to other client, so we have to get the other client connection from
            # the dictionary and send the message to it
            # structure is [0] client id | [1] option asked | [2] id of the receiver client  | [3] message
            client = online_clients[arr[2]]
            client.sendall(str.encode('msg' + '|' + arr[3]))

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

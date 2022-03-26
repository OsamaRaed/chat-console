import socket
from _thread import *

ServerSideSocket = socket.socket()
host = '127.0.0.1'
port = 2004
ThreadCount = 0
ServerSideSocket.bind((host, port))
print('Socket is listening..')
ServerSideSocket.listen(5)

online_clients = dict()


def multi_threaded_client(connection, add):
    connection.send(str.encode('Server is working:'))
    while True:
        data = connection.recv(2048)
        response = ''
        arr = data.decode('utf-8').split('|')
        # print(arr)
        # print(online_clients)
        if arr[1] == '1':
            online_clients[arr[0]] = connection
            array_of_keys = []
            for k in online_clients.keys():
                array_of_keys.append(k)
            # print(online_clients)
            for i in range(len(array_of_keys)):
                if array_of_keys[i] != arr[0]:
                    response = response + '\nclient ' + str(i) + ' ' + str(array_of_keys[i])
                    # print('A')
        elif arr[1] == '2':
            client = online_clients[arr[2]]
            client.sendall(str.encode("test"))
        response = response + '\nServer message: ' + data.decode('utf-8')
        if data.decode('utf-8') == '2':
            break
        if not data:
            break
        connection.sendall(str.encode(response))
    x = online_clients.pop(str(add[1]))
    print(x)
    connection.close()


while True:
    Client, address = ServerSideSocket.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    start_new_thread(multi_threaded_client, (Client, address))
    ThreadCount += 1
    print('Thread Number: ' + str(ThreadCount))
ServerSideSocket.close()

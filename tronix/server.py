import socket
from client_options import OPTION
from _thread import *
import os


ServerSideSocket = socket.socket()
host = '127.0.0.1'
port = 2005
ThreadCount = -1
UTF8 = 'utf-8'
SEPARATOR = "<SEPARATOR>"
users = []
groups = []

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
        data = connection.recv(1024)
        if not data:
            continue
        response = ''
        arr = data.decode(UTF8).split('|')
        if arr[1] == OPTION.SEND_FILE_TO_USER.value:
            reciverCon = users[int(arr[2])][2]

            filename = connection.recv(1024).decode()
            filename = os.path.basename(filename)
            message = 'File from: ' + users[int(arr[0])][1] + '|' +filename
            reciverCon.sendall(message.encode(UTF8))


            while True:
                # read 1024 bytes from the socket (receive)
                bytes_read = connection.recv(4086)
                if bytes_read == '':
                    break
                reciverCon.sendall(bytes_read)
            reciverCon.sendall(''.encode(UTF8))

        elif arr[1] == OPTION.LIST_ONLINE_USERS.value:
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

        elif arr[1] == OPTION.LIST_CURRENT_GROUPS.value:
            id = 0
            temp = ''
            for x in groups:
                temp += 'Group ' + str(id) + ': '
                for y in x:
                    temp += users[y][1] + '   '
                temp += '\n'
                id+=1
            connection.sendall(str.encode(temp))

        elif arr[1] == OPTION.CREATE_GROUP.value:
            temp = [];
            temp.append(int(arr[0]))
            for x in arr[2].split(" "):
                temp.append(int(x))
            groups.append(set(temp))
            print(groups)
            for x in groups:
                for y in x:
                    print(y)

        elif arr[1] == OPTION.JOIN_GROUP.value:
            groups[int(arr[2])].add(int(arr[0]))

        elif arr[1] == OPTION.SEND_MESSAGE_TO_GROUP.value:
            reciver_group = int(arr[2])
            message = 'Message from ' + users[int(arr[0])][1] + ' in group ' + str(reciver_group) + '\nMessage content: ' + arr[3];
            for x in groups[reciver_group]:
                if x == int(arr[0]):
                    continue
                users[x][2].sendall(str.encode(message))

        elif arr[1] == OPTION.BROADCAST_MESSAGE.value:
            message = users[int(arr[0])][1] + ' broadcasts: ' + '\nMessage content: ' + arr[2];
            for x in users:
                if x[0] == int(arr[0]):
                    continue
                x[2].sendall(str.encode(message))

        elif arr[1] == OPTION.CLOSE_CONNECTION.value:
            del users[int(arr[0])]
            print('client'+arr[0]+' is asking to close the connection')
            break


    connection.close()


while True:
    Client, address = ServerSideSocket.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    # start new thread
    start_new_thread(multi_threaded_client, (Client, address))
    ThreadCount += 1
    print('Thread Number: ' + str(ThreadCount))
ServerSideSocket.close()

import socket
from client_options import OPTION
from _thread import *
import sys
import time

ClientMultiSocket = socket.socket()
a_lock = allocate_lock()

host = '127.0.0.1'
port = 2005
name = 'Osama'
UTF8 = 'utf-8'
DASHES = '------------'

print('Waiting for connection response')
ClientMultiSocket.connect((host, port))
# receive Server is working
res = ClientMultiSocket.recv(1024)
print(res.decode(UTF8))
ClientMultiSocket.send(str.encode(name))
id = ClientMultiSocket.recv(1024).decode(UTF8)


def thread_listener(connection):
    while True:
        r_msg = connection.recv(1024)
        if not r_msg:
            continue

        r_msg = r_msg.decode('utf-8')
        if (r_msg.split(' ')[0] == 'File'):
            filename = 'new ' + r_msg.split('|')[1]

            with open(filename, "w") as f:
                while True:
                    # read 1024 bytes from the socket (receive)
                    bytes_read = connection.recv(1024)
                    bytes_read = bytes_read.decode(UTF8)
                    if bytes_read == 'stop':
                        break

                    f.write(bytes_read)
                f.close()


        print(DASHES)
        print('Notification message: ')
        print(r_msg)
        print(DASHES)


args = [ClientMultiSocket]
start_new_thread(thread_listener, tuple(args))

while True:
    time.sleep(0.5)
    print(
        'List of functionalities\n',
        '1) List online users\n',
        '2) List all groups\n',
        '3) Send message to user\n',
        '4) Create group\n',
        '5) Join group\n',
        '6) send message to group\n',
        '7) Broadcast message\n',
        '8) Send File to user\n',
        '9) close connection'

    )
    Input = input('Enter your choice: ')

    # option 1 is about listening online users
    if Input == OPTION.LIST_ONLINE_USERS.value:
        print('receiving online users from the server')
        # structure id [0] | cmd [1]
        ClientMultiSocket.send(str.encode(str(id) + '|' + str(OPTION.LIST_ONLINE_USERS.value)))
        # structure id [0] | cmd [1]
    elif Input == OPTION.LIST_CURRENT_GROUPS.value:
        ClientMultiSocket.send(str.encode(str(id) + '|' + str(OPTION.LIST_CURRENT_GROUPS.value)))


    elif Input == OPTION.SEND_MESSAGE_TO_USER.value:
        reciver_id = input('choose user id: ')
        while True:
            msg = input('Write your message: ')
            if msg == 'end':
                break
            # structure is [0] client id | [1] option asked | [2] id of the receiver client  | [3] message
            temp = str(id) + '|' + OPTION.SEND_MESSAGE_TO_USER.value + '|' + reciver_id + '|' + msg
            ClientMultiSocket.send(str.encode(temp))
            print('sent')
        print(DASHES)

    elif Input == OPTION.CREATE_GROUP.value:
        participants = input('Enter participants ID\'s separated by space: ')
        # structure is [0] client id | [1] option asked | [2] id's of the participants client
        temp = str(id) + '|' + OPTION.CREATE_GROUP.value + '|' + participants
        ClientMultiSocket.send(str.encode(temp))
        print('--Group created--')

    elif Input == OPTION.JOIN_GROUP.value:
        group_id = input('Enter group ID you want to join: ')
        # structure is [0] client id | [1] option asked | [2] group id
        temp = str(id) + '|' + OPTION.JOIN_GROUP.value + '|' + group_id
        ClientMultiSocket.send(str.encode(temp))
        print('--You joined to group ' + group_id + '--')
    elif Input == OPTION.SEND_MESSAGE_TO_GROUP.value:
        group_id = input('Choose group id: ')
        while True:
            msg = input('Write your message: ')
            if msg == 'end':
                break
            # structure is [0] client id | [1] option asked | [2] id of the receiver client  | [3] message
            temp = str(id) + '|' + OPTION.SEND_MESSAGE_TO_GROUP.value + '|' + group_id + '|' + msg
            ClientMultiSocket.send(str.encode(temp))
            print('sent')
        print(DASHES)
    elif Input == OPTION.BROADCAST_MESSAGE.value:
        msg = input('Write your message: ')
        # structure is [0] client id | [1] option asked | [2] message
        temp = str(id) + '|' + OPTION.BROADCAST_MESSAGE.value + '|' + msg
        ClientMultiSocket.send(str.encode(temp))
        print('sent')
        print(DASHES)

    elif Input == OPTION.SEND_FILE_TO_USER.value:
        reciver_id = input('choose user id: ')
        filename = input('Enter file name: ')
        ClientMultiSocket.send(str.encode(id + '|' + OPTION.SEND_FILE_TO_USER.value + '|' + reciver_id))
        ClientMultiSocket.send(filename.encode())
        with open(filename, "r") as f:
            while True:
                # read the bytes from the file
                bytes_read = f.read(1024)
                if not bytes_read:
                    break

                ClientMultiSocket.sendall(bytes_read.encode(UTF8))
            f.close()
        ClientMultiSocket.sendall('stop'.encode(UTF8))
        print('--File Send Successfully--')

    elif Input == OPTION.CLOSE_CONNECTION.value:
        ClientMultiSocket.send(str.encode(id + '|' + OPTION.CLOSE_CONNECTION.value))
        sys.exit('closing the connection')

ClientMultiSocket.close()

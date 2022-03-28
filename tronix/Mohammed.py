import socket
from client_options import OPTION
from _thread import *
import sys

ClientMultiSocket = socket.socket()
a_lock = allocate_lock()

host = '127.0.0.1'
port = 2005
name = 'Mohammed'
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

        print(DASHES)
        print('notification message: \n',r_msg)
        print(DASHES)


args = [ClientMultiSocket]
start_new_thread(thread_listener, tuple(args))

# def recive():
#     return ClientMultiSocket.recv(1024)

while True:
    print(
        'list of functionalities\n',
        '1) list of online users\n',
        '2) message user\n',
        '3) create group\n',
        '6) show messages\n',
        '7) close connection'
    )
    Input = input('ur choice: ')

    # option 1 is about listening online users
    if Input == OPTION.LIST_ONLINE_USERS.value:
        print('receiving online users from the server')
        # structure id | cmd
        ClientMultiSocket.send(str.encode(str(id) + '|' + str(OPTION.LIST_ONLINE_USERS.value)))

    # option 2 is about sending to other user
    elif Input == OPTION.SEND_MESSAGE_TO_USER.value:
        ClientMultiSocket.send(str.encode(str(id) + '|' + str(OPTION.LIST_ONLINE_USERS.value)))


        reciver_id = input('choose user id: ')
        while (True):
            msg = input('Write your message: ')
            if(msg == 'end'):
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

    elif Input == OPTION.SEND_MESSAGE_TO_GROUP.value:
        group_id = input('Choose group id: ')
        while (True):
            msg = input('Write your message: ')
            if(msg == 'end'):
                break
            # structure is [0] client id | [1] option asked | [2] id of the receiver client  | [3] message
            temp = str(id) + '|' + OPTION.SEND_MESSAGE_TO_GROUP.value + '|' + group_id + '|' + msg
            ClientMultiSocket.send(str.encode(temp))
            print('sent')
        print(DASHES)

    # option 7 will send request to close the connection
    elif Input == OPTION.CLOSE_CONNECTION.value:
        ClientMultiSocket.send(str.encode(id + '|' + OPTION.CLOSE_CONNECTION.value))
        sys.exit('closing the connection')
ClientMultiSocket.close()



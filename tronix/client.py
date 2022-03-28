import socket
from client_options import OPTION
from _thread import *
import sys

ClientMultiSocket = socket.socket()
# ClientMultiSocket.setblocking(0)
a_lock = allocate_lock()

host = '127.0.0.1'
port = 2004
id = '1'
UTF8 = 'utf-8'
DASHES = '------------'

print('Waiting for connection response')
ClientMultiSocket.connect((host, port))
# receive Server is working
res = ClientMultiSocket.recv(1024)
print(res.decode(UTF8))
ClientMultiSocket.send(str.encode(id))

while True:
    print(
        'list of functionalities\n',
        '1) list of online users\n',
        '2) message user\n',
        '6) show messages\n',
        '7) close connection'
    )
    Input = input('ur choice: ')

    # option 1 is about listening online users
    if Input == OPTION.LIST_ONLINE_USERS.value:
        print('receiving online users from the server')
        # structure id | cmd
        ClientMultiSocket.send(str.encode(id + '|' + str(OPTION.LIST_ONLINE_USERS.value)))
        res = ClientMultiSocket.recv(1024)
        print(DASHES)
        print(res.decode(UTF8))
        print(DASHES)
    # option 2 is about sending to other user
    elif Input == OPTION.SEND_MESSAGE_TO_USER.value:
        ClientMultiSocket.send(str.encode(id + '|' + str(OPTION.LIST_ONLINE_USERS.value)))
        res = ClientMultiSocket.recv(1024)
        print(DASHES, '\nonline users')
        print(res.decode(UTF8))
        print(DASHES)
        Input = input('choose user id: ')
        msg = input('write ur message: ')
        # structure is [0] client id | [1] option asked | [2] id of the receiver client  | [3] message
        ClientMultiSocket.send(str.encode(id + '|' + OPTION.SEND_MESSAGE_TO_USER.value + '|' + Input + '|' + msg))
        print('message sent!!')
        print(DASHES)
    # option 6 will show messages
    elif Input == OPTION.SHOW_MESSAGES.value:
        ClientMultiSocket.send(str.encode(id + '|' + OPTION.SHOW_MESSAGES.value))
        data = ClientMultiSocket.recv(1024)
        print(DASHES)
        print(data.decode(UTF8))
        print(DASHES)
        print()
    # option 7 will send request to close the connection
    elif Input == OPTION.CLOSE_CONNECTION.value:
        ClientMultiSocket.send(str.encode(id + '|' + OPTION.CLOSE_CONNECTION.value))
        sys.exit('closing the connection')
ClientMultiSocket.close()

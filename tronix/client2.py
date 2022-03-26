import socket
ClientMultiSocket = socket.socket()
host = '127.0.0.1'
port = 2004

id = '4'
print('Waiting for connection response')
try:
    ClientMultiSocket.connect((host, port))
except socket.error as e:
    print(str(e))
res = ClientMultiSocket.recv(1024)
while True:
    print('list of functionalities\n 1) list of online users\n 2) message user')
    Input = input('ur choice: ')
    if Input == '1':
        ClientMultiSocket.send(str.encode(id + '|' + '1'))
    elif Input == '2':
        ClientMultiSocket.send(str.encode(id + '|' + '1'))
        res = ClientMultiSocket.recv(1024)
        print(res.decode('utf-8'))
        client_id = input('Enter user id')
        msg = input('Enter the message')
        ClientMultiSocket.send(str.encode(id + '|' + '2' + '|' + client_id + '|' + msg))

    res = ClientMultiSocket.recv(1024)
    print(res.decode('utf-8'))
ClientMultiSocket.close()
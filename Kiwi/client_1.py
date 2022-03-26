import socket

serverName = '127.0.0.1'
serverPort = 12345
while 1:

    sentence = input('Enter message to the server: ')
    if sentence == 'close':
        break
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((serverName, serverPort))
    s.sendall(str.encode(sentence))
    data = s.recv(1024)
    s.close()
    print('Received', repr(data))

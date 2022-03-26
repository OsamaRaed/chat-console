from socket import *

serverName = '127.0.0.1'
serverPort = 12000

while 1:
    sentence = input('Input lowercase sentence:')
    if sentence == 'close':
        break
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName, serverPort))

    clientSocket.send(sentence)
    modifiedSentence = clientSocket.recv(1024)
    clientSocket.close()

    print('From Server:', modifiedSentence)

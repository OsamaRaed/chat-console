from socket import *
import threading

serverPort = 12000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)
print('The server is ready to receive')


def handleClient(accepted):
    connectionSocket, addr = accepted
    sentence = connectionSocket.recv(1024)
    capitalizedSentence = sentence.upper()
    print(capitalizedSentence)
    connectionSocket.send(capitalizedSentence)
    connectionSocket.close()


while 1:
    clientThread = threading.Thread(handleClient(serverSocket.accept()))






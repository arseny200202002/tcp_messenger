import socket
from server_config import *

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_HOST, SERVER_PORT))

def client_hanler(client_socket):
    while True:
        print('type your message: ')
        request = input()
        request = request.encode('utf-8')
        client_socket.sendall(request)
        answer = client_socket.recv(4096)
        answer = answer.decode('utf-8')
        print(answer)

if __name__ == "__main__":
    client_hanler(client_socket)
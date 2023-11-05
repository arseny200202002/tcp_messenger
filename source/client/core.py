import socket
import configparser

from client_logic import requests
from client_logic import answer_templates

def client_handler(host, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    client_socket.sendall(requests.initialization_request())
    answer = client_socket.recv(1024)

    while True:
        # input part
        print('type your message: ')
        request = input()
        request = request.encode('utf-8')
        # send request
        client_socket.sendall(request)
        # receive answer 
        answer = client_socket.recv(1024)
        answer = answer.decode('utf-8')
        print(answer)
        # prosess answer


if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read("server_config.ini")

    #print(config["SERVER"]["SERVER_HOST"])
    client_handler(config["SERVER"]["SERVER_HOST"], int(config["SERVER"]["SERVER_PORT"]))
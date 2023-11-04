import socket
import configparser

def client_handler(host, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    while True:
        print('type your message: ')
        request = input()
        request = request.encode('utf-8')
        client_socket.sendall(request)
        answer = client_socket.recv(4096)
        answer = answer.decode('utf-8')
        print(answer)

if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read("server_config.ini")

    #print(config["SERVER"]["SERVER_HOST"])
    client_handler(config["SERVER"]["SERVER_HOST"], int(config["SERVER"]["SERVER_PORT"]))
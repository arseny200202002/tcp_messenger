import socket
import configparser

from client_logic import *

class client_data:
    def __init__(self):
        chat_name = ''

def client_handler(host, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    raw_answer = client_socket.recv(1024).decode()
    answer = parse_server_answer(raw_answer)
    template = answer.template

    while True:
        # input part
        request = input_templates.templates[template]()
        
        # если на этапе проверки введенных данных возникла ошибка
        if request == 'error':
            print(client_error_messages[template])
            continue
        # send request
        client_socket.sendall(request)
        # receive answer 
        raw_answer = client_socket.recv(1024).decode()
        print(f"server answer is: {raw_answer}")
        # process answer
        answer = parse_server_answer(raw_answer)

        # обработка ошибок
        if answer.template != 'error':
            template = answer.template # вызываем новый шаблон если не было ошибки на строне сервера
        else:
            print(server_error_messages[template])
            pass
        

if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read("server_config.ini")

    client_handler(config["SERVER"]["SERVER_HOST"], int(config["SERVER"]["SERVER_PORT"]))
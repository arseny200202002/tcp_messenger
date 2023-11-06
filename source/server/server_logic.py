from db.db_requests import *

state_tree = [
    [1, 2],
    [3],
    [3],
    [4, 5],
    [6],
    [6],
]

backward_state_tree = [
    0,
    0,
    0,
    3,
    3,
    3,
    5,
]

state_names = {
    0: 'start',
    1: 'sing_in',
    2: 'sing_up',
    3: 'main',
    4: 'create_chat',
    5: 'choose_chat',
    6: 'send_message',
}


class state_machine:
    def start(data):
        pass
    def sing_in(data):
        pass
    def sing_up(data):
        pass
    def main(data):
        pass
    def create_chat(data):
        pass
    def choose_chat(data):
        pass
    def send_message(data):
        chat_id = data
        #message = Messages(text=text, send_date=send_date, author_name=author_name)
        #create_message(chat_id, message)
        
    state_functions = {
        'start': start,
        'sing_in': sing_in,
        'sing_up': sing_up,
        'main': main,
        'create_chat': create_chat,
        'choose_chat': choose_chat,
        'send_message': send_message,
    }
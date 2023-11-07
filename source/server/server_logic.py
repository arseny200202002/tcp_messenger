from db.db_requests import *
import re

state_names = {
    0: 'authorization',
    1: 'login',
    2: 'register',
    3: 'main_menu',
    4: 'chat_creation',
    5: 'in_chat',
}

responce_expected = {
    0: ['COMMAND'],
    1: ['DATA', 'COMMAND'],
    2: ['DATA', 'COMMAND'],
    3: ['DATA', 'COMMAND'],
    4: ['DATA', 'COMMAND'],
    5: ['DATA', 'COMMAND'],
}

# update будет проверять не пришло ли новое сообщение или не появился ли новый чат
# пока не совсем ясно как это делать
basic_commands = {
    'EXIT': 0
    }

state_tree = {
    0: {'LOGIN': 1, 'REGISTER': 2, 'BACK': 0},
    1: {'DATA': 3, 'BACK': 0},
    2: {'DATA': 3, 'BACK': 0},
    3: {'CREATE': 4, 'DATA': 5, 'BACK': 0},
    4: {'DATA': 5, 'BACK': 3},
    5: {'DATA': 5, 'BACK': 3},
}

class state_processors:
    def authorization():
        pass
    # login : password_hash
    def login(login: str, password_hash: str):
        exists = check_sing_in(login, password_hash)
        if exists:
            user_id = get_user_id(login)
            chats = get_chats(user_id)
            return chats
        else:
            return False
    # login : password_hash : username : address : port
    def register(login: str, password_hash: str, username: str, address: str, port: int):
        exists = check_sing_up(login)
        if exists:
            return False
        else:
            create_user(login, password_hash, username, address, port)
            user_id = get_user_id(login)
            chats = get_chats(user_id)
            return chats
    # chat_name
    def choose_chat(chat_name: str) -> list:
        chat_id = get_chat_id(chat_name)
        messages = get_message_history(chat_id)
        return messages
    # creator_id : chat_name : user_1_id : user_2_id
    def create_chat(creator_id: int, chat_name: str, user_1_id: int, user_2_id: int):
        error = create_chat(creator_id, chat_name, user_1_id, user_2_id)

        if error == Exception:
            return False
        
        chat_id = get_chat_id(chat_name)
        messages = get_message_history(chat_id)
        return messages
    # chat_id : text : author_name
    def send_message(chat_id: int, text: str, author_name: str):
        send_date = datetime.now()
        error = create_message(chat_id, text, send_date, author_name)

        if error == Exception:
            return False
        
        messages = get_message_history(chat_id)
        return messages
    
    state_machine = {
        0: authorization, 
        1: login, # send chats
        2: register, # send chats
        3: choose_chat, # send message history
        4: create_chat, # send message history
        5: send_message, # update message history
    }

def parse_responce(responce: str) -> tuple:
    """
    returns tuple with type of request and body of request
    """
    try:
        keyword, body = re.split(':', responce, 1)
    except:
        return 'ERROR', ''
    if keyword == 'COMMAND':
        command = re.findall(r'\b\S+\b', body)[0]
        return 'COMMAND', command # return the found command
    if keyword == 'DATA':
        data_list = re.split('\|', body)
        return 'DATA', data_list
    else:
        return 'ERROR', ''

def process_responce(address: str, port: int, state: int, responce: tuple) -> tuple:
    """
    function creates request to the client \n
    based on the responce and its current state \n
    returns: \n 
        tuple: \n
            new state: int \n
            request from server to client: str
    """
    keyword, body = responce

    if body in list(basic_commands.keys()):
        new_state = basic_commands[body]
        request = 'TEMPLATE:' + state_names[new_state]
        return new_state, request
    
    if body not in list(state_tree[state].keys()) and keyword not in list(state_tree[state].keys()):
        return state, 'ERROR'
    if keyword == 'ERROR':
        return state, 'ERROR'
    else:
        if keyword == 'DATA':
            # validate received data
            data_to_send = state_processors.state_machine[state](*body)
            # if received data is invalid
            if data_to_send == False:
                return state, 'ERROR'
            # change state
            new_state = state_tree[state][keyword]
            # form request
            request = 'TEMPLATE:' + state_names[new_state] + ':DATA'
            for value in data_to_send:
                request += ':'
                request += str(value)
            return new_state, request
        else: 
            new_state = state_tree[state][body]
            request = 'TEMPLATE:' + state_names[new_state]
            return new_state, request
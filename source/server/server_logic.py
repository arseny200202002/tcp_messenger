from db.db_requests import *
import re
import logging

keywords = ['DATA', 'COMMAND']

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

class state_machine:
    def authorization(address, port):
        pass

    def login(username: str, password_hash: str, address: str, port: int):
        if check_user_existence(username, password_hash):
            user_id = get_user_id(username)
            connect_session(user_id, datetime.now(), address, port)
            chats = get_chats(user_id)
            return chats
        else:
            return False
    
    def register(username: str, password_hash: str, address: str, port: int):
        if check_user_existence(username, password_hash):
            return False
        else:
            result = create_user(username, password_hash, address, port)

            if result == False:

                logging.error(f"unable to create new user")

                return False

            user_id = get_user_id(username)
            chats = get_chats(user_id)
            return chats
        
    def choose_chat(chat_name: str, address, port) -> list:
        chat_id = get_chat_id(chat_name)

        if not chat_id:
            
            logging.error(f"no chat found with such name: {chat_name}")

            return False
        
        set_chat(chat_id, datetime.now(), address, port)
        messages = get_message_history(chat_id)

        return messages
    
    def create_chat(username: str, chat_name, address, port):
        user_2_id = get_user_id(username)
        creator_id = get_user_id_by_session(address, port)

        logging.info(f"creator_id: {creator_id}, second user id: {user_2_id}")

        if any([user_2_id, creator_id]) is None:

            logging.error(f"no users with such name")

            return False
        
        result = create_chat(creator_id, chat_name, creator_id, user_2_id)

        if result == False:
            
            logging.error(f"unable to create chat")

            return False
        
        chat_id = get_chat_id(chat_name)

        if not chat_id:
            
            logging.error(f"no chat found with such name: {chat_name}")

            return False

        set_chat(chat_id, datetime.now(), address, port)
        messages = get_message_history(chat_id)
        return messages
    
    def send_message(text: str, address: str, port: int):
        author_name =   get_username(address, port)
        chat_id =       get_current_chat(address, port)
        result = create_message(chat_id, text, datetime.now(), author_name)

        if result == False:

            logging.error(f"unable to create message in database")

            return False
        
        messages = get_message_history(chat_id)
        return messages
    
    state_processors = {
        0: authorization, 
        1: login,           # send chats
        2: register,        # send chats
        3: choose_chat,     # send message history
        4: create_chat,     # send message history
        5: send_message,    # update message history
    }

def parse_responce(responce: str) -> tuple:
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
    keyword, body = responce

    logging.info(f"keyword: {keyword}, body of responce: {body}, current state: {state}")

    # обработка базовых команд
    if body in list(basic_commands.keys()):
        new_state = basic_commands[body]
        request = 'TEMPLATE:' + state_names[new_state]

        logging.info(f"received command: {body}, send request: {request}")

        return new_state, request

    # обработка заведомо некорректных запросов
    if body not in list(state_tree[state].keys()) and keyword not in list(state_tree[state].keys()):

        logging.error(f"bad received command")

        return state, 'ERROR'
    if keyword == 'ERROR':

        logging.error(f"received error keyword from client")

        return state, 'ERROR'

    # обработка валидных запросов
    else:
        if keyword == 'DATA':
            # validate received data
            body.append(address)
            body.append(port)

            # check if received proper amount of values
            try:
                data_to_send = state_machine.state_processors[state](*body)
            except:
                logging.error(f"bad received data from client, current state {state_names[state]}")
                return state, 'ERROR'
            
            # if received data is invalid
            if data_to_send == False:

                logging.error(f"bad received data from client, current state: {state_names[state]}")

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